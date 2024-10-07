import subprocess
import sys
import os

def run_commands():
    commands = [
        "python manage.py loaddata api/fixtures/assurance_goals.json",
        "python manage.py loaddata api/fixtures/categories.json",
        "python manage.py loaddata api/fixtures/sub_categories.json",
        "python manage.py import_techniques api/management/commands/explainability_techniques.csv 'Explainability'",
        "python manage.py import_techniques api/management/commands/fairness_techniques.csv 'Fairness'"
    ]
    
    for command in commands:
        try:
            # Execute the command based on the platform
            if os.name == 'nt':  # Windows
                subprocess.run(command, check=True, shell=True)
            else:  # Mac or Linux
                subprocess.run(command, check=True, shell=True, executable='/bin/bash')
            print(f"Successfully ran: {command}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to run: {command}")
            sys.exit(1)

if __name__ == "__main__":
    run_commands()