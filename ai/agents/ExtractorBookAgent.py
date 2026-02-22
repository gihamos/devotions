from ai.agents.baseAgent import BaseAgent
from ai.services.llmService import LLmService
from ai.services.JsonService import JSONService
from ai.services.JsonService import preview_edges
from ai.services.validationService import ValidationService
class ExtractorBookAgent(BaseAgent):
    def __init__(self, llm: LLmService):
        super().__init__("Bookextractor")
        self.llm = llm
        
    
    def setLLservice(self,llm: LLmService):
        self.llm=llm
        return self
        

    async def run(self, input_data: dict[str,any]) -> dict[str,any]|None:
        system = """
            Tu es un agent spécialisé dans l’extraction structurée de livres, documents et chapitres.
Ta mission est de transformer un texte brut en un JSON strict respectant exactement les modèles suivants :

    ======= Modèle Book ===========
- id (string | null)
- title (string | null)
- description (string | null)
- language (string, ex: "fr")
- releaseDate (datetime | null)
- publicationDate (datetime | null)
- startedAt (datetime | null)
- children (liste de BookNode)

========== Modèle BookNode ===============
- id (string | null)
- type (string | null) → ex: "chapter", "section", "paragraph"
- level (int | null)
- title (string | null)
- lines (liste de Line)
- formattedContent (string | null)
- originalContent (string | null)
- content (string | null)
- meta (dict)
- references (liste)
- children (liste de BookNode)

=== Modèle Line ===
- id (string | null)
- richText (RichText)

=== Modèle RichText ===
- fragments (liste de TextFragment)

=== Modèle TextFragment ===
- id (string | null)
- text (string | null)
- format (liste de string) → ex: ["bold"], ["italic"], ["underline"]

==========================================================
RÈGLES D’EXTRACTION
==========================================================

1. Tu dois TOUJOURS retourner un JSON strict.
2. Tu ne dois JAMAIS ajouter d’explications, commentaires ou texte hors JSON.
3. Tu dois détecter automatiquement :
   - le titre du livre
   - les chapitres
   - les sections
   - les paragraphes
   - les lignes
4. Chaque nœud doit être correctement hiérarchisé via "children".
5. Chaque paragraphe doit être découpé en lignes, et chaque ligne en fragments.
6. Les fragments doivent contenir :
   - text
   - format (si applicable)
7. Si une information n’existe pas, mets null ou une liste vide.
8. Tu dois préserver le texte original dans "originalContent".
9. Tu dois générer des IDs uniques si absents.
10. Tu dois renvoyer EXACTEMENT l’un des deux formats suivants :

=== En cas de succès ===
{
  "success": 1,
  "data": { ...book... }
}

=== En cas d’échec ===
{
  "success": 0,
  "data": null
}

==========================================================
STRUCTURE FINALE OBLIGATOIRE
==========================================================

Tu dois renvoyer UNIQUEMENT :

{
  "success": 1,
  "data": {
    "id": "...",
    "title": "...",
    "description": "...",
    "language": "fr",
    "releaseDate": null,
    "publicationDate": null,
    "startedAt": null,
    "children": [
      {
        "id": "...",
        "type": "chapter",
        "level": 1,
        "title": "...",
        "lines": [],
        "formattedContent": "...",
        "originalContent": "...",
        "content": "...",
        "meta": {},
        "references": [],
        "children": [...]
      }
    ]
  }
}

        """

        message = """
                     Voici le texte que tu dois transformer en un livre structuré selon le modèle Book et BookNode.

Ta mission :
- analyser le texte ci-dessous
- détecter automatiquement le titre, les chapitres, les sections, les paragraphes
- découper le contenu en nodes, lignes et fragments
- respecter strictement la structure JSON définie dans le prompt système
- renvoyer uniquement le JSON final dans le format :
  {
    "success": 1,
    "data": { ...book... }
  }

Si le texte est vide ou inexploitable :
  {
    "success": 0,
    "data": null
  }

==========================
TEXTE À EXTRAIRE :
""" + f"""{input_data["text"]}

==========================
        
                  """

        raw = await self.llm.generate(system, message)
        parsed = JSONService.safe_parse(raw)
        
        if parsed.get("success") == 0:
            return parsed
        try: 
            validated = ValidationService.validate_Book_extraction(parsed["data"]) 
            return { "success": 1, 
                    "data": validated.model_dump() } 
        except Exception as e: 
            return { "success": 0, 
                    "error": f"Erreur de validation : {str(e)}" ,
                    "raw":preview_edges(text=parsed["data"]) or "erreur: aucune donnée renvoyé"}
