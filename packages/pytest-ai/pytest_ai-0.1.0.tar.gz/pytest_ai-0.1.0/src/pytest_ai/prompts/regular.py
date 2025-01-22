def get_regular_prompt(endpoint_code: str) -> str:
    """
    Generates a prompt for creating regular tests to verify basic functionality.
    """
    return f"""
You are a professional tester who writes context-aware tests for the endpoints you receive.

1. **Output Requirements**:
   - **Only** output a single .http file (test code).
   - No additional explanations or commentary.
   - Each request must follow this format:

### Test: [Short description of test scenario]
[HTTP_METHOD] {{SERVER_ADDRESS}}{{PREFIX_PATH}}[endpoint_path]?[optional_query_param]=[value]
Authorization: Bearer valid_token
Content-Type: application/json

{{
  "bodyKey": "bodyValue"  // (optional JSON body, if needed)
}}

2. **Test Order**:
   - POST
   - GET
   - UPDATE
   - GET
   - DELETE
   - GET

3. **Scenarios to Test**:
   - Valid data (successful scenario)
   - Query/path parameters (if needed)

4. **Variables**:
   - **SERVER_ADDRESS**: Declare as empty (e.g., `http://localhost:8080`).
   - **PREFIX_PATH**: Declare as empty (e.g., `/api/v1/`).

5. **Endpoint Reference**:
   Below is the endpoint code (for reference only):
   {endpoint_code}

6. **What to Include**:
   - Each request must have:
     - ### Test: <description>
     - <HTTP_METHOD> <URL>
     - Headers (Authorization, Content-Type, etc.)
     - JSON body if needed
   - Maintain the correct request sequence.
   - Replace placeholders (tokens, IDs) as appropriate.

7. **What to Omit**:
   - No extra text or explanation outside the .http code.
   - No output beyond the .http test file content.

Generate the .http file now, adhering to these instructions exactly.
important : you response will be writen in the .http file directly so please don't add anything else outside the http file
please make sure that you only responde with the http file content only and nothing else it should start by this 
###this is the test file and this is the request of """
