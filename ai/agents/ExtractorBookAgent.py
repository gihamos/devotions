from ai.agents.baseAgent import BaseAgent
from ai.services.llmService import LLmService
from ai.services.JsonService import JSONService
from ai.services.JsonService import preview_edges
from ai.services.validationService import ValidationService
from utils.fonction import getJsonLLmMessage
class ExtractorBookAgent(BaseAgent):
    def __init__(self, llm: LLmService):
        super().__init__("Bookextractor")
        self.llm = llm
        
    
    def setLLservice(self,llm: LLmService):
        self.llm=llm
        return self
        

    async def run(self, input_data: dict[str,any]) -> dict[str,any]|None:
        system="""
             Tu es un agent d’extraction structurée à partir d'un texte.  
Retourne uniquement un JSON strict selon les modèles Book et BookNode.

DÉFINITION D’UN BOOK :
Un “book” est tout texte long organisé en parties : roman, récit, essai, manuel, article structuré, ou tout document contenant un titre, des chapitres, des sections ou des paragraphes.  
Si cette structure n’existe pas → échec.

MODÈLE Book :
{
  "id": null,
  "title": string|null,
  "description": string|null,
  "language": "fr",
  "releaseDate": null,
  "publicationDate": null,
  "startedAt": null,
  "summary": string|null,
  "keywords": [string],
  "entities": [ { "type": string, "text": string } ],
  "sentiment": float|null,
  "embedding": [],
  "wordCount": int|null,
  "children": [BookNode]
}

MODÈLE BookNode :
{
  "id": null,
  "parentId": null,
  "type": "chapter"|"section"|"paragraph",
  "level": int,
  "order": int,
  "title": string|null,
  "original": string|null,
  "clean": string|null,
  "formatted": string|null,
  "summary": string|null,
  "keywords": [string],
  "entities": [ { "type": string, "text": string } ],
  "sentiment": float|null,
  "embedding": [],
  "wordCount": int|null,
  "path": string|null,
  "meta": {},
  "references": [],
  "children": [BookNode]
}

RÈGLES :
- Aucune invention, aucune interprétation, aucune reformulation.
- Copier strictement le texte source et l’ordre original.
- original = texte brut exact ; clean = version nettoyée ; formatted = version structurée au format html.
- summary = 1 phrase ; keywords = mots-clés ; entities = personnes/lieux/objets ; sentiment = -1 à +1 ; embedding = [].
- Aucun texte hors JSON. Aucun markdown.
- Si info absente → null, "", ou [].

SORTIE :
Succès → { "success": 1, "data": Book }  
Échec → { "success": 0, "data": null }

             """
             
        message="""
Analyse le texte ci-dessous et transforme-le en un livre structuré (Book + BookNode).
Respecte strictement le format JSON défini dans le prompt système.
Ne renvoie que le JSON final.

Si le texte n’est pas un book :
{ "success": 0, "data": null }

        """

        try:
          datas= getJsonLLmMessage(msg_system=system,msg_user=message,text=input_data["text"])
          raws=[]
          for data in datas:
            raw=await self.llm.generate(data)
            
            if raw.get("success")==1:
              parsed = JSONService.safe_parse(raw.get("data"))
              if ValidationService.is_valid_book_json(parsed["data"]):
                raws.append(parsed.get("data"))
          
          
          if len(raws)>0:
            return { "success": 1, 
                     "data": JSONService.merge_and_normalize_book(raws) } 
          return{
            "success":0,
            "error":"le modele n'a pas reussit à extraire le livre"
          }
        except Exception as e: 
            return { "success": 0, 
                    "error": f"Erreur de validation : {str(e)}" ,
                    "raw":preview_edges(text=parsed.get("data")) or "erreur: aucune donnée renvoyé"}
