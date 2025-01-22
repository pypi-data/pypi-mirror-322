from transformers import Blip2Processor, Blip2ForConditionalGeneration, BitsAndBytesConfig
import logging, warnings
import torch

warnings.filterwarnings("ignore", category=FutureWarning, message=".*clean_up_tokenization_spaces.*")
warnings.filterwarnings("ignore")
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("transformers").propagate = False

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
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def describe(self, image) -> str:
        inputs = self.processor(images=image, return_tensors="pt").to(self.device)
        outputs = self.model.generate(**inputs, max_new_tokens=30)
        description = self.processor.batch_decode(outputs, skip_special_tokens=True)[0].strip()
        return description