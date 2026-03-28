import bcrypt

class PasswordManager:
    """Interface for hashing & verifying passwords"""
    
    def hash(self, password: str) -> str:
        """Hash the password"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()
    
    def verify(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode())