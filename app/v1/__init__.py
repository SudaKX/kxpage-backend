
from google.protobuf.message import Message
from fastapi import Response
from app.pbf import Event_pb2
from app.config import ADMIN_HASH

def parse_protobuf(
    msg_type: str, data: bytes, validation: str | None = None
) -> tuple[bool, Response | Message]:
    message = getattr(Event_pb2, msg_type)
    wrapped: Message = message()
    try:
        wrapped.ParseFromString(data)
    except Exception:
        response: Message = Event_pb2.StateResponse()
        response.message = "failed"
        return False, Response(
            response.SerializeToString(), 400,
            media_type="application/octet-stream"
        )
    if validation:
        given_hash = getattr(wrapped, validation)
        if given_hash != ADMIN_HASH:
            response: Message = Event_pb2.StateResponse()
            response.message = "failed"
            return False, Response(
                response.SerializeToString(), 401,
                media_type="application/octet-stream"
            )
    return True, wrapped
