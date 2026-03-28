class TransactionNotFound(Exception):
    def __init__(self, message: str = "Transaction Not Found"):
        super().__init__(message)
        
class TransactionUnableToChangeState(Exception):
    def __init__(self, message: str = "Not Able to Change state of the Transaction"):
        super().__init__(message)