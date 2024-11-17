import sys
import os
import openai
from unittest.mock import MagicMock
import pytest

# Add the root directory to `sys.path` dynamically
sys.path.append(os.path.abspath(".."))

import chatgpt_api_client

# Mocking the chatgpt api call to avoid relying on their services everytime a test is run, avoiding unnecessary waste of tokens as well as being able to test the functionality of the code even when openAI api is unavailable.
def test_ask_normal(mocker):
    # Mock choices structure
    mock_choices = MagicMock()
    mock_choices.message.parsed.answer = "The CEO of Tehisintellekt OÜ is Kristjan Eljand."
    mock_choices.message.parsed.used_subdomains = ["https://tehisintellekt.ee/"]

    # Mock usage structure
    mock_usage = MagicMock()
    mock_usage.prompt_tokens = 14629
    mock_usage.completion_tokens = 35

    # Full mock object mimicking ParsedChatCompletion
    mock_parsed_completion = MagicMock()
    mock_parsed_completion.choices = [mock_choices]
    mock_parsed_completion.usage = mock_usage

    # Patch the actual API call to return the mock object
    mocker.patch("openai.beta.chat.completions.parse", return_value=mock_parsed_completion)

    # Call the function being tested
    question = "Who is the CEO of this company?"
    result = chatgpt_api_client.ask_chatgpt(question, "")

    # Assertions to verify the structure and values of the returned result
    assert result["response"]["user_question"] == question
    assert result["response"]["answer"] == mock_choices.message.parsed.answer
    assert result["response"]["usage"]["input_tokens"] == mock_usage.prompt_tokens
    assert result["response"]["usage"]["output_tokens"] == mock_usage.completion_tokens
    assert result["response"]["sources"] == mock_choices.message.parsed.used_subdomains

def test_ask_openAI_exception(mocker):
    # Define the exception to be raised
    exception_to_raise = openai.OpenAIError("API request failed")

    # Patch the function to raise the exception
    mocker.patch("openai.beta.chat.completions.parse", side_effect=exception_to_raise)

    # Call the function being tested
    question = "Who is the CEO of this company?"
    with pytest.raises(openai.OpenAIError):
        result = chatgpt_api_client.ask_chatgpt(question, "")