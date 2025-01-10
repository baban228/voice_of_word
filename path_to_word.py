class Path:
    path_file = ""
    model_path = "vosk-model-ru"

    path_buffer = "auto.txt"
    def __int__(self):
        pass
    def get_path_file(self):
        return self.path_file
    def set_path_file(self, _path_file):
        self.path_file = _path_file

    def get_model_path(self):
        return self.model_path

    def set_model_path(self, _model_path):
        self.model_path = _model_path

    def get_path_buffer(self):
        return self.path_buffer
    def set_path_buffer(self, _path_buffer):
        self.path_buffer = _path_buffer