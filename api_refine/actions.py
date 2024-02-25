import json
from typing import List

from components.openai_api import (
    chat,
    assign_chatgpt_role,
    make_normal_dependency_context,
    make_hierarchical_dependency_context,
    make_project_context,
    make_inputs_content_from_action_inputs,
    make_output_specifications
)


def refine_question_title(
        form_title: str,
        form_description: str,
        question_title: str
):
    chatgpt_role = assign_chatgpt_role(role="good, creative content generator")

    dependency_context = make_hierarchical_dependency_context(
        primary_inputs=["question_title"],
        secondary_inputs=["form_title", "form_description"]
    )

    project_context = make_project_context(
        main_task_as_opening="Refine the question_title in the input.",
        dependency_context=dependency_context
    )

    inputs_text = make_inputs_content_from_action_inputs(
        form_title=form_title,
        form_description=form_description,
        question_title=question_title
    )

    output_specifications = make_output_specifications(
        format_description="string",
        format_example="Will you bring any friends?"
    )

    message = chatgpt_role + project_context + inputs_text + output_specifications
    print(message)

    result = chat(
        message=message
    )

    print(result)

    return result


def refine_question_description(
        form_title: str,
        form_description: str,
        question_title: str,
        question_description: str
):
    chatgpt_role = assign_chatgpt_role(role="good, creative content generator")

    dependency_context = make_hierarchical_dependency_context(
        primary_inputs=["question_description"],
        secondary_inputs=["form_title", "form_description", "question_title"]
    )

    project_context = make_project_context(
        main_task_as_opening="Refine the question_description in the input.",
        dependency_context=dependency_context
    )

    inputs_text = make_inputs_content_from_action_inputs(
        form_title=form_title,
        form_description=form_description,
        question_title=question_title,
        question_description=question_description
    )

    output_specifications = make_output_specifications(
        format_description="string",
        format_example="Will you bring any friends?"
    )

    message = chatgpt_role + project_context + inputs_text + output_specifications
    print(message)

    result = chat(
        message=message
    )

    print(result)

    return result


def refine_options(
        question_title: str,
        current_options: List[str]
):
    chatgpt_role = assign_chatgpt_role(role="good, creative content generator")

    dependency_context = make_normal_dependency_context(
        inputs=["question_title", "current_options"]
    )

    project_context = make_project_context(
        main_task_as_opening="Generate options based on the inputs.",
        dependency_context=dependency_context,
        other_descriptions=[
            "The current_options is an array of options.",
            "The result should not includes the current_options."
            "The result should be options that makes current_options better combination."
        ]
    )

    inputs_text = make_inputs_content_from_action_inputs(
        question_title=question_title,
        current_options=current_options
    )

    output_specifications = make_output_specifications(
        format_description="array of string with 5 items maximum. Use double quotes for each item.",
        format_example='["alcohol", "onion"]'
    )

    message = chatgpt_role + project_context + inputs_text + output_specifications
    print(message)

    result = chat(
        message=message
    )

    print(result)

    return json.loads(result)
