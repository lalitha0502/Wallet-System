class UserNotFound(Exception):
    def __init__(self, message: str= "User Not Found"):
        super().__init__(message)
        
class UsernameAlreadyExists(Exception):
    def __init__(self, message: str= "Username Already Exists"):
        super().__init__(message)
        
class EmailAlreadyExists(Exception):
    def __init__(self, message: str= "Email Already Exists"):
        super().__init__(message)