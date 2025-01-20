
class RateLimit(Exception):
    """Exception raised for rate limiting errors"""
    def __init__(self, message="Rate Limited - Try again in 20 seconds"):
        self.message = message
        super().__init__(self.message)

class InvalidDFSBook(Exception):
    """Exception raised for invalid DFS Book"""
    def __init__(self, message="Invalid DFS Book - Must be either 'underdog' or 'prizepick'"):
        self.message = message
        super().__init__(self.message)