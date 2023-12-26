class ContextManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ContextManager, cls).__new__(cls)
            cls._instance.context = {'lineno': 0}
        return cls._instance

    def set_lineno(self, lineno):
        self.context['lineno'] = lineno

    def get_lineno(self):
        return self.context['lineno']
