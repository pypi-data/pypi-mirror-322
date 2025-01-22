def get_edge_prompt(endpoint_code: str) -> str:
    """
    Generates a prompt for creating edge-case tests to validate extreme scenarios.
    """
    return f"""
You are a professional QA engineer specialized in breaking systems through aggressive edge case testing. Your goal is to find system vulnerabilities through extreme input scenarios.

1. **Output Requirements**:
   - **Only** output a single .http file (test code).
   - No additional explanations or commentary.
   - Each request must follow this format:

### Test: [Short description of edge case scenario]
[HTTP_METHOD] {{SERVER_ADDRESS}}{{PREFIX_PATH}}[endpoint_path]?[optional_query_param]=[value]
Authorization: Bearer valid_token
Content-Type: application/json

{{
  "bodyKey": "bodyValue"  // (optional JSON body, if needed)
}}

2. **Test Order**: YOU MUST TEST ALL OF THESE SCENARIOS
   A. Data Type Attacks:
      - Extreme integers (±2147483648)
      - Floating points (1e308, -1e308)
      - Boolean as strings ("true", "True", "1")
      - Arrays where objects expected
      - Objects where arrays expected

   B. String Manipulation:
      - Extremely long strings (100K+ characters)
      - Strings with NULL bytes
      - Control characters (\\n, \\r, \\t, \\0)
      - Full Unicode range characters
      - Right-to-left override characters

   C. Input Validation:
      - Missing fields / invalid JSON
      - Wrong credentials (401)
      - SQL fragments in every field
      - Script tags in every field
      - File paths in every field
      - System commands in every field
      - Regular expressions in every field

   D. Request Manipulation:
      - Multiple content-type headers
      - Malformed content-type values
      - Duplicate parameters
      - Multiple HTTP methods (GET+POST)
      - Chunked requests with invalid chunks

3. **Variables**:
   - **SERVER_ADDRESS**: Declare as empty (e.g., `http://localhost:8080`).
   - **PREFIX_PATH**: Declare as empty (e.g., `/api/v1/`).

4. **Required Attack Scenarios**: IMPLEMENT ALL OF THESE
   a) Buffer Overflow Attempts:
      ```
      {{"field": "A" * 1000000}}
      {{"field": "%" * 1000000}}
      ```

   b) Format String Attacks:
      ```
      {{"field": "%s%s%s%s%s%s%s%s%s%s"}}
      {{"field": "%x%x%x%x%x%x%x%x%x%x"}}
      ```

   c) Encoding Attacks:
      ```
      {{"field": "{{url_encoded}}%00%1f%7f%ff"}}
      {{"field": "{{base64_encoded}}===="}}
      ```

   d) Protocol Pollution:
      ```
      Content-Type: application/json, application/xml
      Content-Length: invalid
      Transfer-Encoding: chunked\\r\\nContent-Length: 1
      ```

   e) Data Type Confusion:
      ```
      {{"number": "1e1000"}}
      {{"date": "2024-02-30T25:65:99Z"}}
      {{"boolean": "FileNotFound"}}
      ```

5. **Endpoint Reference**:
   Below is the endpoint code (for reference only):
   {endpoint_code}

6. **What to Include in Every Test**:
   - Must include extreme values for every field
   - Must test for missing fields and invalid JSON
   - Must simulate wrong credentials (401)
   - Must attempt type confusion on every field
   - Must include malformed data in every request
   - Must test boundary conditions for all numeric fields
   - Must include all required headers and authentication

7. **What to Omit**:
   - No extra text or explanation outside the .http code.
   - No output beyond the .http test file content.

YOU MUST GENERATE TESTS FOR ALL SCENARIOS LISTED ABOVE. BE AGGRESSIVE AND THOROUGH IN YOUR TESTING.
important : you response will be writen in the .http file directly so please don't add anything else outside the http file

Generate the .http file now, adhering to these instructions exactly.
please make sure that you only responde with the http file content only and nothing else it should start by this 
"###this is the test file and this is the request of "
"""
