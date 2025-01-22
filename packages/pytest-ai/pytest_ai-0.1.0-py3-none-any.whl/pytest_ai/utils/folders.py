import os

def create_tests_folder(base_folder: str) -> dict:
    """
    Creates and separates folders for different test categories.

    Args:
        base_folder (str): The base directory where the test folders will be created.

    Returns:
        dict: A dictionary containing paths to the created test folders.
    """
    folders = {
        "regular": os.path.join(base_folder, "tests/tests_regular"),
        "edge": os.path.join(base_folder, "tests/tests_edge"),
        "security": os.path.join(base_folder, "tests/tests_security")  # Fixed the typo here
    }
    print("dict_created")
    for path in folders.values():
        os.makedirs(path, exist_ok=True)
    print("folder_created")

    return folders
