from openai import OpenAI

class ChatGPT:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def ask(self, request: str):
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user",
                 "content": request}
                ])
        return str(completion.choices[0].message)

    def paraphrase(self, text: str):
        template = "Paraphrase the following sentence: \"{}\"\nRespond only with the paraphrased sentence, without any additional comments."
        return self.ask(template.format(text))
