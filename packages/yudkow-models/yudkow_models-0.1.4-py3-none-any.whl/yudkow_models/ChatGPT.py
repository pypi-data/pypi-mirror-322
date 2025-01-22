from openai import OpenAI

class ChatGPT:
    def __init__(self, api_key, paraphrase_prompt="Paraphrase the following sentence: \"{}\"\nRespond only with the paraphrased sentence, without any additional comments."):
        self.client = OpenAI(api_key=api_key)
        self.paraphrase_prompt = paraphrase_prompt

    def ask(self, request: str):
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user",
                 "content": request}
                ])
        return completion.choices[0].message.content

    def paraphrase(self, text: str):
        return self.ask(self.paraphrase_prompt.format(text))
