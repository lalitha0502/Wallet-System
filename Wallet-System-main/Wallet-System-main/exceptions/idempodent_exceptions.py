class IdempotencyConflictException(Exception):
    pass


class IdempotencyAlreadyProcessed(Exception):
    def __init__(self, response: str):
        self.response = response
        super().__init__(self)