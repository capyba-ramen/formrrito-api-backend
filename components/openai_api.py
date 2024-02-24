import os
from typing import List

from openai import OpenAI, APIConnectionError, RateLimitError, APIStatusError

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)


class OpenAIError(Exception):
    """An error occurred while calling the OpenAI API."""

    def __init__(self, message, original_exception):
        super().__init__(message)
        self.original_exception = original_exception


def chat(
        message: str,
):
    try:
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": message,
                }
            ],
            temperature=1,
            max_tokens=100,
            top_p=1,
            frequency_penalty=0.5,
            presence_penalty=0
        )
        return chat_completion.choices[0].message.content or ""
    except APIConnectionError as e:
        print("The server could not be reached")
        print(e.__cause__)  # an underlying Exception, likely raised within httpx.
        raise OpenAIError("The server could not be reached", e)
    except RateLimitError as e:
        print("A 429 status code was received; we should back off a bit.")
        raise OpenAIError("A 429 status code was received; we should back off a bit.", e)
    except APIStatusError as e:
        print("Another non-200-range status code was received")
        print(e.status_code)
        print(e.response)
        raise OpenAIError(
            f"Another non-200-range status code was received. Status code: {e.status_code}, Response: {e.response}", e
        )


def assign_chatgpt_role(role: str):
    # In the current use case, the role is always "good, creative content generator"
    return f"Your are a {role}."


def make_normal_dependency_context(
        inputs: List[str]
):
    return f"The result should be based on the inputs, which are {', '.join(inputs)}."


def make_hierarchical_dependency_context(
        primary_inputs: List[str],
        secondary_inputs: List[str]
):
    return f"The result should be based on the input, mainly {', '.join(primary_inputs)}, then secondarily {', '.join(secondary_inputs)}."


def make_project_context(
        main_task_as_opening: str,
        dependency_context: str,
        other_descriptions: list[str] = None
):
    result_dependent_descriptions = f"{''.join(other_descriptions)}." if other_descriptions else ""
    return main_task_as_opening + dependency_context + result_dependent_descriptions


def make_inputs_content_from_action_inputs(**kwargs):
    return f"inputs={kwargs}"


def make_output_specifications(
        format_description: str,
        format_example: str
):
    format_specification = f"Generate the result directly in {format_description}, for example: {format_example}."
    language_specification = "Generate the result in the same language as the input, if the input is Chinese, show " \
                             "traditional Chinese."
    return format_specification + language_specification
