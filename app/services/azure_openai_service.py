"""
Azure OpenAI service.

Provides Azure OpenAI access using Azure identity-based authentication.
"""

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import OpenAI

from app.core.config import settings


class AzureOpenAIService:
    """
    Service responsible for communicating with Azure OpenAI.
    """

    def __init__(self) -> None:
        """
        Initialize the Azure OpenAI client.
        """

        if not settings.azure_openai_endpoint:
            raise ValueError("AZURE_OPENAI_ENDPOINT is not configured.")

        if not settings.azure_openai_deployment:
            raise ValueError("AZURE_OPENAI_DEPLOYMENT is not configured.")

        credential = DefaultAzureCredential()

        token_provider = get_bearer_token_provider(
            credential,
            "https://ai.azure.com/.default",
        )

        self._client = OpenAI(
            base_url=(f"{settings.azure_openai_endpoint.rstrip('/')}" "/openai/v1/"),
            api_key=token_provider,
        )

        self._deployment = settings.azure_openai_deployment

    def generate_response(
        self,
        prompt: str,
    ) -> str:
        """
        Generate an AI response using Azure OpenAI.
        """

        response = self._client.chat.completions.create(
            model=self._deployment,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an enterprise IT helpdesk assistant. "
                        "Provide concise, safe, and useful IT support."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        content = response.choices[0].message.content

        if content is None:
            return ""

        return content
