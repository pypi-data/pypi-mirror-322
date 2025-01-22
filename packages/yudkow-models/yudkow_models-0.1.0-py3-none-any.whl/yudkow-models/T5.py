from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch


class T5:
    def __init__(self, model="google/flan-t5-base"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model).to(self.device)

    def request(self, text: str) -> str:
        input_ids = self.tokenizer(text, return_tensors="pt").input_ids.to(self.device)
        outputs = self.model.generate(input_ids, max_new_tokens=30).to(self.device)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    def text_to_keywords(self, text: str) -> str:
        return self.request("Generate a sentence with the following keywords: " + text)