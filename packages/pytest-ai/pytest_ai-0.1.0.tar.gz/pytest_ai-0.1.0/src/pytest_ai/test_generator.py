import glob
import os
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate

from pytest_ai.models import HttpCode
from pytest_ai.prompts.edge import get_edge_prompt
from pytest_ai.prompts.regular import get_regular_prompt
from pytest_ai.prompts.security import get_security_prompt
from pytest_ai.utils.folders import create_tests_folder


async def generate_tests_for_directory(directory: str, model) -> None:
    """
    Generate test files for all .py files in the specified directory using streaming.

    Args:
        directory (str): The directory containing .py files for which tests will be generated.
        model: The AI model used for generating test cases.
    """
    parser = JsonOutputParser(pydantic_object=HttpCode)

    # Create test folders in the parent directory
    routes_parent = os.path.dirname(directory)
    test_folders = create_tests_folder(routes_parent)

    # Get all Python files in the directory
    py_files = glob.glob(os.path.join(directory, "*.py"))
    for py_file in py_files:
        filename = os.path.basename(py_file)
        base_name, _ = os.path.splitext(filename)

        # Read the file content
        with open(py_file, "r", encoding="utf-8") as f:
            endpoint_code = f.read()

        # Prepare prompts for all categories
        prompts = {
            "regular": get_regular_prompt(endpoint_code),
            "edge": get_edge_prompt(endpoint_code),
            "security": get_security_prompt(endpoint_code),
        }

        # Generate test cases for each category
        for category, prompt in prompts.items():
            PromptTem = PromptTemplate(
                template="this is is what you have to do{format_instructions} {prompt} please",
                input_variables=["prompt"],
                partial_variables={"format_instructions": parser.get_format_instructions()},
            )
            TestFilePath = os.path.join(test_folders[category], f"{base_name}.http")
            chain = PromptTem | model
            print("chain_created")
            #print(chain)
            r=chain.invoke({"prompt": prompt})
            #print(r)

            print(f"Generating tests for category: {category}")
            print(f"Output will be saved to: {TestFilePath}")
            chunks = []
            for chunk in chain.stream({"prompt": prompt}):
                print("streaming loop started")
                safe_content = f'"""{chunk.content}"""'
                print(safe_content,end="|")
                chunks.append(safe_content)
            final_content = "".join(chunks)
            final_content = final_content.replace('"""', '')


            with open(TestFilePath, "w", encoding="utf-8") as f:
                print(final_content)
                f.write("".join(final_content[3:-3]))





