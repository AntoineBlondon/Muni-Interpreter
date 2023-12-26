class ContextManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ContextManager, cls).__new__(cls)
            cls._instance.context = {'lineno': None, 'runtime': None}
        return cls._instance

    def set_lineno(self, lineno):
        self.context['lineno'] = lineno

    def get_lineno(self):
        return self.context['lineno']
    
    def set_runtime(self, runtime):
        self.context['runtime'] = runtime

    def get_runtime(self):
        return self.context['runtime']
    
