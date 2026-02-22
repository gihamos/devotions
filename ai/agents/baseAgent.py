class BaseAgent:
    def __init__(self,name:str):
        self.name=name
    
    
    def getName(self)->str:
        self.name
        
        
    async def run(self,input_data: dict[str,any])-> dict[str,any]|None:
        """_summary_

        Args:
            input_data (dict[str,any]): c'est la donnée en entré avec la clé text\nex: {"text" : "[maison, livre]" }

        Raises:
            NotImplementedError: _description_

        Returns:
            dict[str,any]: _description_
        """
        raise NotImplementedError("cet agent ne peut être implementé")

    