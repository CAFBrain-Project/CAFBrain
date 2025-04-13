import os
import torch
from transformers import AutoProcessor, AutoModelForImageTextToText


class OCR:
    def __init__(self, repo_id = "stepfun-ai/GOT-OCR-2.0-hf", model_dir = "agent/models/weights/ocr"):
        model_path = os.path.join(model_dir, "model")
        processor_path = os.path.join(model_dir, "processor")
        
        if not os.path.exists(model_dir):
            processor = AutoProcessor.from_pretrained(repo_id, use_fast = True)
            model = AutoModelForImageTextToText.from_pretrained(repo_id)

            processor.save_pretrained(processor_path)
            model.save_pretrained(model_path)
            
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.processor = AutoProcessor.from_pretrained(processor_path, use_fast = True)
        self.model = AutoModelForImageTextToText.from_pretrained(model_path, device_map = self.device)
        

    def forward(self, image_path):
        inputs = self.processor(image_path, return_tensors = "pt").to(self.device)

        generate_ids = self.model.generate(
            **inputs,
            do_sample = False,
            tokenizer = self.processor.tokenizer,
            stop_strings="<|im_end|>",
            max_new_tokens = 4096,
        )

        decoded_text = self.processor.decode(generate_ids[0, inputs["input_ids"].shape[1]:], skip_special_tokens = True)

        return decoded_text
