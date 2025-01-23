# PyTest-AI

`pytest-ai` is a Python package designed to generate comprehensive HTTP test cases for APIs, including regular, edge case, and security test scenarios.

## Features
- Generate regular tests for API endpoints.
- Test edge cases with extreme inputs.
- Validate API security against vulnerabilities like SQL injection, XSS, and more.
- Supports various language models, including any LangChain-compatible model, such as OpenAI, Claude, Mistral, Cohere, and others.

## Installation
Install the package using pip:
```bash
pip install pytest-ai
```

## Usage

### Example
Here is an example of how to use the package to generate HTTP tests:

```python
import asyncio
import os
from dotenv import load_dotenv

# Import the test generator
from pytest_ai.test_generator import generate_tests_for_directory

# Load environment variables
load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")

# Import and initialize your language model
# You can use any LangChain-compatible model
from langchain_openai import ChatOpenAI
model = ChatOpenAI(model="gpt-4o-mini")

# Define the folder containing your API routes
RoutesFolder = "/path/to/your/routes"

# Run the test generation
asyncio.run(generate_tests_for_directory(RoutesFolder, model))
```

### What Happens When You Run the Script
- The package will create a folder named `tests` in the same directory as the provided routes folder.
- Inside the `tests` folder, it will generate three subfolders:
  - `tests_regular`: Contains HTTP tests for regular scenarios.
  - `tests_edge`: Contains HTTP tests for edge cases with extreme inputs.
  - `tests_security`: Contains HTTP tests for security vulnerabilities.
- Each test is saved as an `.http` file, organized by category.

### Configuration
- **Server Address and Prefix Path**: The generated `.http` test files include placeholders for the server address (`SERVER_ADDRESS`) and prefix path (`PREFIX_PATH`). You can configure them as needed after generation.

## License
This project is licensed under the Apache License 2.0. See the LICENSE file for details.

