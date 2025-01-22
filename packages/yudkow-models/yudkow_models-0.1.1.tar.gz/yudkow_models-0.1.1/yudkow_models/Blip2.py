from transformers import Blip2Processor, Blip2ForConditionalGeneration


class Blip2:
    def __init__(self, model="Salesforce/blip2-opt-2.7b"):
        self.processor = Blip2Processor.from_pretrained(model)
        self.model = Blip2ForConditionalGeneration(model)

    def describe(self, image) -> str:
        inputs = self.processor(images=image, return_tensors="pt")
        outputs = self.model.generate(**inputs)
        description = self.processor.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return description