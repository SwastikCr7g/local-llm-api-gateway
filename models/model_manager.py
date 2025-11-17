import ollama

class ModelManager:
    def __init__(self, models):
        """
        Initialize with a list of model names.
        """
        self.models = models

    def get_model(self, name):
        """
        Checks if model is available.
        If not found, raises Exception.
        """
        if name not in self.models:
            raise Exception(f"Model '{name}' not found in configuration.")
        return name  # Just return name for use in ollama.generate()
    
    def generate(self, model_name, prompt):
        """
        Calls ollama.generate for the given model and prompt.
        """
        return ollama.generate(model=model_name, prompt=prompt)["response"]
