import os
import json
import tempfile
import subprocess


def create_terraform_files(tf_files: dict, working_dir: str):
    for filename, content in tf_files.items():
        with open(os.path.join(working_dir, filename), "w") as f:
            f.write(content)


def create_terraform_plan(tf_files: dict, working_dir: str) -> tuple[bool, str, dict]:
    create_terraform_files(tf_files, working_dir)

    try:
        subprocess.run(
            ["terraform", "init"],
            cwd=working_dir,
            check=True,
            capture_output=True,
            text=True,
        )
        result = subprocess.run(
            ["terraform", "plan", "-out=tfplan", "-json"],
            cwd=working_dir,
            check=True,
            capture_output=True,
            text=True,
        )

        with open(os.path.join(working_dir, "tfplan.json"), "w") as f:
            json.dump(json.loads(result.stdout), f)

        return True, "Plan created successfully", json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        return False, f"Error creating plan: {e.stderr}", {}


def apply_terraform(tf_files: dict, working_dir: str) -> tuple[str, str]:
    create_terraform_files(tf_files, working_dir)

    try:
        subprocess.run(
            ["terraform", "init"],
            cwd=working_dir,
            check=True,
            capture_output=True,
            text=True,
        )
        result = subprocess.run(
            ["terraform", "apply", "-auto-approve"],
            cwd=working_dir,
            check=True,
            capture_output=True,
            text=True,
        )

        state_result = subprocess.run(
            ["terraform", "show", "-json"],
            cwd=working_dir,
            check=True,
            capture_output=True,
            text=True,
        )
        tf_state = json.loads(state_result.stdout)

        return result.stdout, json.dumps(tf_state)
    except subprocess.CalledProcessError as e:
        return f"Error applying Terraform: {e.stderr}", ""


def run_terraform_operation(tf_files: dict, operation: str) -> tuple[bool, str, dict]:
    with tempfile.TemporaryDirectory() as tmpdir:
        if operation == "plan":
            return create_terraform_plan(tf_files, tmpdir)
        elif operation == "apply":
            output, state = apply_terraform(tf_files, tmpdir)
            return True, output, json.loads(state)
        else:
            return False, f"Unknown operation: {operation}", {}
