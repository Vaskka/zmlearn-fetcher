class TypeNotSupportError(RuntimeError):

    def __init__(self, *arg, **kwargs):
        super(TypeNotSupportError, self).__init__(arg, kwargs)
        pass

    pass
