from transformers import Blip2Processor, Blip2ForConditionalGeneration, BitsAndBytesConfig


class Blip2:
    def __init__(self, model="Salesforce/blip2-opt-2.7b"):
        quantization_config = BitsAndBytesConfig()
        self.processor = Blip2Processor.from_pretrained(model,
                        revision="51572668da0eb669e01a189dc22abe6088589a24")
        self.model = Blip2ForConditionalGeneration.from_pretrained(model,
                        quantization_config=quantization_config,
                        revision="51572668da0eb669e01a189dc22abe6088589a24",
                        device_map="auto")
        self.processor.padding_side = "left"
    def describe(self, image) -> str:
        inputs = self.processor(images=image, return_tensors="pt")
        outputs = self.model.generate(**inputs, max_new_tokens=30)
        description = self.processor.tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
        return description