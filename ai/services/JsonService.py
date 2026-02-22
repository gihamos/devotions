import json
from utils.logger import logger
from utils.fonction import preview_edges

class JSONService:
    @staticmethod
    def safe_parse(text: str) -> dict:
        try:
            return json.loads(text)

        except json.JSONDecodeError as e:
            logger.error(f"JSON invalide renvoyé par le modèle : {e}")
            return {
                "success": 0,
                "error": "Le modèle n'a pas renvoyé un JSON valide",
                "raw": preview_edges(text=text)
            }

        except Exception as e:
            logger.exception("Erreur inattendue dans safe_parse()")
            return {
                "success": 0,
                "error": f"Erreur interne : {str(e)}",
                "raw":preview_edges(text=text)
            }

