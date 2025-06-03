""" TNG Enterprise NCC-1701-D Computer Module """
from openai import OpenAI


class Computer:
    """ TNG Enterprise NCC-1701-D Computer """
    def __init__(self, name, model):
        self.llm = OpenAI()
        self.model = 'gpt-4o-mini'

    def summarize_please(self, text: str) -> str:
        """
        Summarize the text provided.

        Args:
            text (str): The text to summarize.

        Returns:
            str: The summarized text.

        """
        completion = self.llm.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": text
                }
            ]
        )

        try:
            return completion.choices[0].message
        except IndexError as error:
            return f"Error attempting to return choice[0].message: {error}"

