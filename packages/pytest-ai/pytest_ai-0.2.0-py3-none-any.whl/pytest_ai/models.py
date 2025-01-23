from pydantic import  BaseModel , Field


class HttpCode(BaseModel):

    """model for structured HTTP code generation response"""
    code: dict[str, str] = Field(description="the .http file content to test given endpoint . this is the generated test case code")
