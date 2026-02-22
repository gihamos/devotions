import httpx
from ai.services.llmService import LLmService
from utils.logger import logger

class UniversalLLMService(LLmService):
    def __init__(
        self,
        provider: str = "ollama",
        api_key: str = None,
        base_url: str = "http://localhost:11434",
        model="llama3"
    ):
        """
        Args:
            provider (str): "ollama" ou "openai"
            api_key (str): clé API si provider = openai
            base_url (str): URL du serveur LLM
        """
        super().__init__(model=model)
        self.provider = provider
        self.api_key = api_key
        self.base_url = base_url

    async def generate(self, system: str, message: str):
        try:
            async with httpx.AsyncClient(timeout=30) as client:

                # --- OpenAI / Azure / API OpenAI-like ---
                if self.provider == "openai":
                    response = await client.post(
                        f"{self.base_url}/v1/chat/completions",
                        headers={"Authorization": f"Bearer {self.api_key}"},
                        json={
                            "model": self.model,
                            "messages": [
                                {"role": "system", "content": system},
                                {"role": "user", "content": message}
                            ]
                        }
                    )

                    response.raise_for_status()
                    data = response.json()
                    return data["choices"][0]["message"]["content"]

                # --- Ollama local ---
                elif self.provider == "ollama":
                    response = await client.post(
                        f"{self.base_url}/api/chat",
                        json={
                            "model": model,
                            "messages": [
                                {"role": "system", "content": system},
                                {"role": "user", "content": message}
                            ],
                            "stream": False
                        }
                    )

                    response.raise_for_status()
                    data = response.json()
                    return data["message"]["content"]

                else:
                    logger.error("Provider incorrect : %s", self.provider)
                    raise ValueError("Provider non supporté")

        except httpx.ConnectError:
            logger.error("Impossible de se connecter au serveur LLM (%s)", self.base_url)
            return {"error": "Connexion impossible au serveur LLM"}

        except httpx.HTTPStatusError as e:
            logger.error("Erreur HTTP du LLM : %s", e)
            return {"error": f"Erreur HTTP du LLM : {e.response.text}"}

        except ValueError as e:
            logger.error("Erreur de parsing JSON : %s", e)
            return {"error": "Réponse du modèle invalide (JSON non valide)"}

        except Exception as e:
            logger.exception("Erreur inattendue dans UniversalLLMService")
            return {"error": f"Erreur interne : {str(e)}"}
        
   
   