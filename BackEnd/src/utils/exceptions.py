
class HTTPException(Exception):

    def __init__(self, *args, **kargs):
        self.status = kargs["status"]
        del kargs["status"]
        super().__init__(*args, **kargs)
    

class Conflict(HTTPException):
    pass


class InvalidBody(HTTPException):
    pass
