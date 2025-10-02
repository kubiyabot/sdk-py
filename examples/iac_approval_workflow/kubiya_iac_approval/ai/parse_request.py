from litellm import completion
from kubiya_iac_approval.config.prompts import PARSE_REQUEST_PROMPT


def parse_user_request(user_input: str):
    messages = [
        {"content": PARSE_REQUEST_PROMPT, "role": "system"},
        {"content": user_input, "role": "user"},
    ]
    try:
        response = completion(model="gpt-4", messages=messages, format="json")
        parsed_request = response["choices"][0]["message"]["content"]
        return parsed_request, None
    except Exception as e:
        return None, str(e)
