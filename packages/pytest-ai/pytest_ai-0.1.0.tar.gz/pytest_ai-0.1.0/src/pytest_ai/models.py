from pydantic import  BaseModel , Field
from typing_extensions import Annotated, TypedDict


class HttpCode(BaseModel):

    """model for structured HTTP code generation response"""
    code: dict[str, str] = Field(description="the .http file content to test given endpoint . this is the generated test case code")
class http_code(TypedDict):
    description:Annotated[str, ..., "the .http file content to test given endpoint . this is the generated test case code"]
    code:Annotated[str, ..., "the .http file content to test given endpoint . this is the generated test case code"]
