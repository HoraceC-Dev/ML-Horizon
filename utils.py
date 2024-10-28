import importlib.util
import os

def find_and_import_module(module_name, function_name):
    # Walk through the directories to find the module
    for root, dirs, files in os.walk('.'):  # Starts searching from the current directory
        if f"{module_name}.py" in files:
            # Construct the full path to the module
            module_path = os.path.join(root, f"{module_name}.py")

            # Import the module dynamically
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Get the function from the imported module
            if hasattr(module, function_name):
                return getattr(module, function_name)
            else:
                raise ImportError(f"Function '{function_name}' not found in '{module_name}'")

    raise FileNotFoundError(f"Module '{module_name}.py' not found in the directory tree.")
