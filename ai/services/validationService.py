from data.model.databaseModels import Book
class ValidationService:
    @staticmethod
    def validate_Book_extraction(data:dict)->Book:
        return Book(**data)
    
    pass