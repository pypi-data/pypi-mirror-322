def get_security_prompt(endpoint_code: str) -> str:
    """
    Generates a prompt for creating security tests to validate against vulnerabilities.
    """
    return f"""
You are an aggressive security tester specialized in finding critical vulnerabilities. Your goal is to attempt every possible attack vector against the API endpoints.

1. **Output Requirements**:
   - **Only** output a single .http file (test code).
   - No additional explanations or commentary.
   - Each request must follow this format:

### Test: [Short description of security test scenario]
[HTTP_METHOD] {{SERVER_ADDRESS}}{{PREFIX_PATH}}[endpoint_path]?[optional_query_param]=[value]
Authorization: Bearer valid_token
Content-Type: application/json

{{
  "bodyKey": "bodyValue"  // (optional JSON body, if needed)
}}

2. **Test Order**: YOU MUST TEST ALL OF THESE ATTACK VECTORS
   A. Injection Attacks:
      - SQL Injection (Multiple variants)
      - NoSQL Injection
      - Command Injection
      - Template Injection
      - LDAP Injection
      - XML Injection
      - XPATH Injection

   B. Cross-Site Attacks:
      - XSS (Reflected, Stored, DOM)
      - CSRF with various tokens
      - XSSI attempts
      - Clickjacking

   C. Authentication Attacks:
      - JWT tampering
      - OAuth exploitation
      - Session fixation
      - Cookie manipulation

   D. Server Attacks:
      - Path traversal
      - File inclusion
      - DoS attempts
      - Buffer overflow
      - Memory leaks

3. **Variables**:
   - **SERVER_ADDRESS**: Declare as empty (e.g., `http://localhost:8080`).
   - **PREFIX_PATH**: Declare as empty (e.g., `/api/v1/`).

4. **Required Attack Payloads**: IMPLEMENT ALL OF THESE
   a) SQL Injection (Try all variants):
      ```
      {{"field": "' OR '1'='1"}}
      {{"field": "'; DROP TABLE users; --"}}
      {{"field": "' UNION SELECT NULL,NULL,NULL,NULL,NULL--"}}
      {{"field": "' WAITFOR DELAY '0:0:10'--"}}
      {{"field": "')) OR 1=1--"}}
      ```

   b) NoSQL Injection:
      ```
      {{"field": {{"$gt": ""}}}}
      {{"field": {{"$where": "function() {{ return true; }}"}}}}
      {{"field": {{"$regex": ".*"}}}}
      ```

   c) XSS Payloads:
      ```
      {{"field": "<script>alert(document.cookie)</script>"}}
      {{"field": "<img src='x' onerror='alert(1)'>"}}
      {{"field": "javascript:alert(document.domain)"}}
      {{"field": "<svg onload='alert(1)'>"}}
      {{"field": "\\"><script>alert(1)</script>"}}
      ```

   d) Command Injection:
      ```
      {{"field": "| cat /etc/passwd"}}
      {{"field": "; rm -rf /"}}
      {{"field": "\`id\`"}}
      {{"field": "$(whoami)"}}
      ```

   e) Path Traversal:
      ```
      {{"path": "../../../etc/passwd"}}
      {{"path": "..%2f..%2f..%2fetc%2fpasswd"}}
      {{"path": "\\..\\..\\windows\\win.ini"}}
      ```

   f) Authentication Attacks:
      ```
      Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0
      Authorization: Bearer ' OR '1'='1
      Cookie: session=../../etc/passwd
      ```

5. **Endpoint Reference**:
   Below is the endpoint code (for reference only):
   {endpoint_code}

6. **What to Include in Every Test**:
   - Must try every injection attack on every field
   - Must include all XSS variants
   - Must attempt all authentication bypasses
   - Must test for every type of injection
   - Must include malicious payloads in headers
   - Must try path traversal on all paths
   - Must attempt command injection everywhere

7. **What to Omit**:
   - No extra text or explanation outside the .http code.
   - No output beyond the .http test file content.

YOU MUST GENERATE TESTS FOR ALL ATTACK VECTORS LISTED ABOVE. BE AGGRESSIVE AND THOROUGH IN YOUR SECURITY TESTING.
important : you response will be writen in the .http file directly so please don't add anything else outside the http file
please make sure that you only responde with the http file content only and nothing else it should start by this 
###this is the test file and this is the request of """
