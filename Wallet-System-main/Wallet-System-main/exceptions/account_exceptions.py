class AccountNotFound(Exception):
    def __init__(self, message = "Account Not Found"):
        super().__init__(message)
        
