import httpx
from ai.services.llmService import LLmService
from utils.logger import logger
from utils.fonction import remove_think_blocks

class UniversalLLMService(LLmService):
    def __init__(
        self,
        provider: str = "ollama",
        api_key: str = None,
        base_url: str = "http://localhost:11434",
        model="deepseek-v3.1:671b-cloud"#"deepseek-r1:latest"
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

    async def generate(self,messages: list[dict[str, any]],**kwargs)->dict[str,any]:
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(500.0, connect=60.0)) as client:
                json_message={
                    "model": self.model,
                    "messages":messages,
                    "stream":False
                    }
                json_message.update(kwargs)
                # --- OpenAI / Azure / API OpenAI-like ---
                if self.provider == "openai":
                    response = await client.post(
                        f"{self.base_url}/v1/chat/completions",
                        headers={"Authorization": f"Bearer {self.api_key}"},
                        json=json_message
                    )

                    response.raise_for_status()
                    data = response.json()
                    return {"success":1,
                            "data":remove_think_blocks(data["choices"][0]["message"]["content"])}

                # --- Ollama local ---
                elif self.provider == "ollama":
                    response = await client.post(
                        f"{self.base_url}/api/chat",
                        json=json_message
                    )

                    response.raise_for_status()
                    data = response.json()
                    return  {
                        "success":1,
                        "data":remove_think_blocks(data["message"]["content"])}

                else:
                    logger.error("Provider incorrect : %s", self.provider)
                    raise ValueError("Provider non supporté")

        except httpx.ConnectError:
            logger.exception("Impossible de se connecter au serveur LLM (%s)", self.base_url)
            return {"success":0,
                    "error": "Connexion impossible au serveur LLM"
                    }

        except httpx.HTTPStatusError as e:
            logger.exception("Erreur HTTP du LLM : %s", e)
            return {"success":0,
                    "error": f"Erreur HTTP du LLM : {e.response.text}"}

        except ValueError as e:
            logger.exception("Erreur de parsing JSON : %s", e)
            return {"success":0,
                    "error": "Réponse du modèle invalide (JSON non valide)"}
        except httpx.ReadTimeout:
            logger.exception("delais d'attente de lecture dépassé")
            return {"success":0,
                      "error": "delai  d'attente de reception de donnée dépassé"}

        except Exception as e:
            logger.exception("Erreur inattendue dans UniversalLLMService")
            return {"success":0,
                    "error": f"Erreur interne : {str(e)}"}
        
   
   