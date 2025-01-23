from os import environ
from openai import OpenAI


class OpenAIService:
    def __init__(self, prompt):
        self.prompt = prompt
        self.client = OpenAI()

    def run(self) -> None:
        response = self.client.chat.completions.create(
            model=environ["OPENAI_MODEL"],
            messages=[
                {
                    "role": "developer",
                    "content": "You are a professional software developer that performs developer tasks such as generating readme files, technical docs, generating test files etc.",
                },
                {"role": "user", "content": self.prompt},
            ],
        )
        return response.choices[0].message
