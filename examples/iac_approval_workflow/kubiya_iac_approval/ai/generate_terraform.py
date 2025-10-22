from litellm import completion
from kubiya_iac_approval.config.prompts import GENERATE_TERRAFORM_PROMPT


def generate_terraform_code(resource_details: dict):
    messages = [
        {"content": GENERATE_TERRAFORM_PROMPT, "role": "system"},
        {"content": str(resource_details), "role": "user"},
    ]
    try:
        response = completion(model="gpt-4", messages=messages, format="json")
        tf_code_details = response["choices"][0]["message"]["content"]
        return tf_code_details
    except Exception as e:
        raise ValueError(f"Failed to generate Terraform code: {str(e)}")
