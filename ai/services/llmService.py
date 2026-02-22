class LLmService:
    
    def __init__(self,model:str):
        self.model=model
        pass
    
    def setModel(self,model:str):
        self.model=model
        return self
    
    async def generate(self, system: str, message: str):
        """_summary_

        Args:
            system (str): definie le role du systeme \n ex: "tu est un agent traducteur du français et de l'anglais "
            message (str): represente la demande à effectuer ex: traduit mangé en anglais
            model (str): respresente le model à utlisé ex : "llama2"

        """
        raise NotImplementedError("ce service ne peut etre implementer")