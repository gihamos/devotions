from typing import Optional, Dict, Any, List

class ValidationService:

    @staticmethod
    def is_valid_book_json(data: dict) -> bool:
        """
        Vérifie si le JSON correspond à un livre structuré valide.
        Conditions :
        - data["children"] doit exister et être une liste non vide
        - au moins un BookNode doit contenir du texte réel :
            - original
            - clean
            - formatted
        """

        # Vérifie la présence des enfants
        children = data.get("children")
        if not isinstance(children, list) or len(children) == 0:
            return False

        # Vérifie qu'au moins un node contient du contenu réel
        def has_real_content(nodes: List[Dict[str, Any]]) -> bool:
            for node in nodes:
                if not isinstance(node, dict):
                    continue

                # Nouveau modèle : original / clean / formatted
                if (
                    node.get("original") not in (None, "", []) or
                    node.get("clean") not in (None, "", []) or
                    node.get("formatted") not in (None, "", [])
                ):
                    return True

                # Vérifie récursivement les enfants
                if has_real_content(node.get("children", [])):
                    return True

            return False

        return has_real_content(children)
