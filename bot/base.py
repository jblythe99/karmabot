
REGISTERED_CLASSES = {}

class Setup(object):

    def register(self, name):

        def decorator(cls):
            REGISTERED_CLASSES[name] = cls
        return decorator

    def list(self):
        pass

connector = Setup()