from typing import Literal

from pydantic import BaseModel


class EvalCase(BaseModel):
    input: str
    output: str
    tools: list


class Message(BaseModel):
    role: Literal["user", "assistant", "tool_call", "tool_response"]
    content: str = ""
    tool_name: str = ""
    tool_args: str = ""
    tool_response: str = ""
    event_id: str = ""
    invocation_id: str = ""
