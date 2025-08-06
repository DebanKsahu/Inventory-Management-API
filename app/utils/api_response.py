from typing import Any

from pydantic import BaseModel

from app.utils.enums import ResponseStatus


class APIResponse(BaseModel):
    response_status: ResponseStatus
    message: str
    data: Any | None

    @classmethod
    def successful_response(cls, data: Any | None = None, message: str = "Task successfully performed"):
        return cls(response_status = ResponseStatus.SUCCESS, message = message, data = data)
    
    @classmethod
    def unsuccessful_response(cls, message: str = "Some error occured"):
        return cls(response_status = ResponseStatus.FAIL, message = message, data = None)