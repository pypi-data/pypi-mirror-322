import os
import subprocess
from pathlib import Path
from tqdm import tqdm

def installing_animation(command):
    """Execute a command and display a progress bar based on the process"""
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # Create a progress bar with `tqdm`
    for line in iter(process.stdout.readline, ''):
        if line:
            # Display each line of the standard output
            print(line.strip())
            # Update the progress bar
            tqdm.write(line.strip())
    process.stdout.close()
    process.wait()

def main():
    project_name = input("Django project name: ")
    
    # 1. Create the Django project
    print("Creating the Django project...")
    subprocess.run(["django-admin", "startproject", project_name])

    # 2. Initialize Git
    os.chdir(project_name)
    print("Initializing Git...")
    subprocess.run(["git", "init"])

    # 3. Create a .gitignore file
    print("Creating the .gitignore file...")
    gitignore_content = """
    *.pyc
    __pycache__/
    db.sqlite3
    .env
    """
    with open(".gitignore", "w") as f:
        f.write(gitignore_content)

    # 4. Create a .env file
    print("Creating the .env file...")
    env_content = """
    SECRET_KEY=change-me
    DEBUG=True
    """
    with open(".env", "w") as f:
        f.write(env_content)

    # 5. Add dependencies to requirements.txt
    print("Creating requirements.txt...")
    with open("requirements.txt", "w") as f:
        f.write("Django\ndjangorestframework\ndjango-filter\n")

    # 6. Install dependencies in real-time with `tqdm`
    print("Installing dependencies with pip...")
    installing_animation(["pip", "install", "-r", "requirements.txt"])

    # 7. Add django_rest_framework to INSTALLED_APPS
    # settings_path = Path(project_name) / project_name / "settings.py"
    # app_name = "rest_framework"
    # print(f"Adding '{app_name}' to INSTALLED_APPS in {settings_path}...")
    # with open(settings_path, "r") as f:
    #     settings = f.read()

    # if "INSTALLED_APPS" in settings:
    #     settings = settings.replace(
    #         "INSTALLED_APPS = [",
    #         f"INSTALLED_APPS = [\n    '{app_name}',"
    #     )

    # with open(settings_path, "w") as f:
    #     f.write(settings)
    
    print("\nDjango project initialized successfully!")

if __name__ == "__main__":
    main()
