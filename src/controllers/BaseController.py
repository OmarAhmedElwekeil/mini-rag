from helpers.config import get_settings, settings
import os
import random
import string


class BaseController:
    def __init__(self):
        self.app_settings = get_settings()
        self.BaseDir = os.path.dirname(os.path.dirname(__file__))
        self.files_dir = os.path.join(self.BaseDir, "assets", "files")
    
    def generate_random_string(self, length: int = 12):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))