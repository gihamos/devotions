import json
from utils.logger import logger
from utils.fonction import preview_edges,strip_markdown_json
import uuid

class JSONService:
    @staticmethod
    def safe_parse(text) -> dict:
        try:
            return json.loads(strip_markdown_json(text))

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
       
    @staticmethod
    def generate_id():
        return str(uuid.uuid4())

    @staticmethod
    def normalize_node(node, parent=None, index=0, path_prefix=""):
        """
    Normalise un BookNode :
    - id
    - parentId
    - order
    - level
    - path
    - wordCount
    - récursion sur children
    """

    # ID
        if not node.get("id"):
            node["id"] = JSONService.generate_id()

    # Parent
        node["parentId"] = parent["id"] if parent else None

    # Order
        node["order"] = index + 1

    # Level
        if parent is None:
            node["level"] = 1
        else:
            node["level"] = parent["level"] + 1

    # Path
        node["path"] = f"{path_prefix}{node['order']}"

    # Word count
        text = node.get("clean") or node.get("original") or ""
        node["wordCount"] = len(text.split()) if text else 0

    # Children
        children = node.get("children", [])
        for i, child in enumerate(children):
            JSONService.normalize_node(child, node, i, node["path"] + ".")

        return node

    @staticmethod
    def merge_and_normalize_book(chunk_results: list[dict]) -> dict:
        """
    Fusionne plusieurs chunks (si plusieurs) et normalise le livre complet.
    Si un seul chunk → normalisation simple.
    """
         
    # Cas simple : un seul chunk
        if len(chunk_results) == 1:
            book = chunk_results[0]
            book.get("id")=JSONService.generate_id()
            for i, child in enumerate(book.get("children", [])):
                JSONService.normalize_node(child, None, i)
            return book

        # Cas multi-chunks : fusion simple (concaténation des chapters)
        merged = chunk_results[0]
        merged.get("id")=JSONService.generate_id()

        for chunk in chunk_results[1:]:
            if "children" in chunk:
                merged["children"].extend(chunk["children"])

    # Normalisation complète
        for i, child in enumerate(merged.get("children", [])):
            JSONService.normalize_node(child, None, i)

        return merged


