import os
import torch
from PIL import Image as PILImage
from transformers import BlipProcessor, BlipForConditionalGeneration

class ImageCaption:
    def __init__(self, repo_id = "Salesforce/blip-image-captioning-large", model_dir = "agent/models/weights/image_caption"):
        model_path = os.path.join(model_dir, "model")
        processor_path = os.path.join(model_dir, "processor")

        if not os.path.exists(model_dir):
            processor = BlipProcessor.from_pretrained(repo_id, use_fast = True)
            model = BlipForConditionalGeneration.from_pretrained(repo_id)

            processor.save_pretrained(processor_path)
            model.save_pretrained(model_path)

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.processor = BlipProcessor.from_pretrained(processor_path, use_fast = True)
        self.model = BlipForConditionalGeneration.from_pretrained(model_path, device_map = self.device)

    def forward(self, image_path, conditional_image_captioning = True):
        raw_image = PILImage.open(image_path).convert('RGB')

        if conditional_image_captioning == True:
            text = "a photography of"
            inputs = self.processor(raw_image, text, return_tensors = "pt").to(self.device)

        else:
            inputs = self.processor(raw_image, return_tensors = "pt").to(self.device)

        out = self.model.generate(**inputs)
        text = self.processor.decode(out[0], skip_special_tokens = True)

        return text
