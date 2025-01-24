import boto3
from typing import List, Optional
from decimal import Decimal
import asyncio
from pydantic import Field
from boto3.dynamodb.types import TypeDeserializer
from botocore.exceptions import ClientError
from tenacity import wait, stop, retry_unless_exception_type

from opal_common.fetcher.fetch_provider import BaseFetchProvider
from opal_common.fetcher.events import FetcherConfig, FetchEvent
from opal_common.logger import logger


class DynamoDBFetcherConfig(FetcherConfig):
    fetcher: str = "DynamoDBFetchProvider"
    region: str = Field(..., description="AWS region name")
    tableName: str = Field(..., description="DynamoDB table name")
    segments: int = Field(..., description="Total segments for table scanning")
    client: Optional[str] = Field(..., description="OPAL client identifier")


class DynamoDBFetchEvent(FetchEvent):
    fetcher: str = "DynamoDBFetchProvider"
    config: DynamoDBFetcherConfig = None


class DynamoDBFetchProvider(BaseFetchProvider):

    RETRY_CONFIG = {
        "wait": wait.wait_fixed(1200),
        "stop": stop.stop_after_attempt(5),
        "retry": retry_unless_exception_type(ClientError),
        "reraise": True,
    }

    def __init__(self, event: DynamoDBFetchEvent):
        if event.config is None:
            event.config = DynamoDBFetcherConfig()
        super().__init__(event)

    def parse_event(self, event: FetchEvent) -> DynamoDBFetchEvent:
        config_data = event.config
        config_instance = DynamoDBFetcherConfig(**config_data)
        return DynamoDBFetchEvent(
            **event.dict(exclude={"config"}), config=config_instance
        )

    async def _fetch_(self) -> List[dict]:
        logger.info(f"Fetching data for client: {self._event.config.client}")

        total_segments = self._event.config.segments
        scan_kwargs = {"TableName": self._event.config.tableName}

        if "Entitlements" in self._event.config.tableName and self._event.config.client:
            scan_kwargs.update(
                {
                    "FilterExpression": "clientTag = :tagValue",
                    "ExpressionAttributeValues": {
                        ":tagValue": {"S": self._event.config.client}
                    },
                }
            )

        async def scan_segment(segment: int) -> List[dict]:
            segment_kwargs = {
                **scan_kwargs,
                "Segment": segment,
                "TotalSegments": total_segments,
            }
            items = []
            try:
                response = self.client.scan(**segment_kwargs)
                items.extend(response.get("Items", []))
                while "LastEvaluatedKey" in response:
                    response = self.client.scan(
                        **segment_kwargs, ExclusiveStartKey=response["LastEvaluatedKey"]
                    )
                    items.extend(response.get("Items", []))
            except Exception as e:
                logger.error(f"Error scanning segment {segment}: {e}")
            return items

        tasks = [scan_segment(segment) for segment in range(total_segments)]
        results = await asyncio.gather(*tasks)

        all_items = [item for segment_items in results for item in segment_items]
        logger.info(
            f"Fetched {len(all_items)} items from table {self._event.config.tableName}"
        )

        return all_items

    async def __aenter__(self) -> "DynamoDBFetchProvider":
        logger.info(
            f"Entering DynamoDB Fetch Provider context with config: {self._event.config}"
        )
        self.client = boto3.client("dynamodb", region_name=self._event.config.region)
        self.serializer = TypeDeserializer()
        return self

    async def __aexit__(self, exc_type=None, exc_val=None, tb=None):
        logger.info("Exiting DynamoDB Fetch Provider context...")

    async def _process_(self, records: List[dict]) -> dict:
        deserialized_data = self.deserialize(records)
        return self.transform_response(deserialized_data)

    def convert_decimal(self, obj: Decimal) -> float:
        if isinstance(obj, Decimal):
            return float(obj)
        raise TypeError("Unexpected type for decimal conversion")

    def deserialize(self, data: dict | list | str) -> dict | list | str:
        if isinstance(data, list):
            return [self.deserialize(v) for v in data]
        if isinstance(data, dict):
            try:
                return self.serializer.deserialize(data)
            except TypeError:
                return {k: self.deserialize(v) for k, v in data.items()}
        return data

    def transform_response(self, data: List[dict]) -> dict:
        if "Entitlements" in self._event.config.tableName:
            return self._transform_entitlements(data)
        return self._transform_assignments(data)

    def _transform_entitlements(self, data: List[dict]) -> dict:
        transformed = {}
        for item in data:
            entitlement_id = item.pop("entitlementId", None)
            if entitlement_id:
                transformed[entitlement_id] = item
        return transformed

    def _transform_assignments(self, data: List[dict]) -> dict:
        transformed = {}
        for item in data:
            user_id = item.get("userId")
            if not user_id:
                continue

            assignment = {
                "createdAt": item.get("createdAt"),
                "entitlementId": item.get("entitlementId"),
                "expiryDate": item.get("expiryDate"),
                "credits": item.get("credits"),
            }

            if user_id not in transformed:
                transformed[user_id] = {"assignments": []}

            transformed[user_id]["assignments"].append(assignment)
        return transformed
