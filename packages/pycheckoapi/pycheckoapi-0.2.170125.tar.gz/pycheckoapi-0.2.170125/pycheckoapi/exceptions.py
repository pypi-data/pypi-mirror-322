class MessageException(Exception):
    def __init__(self, *args,msg):
        self.msg = msg

    def __str__(self):
        return self.msg
    