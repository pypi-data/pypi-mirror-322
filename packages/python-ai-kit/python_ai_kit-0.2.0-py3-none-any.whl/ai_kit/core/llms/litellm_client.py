from litellm import models_by_provider, completion

class LitellmClient:
    def __init__(self, model: str):
        self.model = model

    @property
    def models(self) -> dict:
        return models_by_provider

    @staticmethod
    def print_models(self):
        for provider, models in self.models.items():
            print(provider)
            for model in models:
                print(model)

    async def completion(self, *args, **kwargs):
        return completion(model=self.model, *args, **kwargs)
        
