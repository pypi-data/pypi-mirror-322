"""Models for AWS Lambda handler utilities.

Defines request and response structures for Lambda functions.
"""
import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any, Optional, Dict, Union, TypeVar, Generic, TypedDict

from chainsaws.utils.dict_utils import convert_decimal_to_number

T = TypeVar('T')

class RequestContext(TypedDict, total=False):
    """AWS API Gateway request context."""
    identity: Dict[str, Any]
    request_id: Optional[str]
    domain_name: Optional[str]
    api_id: Optional[str]
    account_id: Optional[str]
    stage: Optional[str]

    @staticmethod
    def get_source_ip(identity: Dict[str, Any]) -> Optional[str]:
        """Get source IP address from request context."""
        return identity.get("sourceIp")


class ResponseHeaders(TypedDict, total=False):
    """API Gateway response headers."""
    Access_Control_Allow_Origin: str
    Access_Control_Allow_Headers: str
    Access_Control_Allow_Credentials: bool
    Access_Control_Allow_Methods: str
    Content_Type: str
    charset: str

    @staticmethod
    def default() -> 'ResponseHeaders':
        """Get default headers."""
        return {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Credentials": True,
            "Access-Control-Allow-Methods": "*",
            "Content-Type": "application/json",
            "charset": "UTF-8"
        }


@dataclass
class HandlerConfig:
    """Configuration for Lambda handler."""
    error_receiver: Optional[Any] = None
    content_type: str = "application/json"
    use_traceback: bool = True
    ignore_app_errors: list = field(default_factory=list)


@dataclass
class ResponseMeta:
    """Response metadata."""
    rslt_cd: str = "S00000"
    rslt_msg: str = "Success"
    duration: Optional[float] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    request_id: Optional[str] = None
    traceback: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary, excluding None values."""
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class ResponseData(Generic[T]):
    """Generic response data wrapper."""
    data: T
    meta: ResponseMeta = field(default_factory=ResponseMeta)

    def to_dict(self) -> dict:
        """Convert to dictionary format."""
        return {
            "data": self.data,
            "meta": self.meta.to_dict()
        }


class LambdaEvent:
    """AWS Lambda event structure."""

    def __init__(
        self,
        body: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        request_context: Optional[RequestContext] = None,
        **kwargs: Any
    ) -> None:
        self.body = body
        self.headers = headers or {}
        self.request_context = request_context or {}
        self.raw_event = kwargs

    @classmethod
    def from_dict(cls, event: Dict[str, Any]) -> 'LambdaEvent':
        """Create LambdaEvent from dictionary."""
        return cls(
            body=event.get("body"),
            headers=event.get("headers", {}),
            request_context=event.get("requestContext", {}),
            **event
        )

    @staticmethod
    def is_api_gateway_event(event: Dict[str, Any]) -> bool:
        """Check if the event is from API Gateway (REST or HTTP)."""
        request_context = event.get("requestContext", {})
        domain_name = request_context.get("domainName", "")
        is_execute_api_url = "execute-api" in domain_name

        # Check for HTTP API (v2)
        is_http_api = (
            is_execute_api_url and
            request_context.get("apiId") is not None and
            event.get("version") == "2.0" and
            request_context.get("accountId") != "anonymous"
        )

        # Check for REST API (v1)
        is_rest_api = (
            is_execute_api_url and
            request_context.get("apiId") is not None and
            request_context.get("stage") is not None and
            event.get("version") is None
        )

        return is_http_api or is_rest_api

    @staticmethod
    def is_alb_event(event: Dict[str, Any]) -> bool:
        """Check if event is from ALB."""
        return (
            isinstance(event, dict)
            and "requestContext" in event
            and "elb" in event.get("requestContext", {})
        )

    def get_json_body(self) -> Optional[Dict[str, Any]]:
        """Get JSON body from event."""
        if not self.body:
            return None
        try:
            return json.loads(self.body)
        except json.JSONDecodeError:
            return None


class LambdaResponse:
    """Lambda response formatter."""

    @staticmethod
    def create(
        body: Union[str, dict, list],
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None,
        content_type: str = "application/json",
        status_description: Optional[str] = None,
        is_base64_encoded: bool = False,
        serialize: bool = True,
        transform_data: bool = True,
    ) -> dict:
        """Create Lambda response."""
        if not serialize:
            return body if isinstance(body, dict) else {"body": body}

        if transform_data and isinstance(body, dict):
            # Extract metadata fields
            meta = ResponseMeta(
                rslt_cd=body.pop("rslt_cd", "S00000"),
                rslt_msg=body.pop("rslt_msg", "Success"),
                duration=body.pop("duration", None),
                traceback=body.pop("traceback", None),
                request_id=body.pop("request_id", None)
            )
            
            # Create response with remaining data
            response_data = ResponseData(
                data=convert_decimal_to_number(body),
                meta=meta
            )
            body = response_data.to_dict()

        if isinstance(body, dict):
            response_data = {
                "data": {
                    k: v for k, v in body.items()
                    if k not in ["rslt_cd", "rslt_msg", "duration", "traceback", "error_receiver_failed"]
                }
            }
            for meta_key in ["rslt_cd", "rslt_msg", "duration", "traceback", "error_receiver_failed"]:
                if meta_key in body:
                    response_data[meta_key] = body[meta_key]

            body = convert_decimal_to_number(dict_detail=response_data)

            # API Gateway를 통한 호출인 경우 True
            if serialize:
                # 한글이 깨져보이는 이슈 수정
                body = json.dumps(body, ensure_ascii=False)

        response = {
            "statusCode": status_code,
            "isBase64Encoded": is_base64_encoded,
        }

        # Add headers
        response["headers"] = headers or {"Content-Type": content_type}

        # Add status description for ALB
        if status_description:
            response["statusDescription"] = status_description

        # Format body
        if isinstance(body, (dict, list)):
            response["body"] = json.dumps(body)
        else:
            response["body"] = str(body)

        return response
