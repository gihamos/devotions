class LLmService:
    
    def __init__(self,model:str):
        self.model=model
        pass
    
    def setModel(self,model:str):
        self.model=model
        return self
    async def generate(self, messages: list[dict[str, any]],**kwargs)->dict[str,any]:
        """
        `messages` doit être une liste de messages pour le LLM.
        Chaque message contient :
          - role : \"system\", \"user\" ou \"assistant\"
          - content : le texte associé à ce rôle

        `Exemple :`
        [
          {"role": "system", "content": "Règles et rôle du modèle"},
          {"role": "user", "content": "Voici le chunk 1"},
          {"role": "user", "content": "Voici le chunk 2"},
          {"role": "user", "content": "Génère maintenant le JSON final"}
        ]
        
        `**kwargs` : paramètres optionnels (ex: temperature=0.2,stream=True)
        """
        raise NotImplementedError("ce service ne peut etre implementer")

