"""Main entry point for Optical Character Understanding"""

from mlx_vlm import load, generate


class VLMEngine:
    """Main implementation method for VLMEngine inferencing"""

    model_path = "mlx-community/Phi-3-vision-128k-instruct-4bit"
    model = None
    processor = None
    temp = 0
    top_p = 1

    def __init__(self, model_path: str | None = None, temp=0, top_p=1) -> None:
        if model_path is not None:
            self.model_path = model_path

        model, processor = load(
            self.model_path, processor_config={"trust_remote_code": True}, lazy=True
        )
        self.model = model
        self.processor = processor
        self.temp = temp
        self.top_p = top_p

    def query_on_image(self, prompt: str, image_path: str) -> str:
        """Perform user query on image provided"""
        prompt = self.processor.tokenizer.apply_chat_template(
            [{"role": "user", "content": f"<|image_1|>\n{prompt}"}],
            tokenize=False,
            add_generation_prompt=True,
        )

        output = generate(
            self.model,
            self.processor,
            image_path,
            prompt,
            verbose=True,
        )

        output.replace("<|end|>", "")

        return output
