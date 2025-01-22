from openai import OpenAI
from openai import AzureOpenAI
from pydantic import BaseModel
import os
import openai
import json
import time
from typing import Optional, Union, Literal

# TODO: Add Azure OpenAI Implementation

class OpenAIResponse(BaseModel):
    """
    OpenAI Response Model.
    """
    content: Union[str, dict]
    token_usage: dict
    model: str
    response_format: Literal["string", "json"]

    def to_json(self):
        """Converts the Pydantic object to JSON/dict for client use."""
        return self.dict()

class OpenAIWrapper:
    def __init__(
        self, 
        api_key: Optional[str] = None, 
        service_provider: Literal["openai", "azure"] = "openai", 
        max_retries: int = 3
    ):
        """
        Initialize the OpenAI Wrapper.
        
        :param api_key: OpenAI API key. Reads from environment if not provided.
        :param service_provider: Service provider, either 'openai' or 'azure'.
        :param max_retries: Maximum number of retries for API calls.
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("API key is required. Set it in environment or pass explicitly.")
        
        self.service_provider = service_provider
        self.max_retries = max_retries
        
        if service_provider == "openai":
            openai.api_key = self.api_key
        elif service_provider == "azure":
            openai.api_type = "azure"
            openai.api_key = self.api_key
            openai.api_base = os.getenv("AZURE_OPENAI_API_BASE")
            openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2023-05-15")
        else:
            raise ValueError("Invalid service provider. Choose 'openai' or 'azure'.")

    def _retry_api_call(self, func, *args, **kwargs):
        """
        Retry logic for API calls.
        """
        attempts = 0
        while attempts < self.max_retries:
            try:
                return func(*args, **kwargs)
            except openai.OpenAIError as e:
                attempts += 1
                if attempts >= self.max_retries:
                    raise e
                time.sleep(2 ** attempts)

    def generate_response(
        self, 
        system_prompt: str, 
        user_prompt: str, 
        model: str = "gpt-4o", 
        max_tokens: int = 150, 
        temperature: float = 0.7, 
        output_format: Literal["string", "json"] = "string"
    ) -> Union[str, dict]:
        """
        Generate a response from OpenAI or Azure OpenAI service.
        
        :param system_prompt: The system prompt to set the assistant's behavior.
        :param user_prompt: The user's prompt to generate a response.
        :param model: Model to use for generation (e.g., 'gpt-4').
        :param max_tokens: Maximum number of tokens in the output.
        :param temperature: Sampling temperature.
        :param output_format: Format of the output, either 'str' or 'json'.
        :return: The response as a string or JSON, based on output_format.
        """

        retry_count = 0
        while retry_count < self.max_retries:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]

            try:
                response = self._retry_api_call(
                    openai.chat.completions.create,
                    model=model,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    response_format={"type": "json_object"} if output_format == "json" else None,
                )

                exact_response = response.choices[0].message.content
                print("response", response)
                token_usage = {
                    "total_tokens": response.usage.total_tokens or 0,
                    "prompt_tokens": response.usage.prompt_tokens or 0,
                    "completion_tokens": response.usage.completion_tokens or 0,
                }

                if output_format == "json":
                    exact_response = exact_response.replace("json", " ").replace("```", "")
                    try:
                        exact_response = json.loads(exact_response)
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON: {e}. Retrying generation...")
                        retry_count += 1
                        if retry_count >= self.max_retries:
                            raise ValueError(f"Failed to parse response as JSON after {self.max_retries} retries.")
                        continue
                        
                return OpenAIResponse(
                        content=exact_response, 
                        token_usage=token_usage, 
                        model=model,
                        response_format=output_format
                    ).to_json()

            except openai.OpenAIError as e:
                retry_count += 1
                if retry_count >= self.max_retries:
                    raise ValueError(f"Failed to generate a valid response after {self.max_retries} retries.")
                print(f"API call failed with error: {e}. Retrying...")
                time.sleep(2 ** retry_count)


