import importlib.util
import json
import os
import shutil
import subprocess
import sys
import traceback

import requests
import yaml

from infsh import BaseApp, BaseAppInput, BaseAppOutput

# ANSI color codes
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

# Import default template contents
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")
DEFAULT_TEMPLATES = {
    ".gitignore": None,
    "inf.yml": None, 
    "inference.py": None,
    "schema.json": None
}

# Load all template contents
for template in DEFAULT_TEMPLATES:
    with open(os.path.join(TEMPLATES_DIR, template)) as f:
        DEFAULT_TEMPLATES[template] = f.read()

def generate_default_init_py():
    """Generate __init__.py if it doesn't exist."""
    if os.path.exists("__init__.py"):
        print("» __init__.py already exists, skipping...")
        return False
    
    print("» Creating __init__.py...")
    with open("__init__.py", "w") as f:
        f.write("")
    print(f"{GREEN}✓ Created __init__.py{RESET}")
    return True

def generate_default_yaml():
    """Generate inf.yml if it doesn't exist."""
    if os.path.exists("inf.yml"):
        with open("inf.yml", "r") as f:
            config = yaml.safe_load(f)
        print(f"{YELLOW}⚠ inf.yml already exists with name: {config['name']}{RESET}")
        return False
    
    print("» Creating inf.yml...")
    with open("inf.yml", "w") as f:
        f.write(DEFAULT_TEMPLATES["inf.yml"].strip())
    print(f"{GREEN}✓ Created inf.yml{RESET}")
    return True

def generate_default_inference():
    """Generate inference.py if it doesn't exist."""
    if os.path.exists("inference.py"):
        print("» inference.py already exists, skipping...")
        return False
    
    print("» Creating inference.py...")
    with open("inference.py", "w") as f:
        f.write(DEFAULT_TEMPLATES["inference.py"].strip())
    print(f"{GREEN}✓ Created inference.py{RESET}")
    return True

def generate_default_requirements():
    """Generate requirements.txt if it doesn't exist."""
    if os.path.exists("requirements.txt"):
        print(f"{YELLOW}⚠ requirements.txt already exists, skipping...{RESET}")
        return False
    
    print(f"{BLUE}» Creating requirements.txt...{RESET}")
    with open("requirements.txt", "w") as f:
        f.write("pydantic>=2.0.0\n")
        f.write("infsh\n")
    print(f"{GREEN}✓ Created requirements.txt{RESET}")
    return True

def generate_default_gitignore():
    """Generate .gitignore if it doesn't exist."""
    if os.path.exists(".gitignore"):
        print("» .gitignore already exists, skipping...")
        return False
    
    print("» Creating .gitignore...")
    with open(".gitignore", "w") as f:
        f.write(DEFAULT_TEMPLATES[".gitignore"].strip())
    print("✓ Created .gitignore")
    return True

def generate_default_schema():
    """Generate schema.json if it doesn't exist."""
    if os.path.exists("schema.json"):
        print("» schema.json already exists, skipping...")
        return False
    
    print("» Creating schema.json...")
    with open("schema.json", "w") as f:
        f.write(DEFAULT_TEMPLATES["schema.json"].strip())
    print(f"{GREEN}✓ Created schema.json{RESET}")
    return True

def create_app():
    """Create a new inference.sh application."""
    generate_default_yaml()
    generate_default_inference()
    generate_default_requirements()
    generate_default_gitignore()
    generate_default_schema()
    print(f"{GREEN}✓ Successfully created new inference.sh app structure!{RESET}")

def login():
    """Login to inference.sh (dummy implementation)."""
    # Dummy implementation
    print("✓ Logged in as: test_user")
    return "test_user"

def generate_schema(module) -> dict:
    """Generate simplified schema from AppInput and AppOutput models."""
    print(f"{BLUE}» Generating schema...{RESET}")
    schema = {
        "input": module.AppInput.model_json_schema(),
        "output": module.AppOutput.model_json_schema()
    }
    print(f"{GREEN}✓ Schema generated successfully{RESET}")
    return schema

def generate_requirements(temp_dir):
    """Generate requirements.txt."""
    print(f"{BLUE}» Generating requirements.txt...{RESET}")
    
    # Check if requirements.txt exists and has more than 2 lines
    if os.path.exists("requirements.txt"):
        with open("requirements.txt") as f:
            existing_reqs = f.readlines()
        if len([line for line in existing_reqs if line.strip()]) > 2:
            print(f"{YELLOW}⚠ requirements.txt has manual changes, skipping automatic generation{RESET}")
            return
    
    requirements = []
    # Add infsh requirement without version
    requirements.append("infsh")
    
    # Add pydantic requirement if not already present
    if not any(req.startswith("pydantic>=") for req in requirements):
        requirements.append("pydantic>=2.0.0")

    # Capture pipreqs output instead of writing to file
    result = subprocess.run(["pipreqs", temp_dir, "--print"], capture_output=True, text=True, check=True)
    pipreqs_requirements = result.stdout.splitlines()
    
    # Remove duplicate requirements by keeping only the latest version of each package
    print(f"{YELLOW}⚠ Warning: Automatic requirement generation is experimental{RESET}")
    print(f"{YELLOW}⚠ It might choose incorrect package versions{RESET}")
    print(f"{YELLOW}⚠ Use this as a starting point and verify requirements.txt is correct{RESET}")
    unique_reqs = {}
    for req in pipreqs_requirements:
        pkg_name = req.split('==')[0].split('>=')[0].strip()
        unique_reqs[pkg_name] = req
    pipreqs_requirements = list(unique_reqs.values())
    
    # Remove infsh related requirements
    pipreqs_requirements = [req for req in pipreqs_requirements if not req.startswith("infsh")]
    
    # Write combined requirements to file
    requirements.extend(pipreqs_requirements)
    with open("requirements.txt", "w") as f:
        f.write("\n".join(requirements) + "\n")
        
    print(f"{GREEN}✓ Requirements.txt generated successfully ({len(requirements)} dependencies){RESET}")

def predeploy():
    """Run predeploy checks."""
    print(f"{BLUE}» Running predeploy checks...{RESET}")
    try:
        # Generate missing files if needed
        if not os.path.exists("inf.yml"):
            print(f"{BLUE}» Creating inf.yml...{RESET}")
            generate_default_yaml()
        if not os.path.exists("inference.py"):
            print(f"{BLUE}» Creating inference.py...{RESET}")
            generate_default_inference()
        if not os.path.exists("requirements.txt"):
            print(f"{BLUE}» Creating requirements.txt...{RESET}")
            generate_default_requirements()
        if not os.path.exists(".gitignore"):
            print(f"{BLUE}» Creating .gitignore...{RESET}")
            generate_default_gitignore()

        # Check if git is initialized
        if not os.path.exists(".git"):
            init_git()
        
        # Check if there are any changes to commit
        status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        if status.stdout:
            print(f"{RED}✗ Uncommitted changes detected. Please commit all changes before deploying{RESET}")
            return False

        # Use the context manager to handle imports
        with TemporaryPackageStructure() as package:
            print(f"{GREEN}✓ inference.py successfully imported{RESET}")
            
            # Check required classes and methods
            inference_app = package.module.App()
            if not all(hasattr(inference_app, method) for method in ['setup', 'run', 'unload']):
                print(f"{RED}✗ App must implement setup, run, and unload methods{RESET}")
                return False
            print(f"{GREEN}✓ App implements required methods: setup, run, unload{RESET}")

            # Verify App is a valid class
            if not isinstance(package.module.App, type) or not issubclass(package.module.App, BaseApp):
                print(f"{RED}✗ App must be a class that inherits from BaseApp{RESET}")
                return False
            print(f"{GREEN}✓ App class inherits from BaseApp{RESET}")

            # Verify AppInput and AppOutput are valid models
            if not (isinstance(package.module.AppInput, type) and issubclass(package.module.AppInput, BaseAppInput)):
                print(f"{RED}✗ AppInput must inherit from BaseAppInput{RESET}")
                return False
            print(f"{GREEN}✓ AppInput model inherits from BaseAppInput{RESET}")
            if not (isinstance(package.module.AppOutput, type) and issubclass(package.module.AppOutput, BaseAppOutput)):
                print(f"{RED}✗ AppOutput must inherit from BaseAppOutput{RESET}")
                return False
            print(f"{GREEN}✓ AppOutput model inherits from BaseAppOutput{RESET}")

            # Generate schema
            schema = generate_schema(package.module)
            
            with open("schema.json", "w") as f:
                json.dump(schema, f, indent=2)

            generate_requirements(package.temp_dir)

            print(f"{GREEN}✓ All predeploy checks passed{RESET}")
            return True

    except Exception as e:
        print(f"\n{RED}✗ Predeploy failed:{RESET}")
        print(f"{RED}✗ Type: {type(e).__name__}{RESET}")
        print(f"{RED}✗ Message: {str(e)}{RESET}")
        
        print(f"\n{YELLOW}⚠ Traceback:{RESET}")
        traceback.print_exc()
        return False

def get_app_yaml():
    """Get the app.yml file."""
    with open("inf.yml", "r") as f:
        return yaml.safe_load(f)
    
def get_schema_json():
    """Get the schema.json file."""
    with open("schema.json", "r") as f:
        return json.load(f)

def get_api_key():
    """Get the API key from the environment variable."""
    return os.getenv("INFSH_APIKEY")

def register():
    """Register the app to inference.sh."""
    app_yaml = get_app_yaml()
    schema_json = get_schema_json()

    app_name = app_yaml.get("name", "")
    app_description = app_yaml.get("description", "")
    app_repository = app_yaml.get("repository", "")
    app_version = app_yaml.get("version", "")
    api_key = get_api_key()
    
    register_url = "http://localhost:8080/internal/apps"

    register_data = {
        "app": {
            "name": app_name,
            "description": app_description,
            "repository": app_repository,
            "schema": schema_json,
            "version": app_version
        }
    }

    try:
        response = requests.post(
            register_url,
            json=register_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
        )
        response.raise_for_status()
        print(f"✓ Successfully registered app '{app_name}'")
        return True

    except requests.exceptions.RequestException as e:
        print(f"{RED}✗ Failed to register app: {str(e)}{RESET}")
        if isinstance(e, requests.exceptions.HTTPError):
            if e.response.status_code == 401:
                print(f"{RED}✗ Authentication failed. Please check your API key{RESET}")
            elif e.response.status_code == 403:
                print(f"{RED}✗ Permission denied. You don't have access to register apps{RESET}")
            elif e.response.status_code == 409:
                print(f"{RED}✗ App name already exists. Please choose a different name{RESET}")
            elif e.response.status_code == 400:
                print(f"{RED}✗ Invalid request. Please check your app configuration{RESET}")
            else:
                print(f"{RED}✗ HTTP error occurred: {e.response.status_code}{RESET}")
                if e.response.text:
                    print(f"{RED}✗ Response: {e.response.text}{RESET}")
        elif isinstance(e, requests.exceptions.ConnectionError):
            print(f"{RED}✗ Failed to connect to server. Please check your internet connection{RESET}")
        elif isinstance(e, requests.exceptions.Timeout):
            print(f"{RED}✗ Request timed out. Please try again{RESET}")
        return False
    
def init_git():
    """Initialize git repository."""
    if not os.path.exists(".git"):
        print("» Initializing git repository...")
        subprocess.run(["git", "init"], check=True)
        print(f"{GREEN}✓ Git repository initialized{RESET}")
        return True
    
    # Do initial commit
    print("» Creating initial commit...")
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)
        print(f"{GREEN}✓ Created initial commit{RESET}")
    except subprocess.CalledProcessError:
        print(f"{RED}✗ Failed to create initial commit{RESET}")
        return False
    
    print(f"{YELLOW}⚠ Git repository already initialized{RESET}")
    return False

def deploy():
    """Deploy the app to inference.sh."""
    print("» Starting deployment process...")
    predeploy()        
    # Check if remote exists
    try:
        subprocess.run(["git", "remote", "get-url", "origin"], check=True)
        print(f"{GREEN}✓ Remote repository configured{RESET}")
    except subprocess.CalledProcessError:
        print(f"{RED}✗ Remote repository not found. Please run 'git remote add origin <your-repo-url>' first{RESET}")
        return False

    try:
        subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
        print(f"{GREEN}✓ Code pushed to remote repository{RESET}")
    except subprocess.CalledProcessError:
        print(f"{RED}✗ Failed to push to remote repository. Please check your git configuration{RESET}")
        return False
    print(f"{GREEN}✓ Application deployed successfully{RESET}")

    try:
        register()
    except Exception as e:
        print(f"{RED}✗ Failed to register app: {str(e)}{RESET}")
        return False
    return True

class TemporaryPackageStructure:
    def __init__(self):
        print(f"{BLUE}» Creating temporary package structure...{RESET}")
        self.current_dir = os.getcwd()
        self.infsh_dir = os.path.join(self.current_dir, ".infsh")
        self.temp_dir = os.path.join(self.infsh_dir, "build")
        self.module = None
        print(f"{GREEN}» Temporary package structure created{RESET}")

    def __enter__(self):
        print(f"{BLUE}» Entering temporary package structure...{RESET}")
        # Create .infsh/build structure
        os.makedirs(self.temp_dir, exist_ok=True)
            
        # Copy entire directory contents
        print(f"{BLUE}» Copying directory contents to temporary build directory...{RESET}")
        for item in os.listdir(self.current_dir):
            # Skip .infsh directory and any other hidden files/directories
            if item.startswith('.'):
                continue
                
            source = os.path.join(self.current_dir, item)
            destination = os.path.join(self.temp_dir, item)
            
            if os.path.isdir(source):
                if os.path.exists(destination):
                    shutil.rmtree(destination)
                shutil.copytree(source, destination)
            else:
                shutil.copy2(source, destination)
        
        # Create __init__.py if it doesn't exist
        print(f"{BLUE}» Creating temporary __init__.py...{RESET}")
        init_path = os.path.join(self.temp_dir, "__init__.py")
        if not os.path.exists(init_path):
            with open(init_path, "w") as f:
                pass
            
        # Add the parent directory to sys.path so Python treats the build dir as a package
        print(f"{BLUE}» Adding parent directory to sys.path...{RESET}")
        if os.path.dirname(self.temp_dir) not in sys.path:
            sys.path.insert(0, os.path.dirname(self.temp_dir))
            
        # Import module as part of the build package
        print(f"{BLUE}» Importing module as part of the build package...{RESET}")
        spec = importlib.util.spec_from_file_location(
            "build.inference",
            os.path.join(self.temp_dir, "inference.py")
        )
        if not spec or not spec.loader:
            raise ImportError("Cannot load inference.py")
            
        self.module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = self.module
        spec.loader.exec_module(self.module)
        
        print(f"{GREEN}✓ Module imported successfully{RESET}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"{BLUE}» Exiting temporary package structure...{RESET}")
        # Clean up build directory but keep .infsh
        # shutil.rmtree(self.temp_dir)
        if "build.inference" in sys.modules:
            del sys.modules["build.inference"]
