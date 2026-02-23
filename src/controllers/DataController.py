from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import UploadFile
from models import ResponseEnum
import re #for filename sanitization (text handling)
import os


class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.size_scale = 1024 * 1024

    def validate_uploaded_file(self, file: UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseEnum.FILE_TYPE_NOT_ALLOWED.value
        
        if file.size > self.app_settings.FILE_MAX_SIZE_MB * self.size_scale:
            return False, ResponseEnum.FILE_SIZE_EXCEEDS_LIMIT.value
        
        return True, ResponseEnum.FILE_IS_VALID.value
    
    def generate_unique_file_path(self, original_filename: str, project_id: str):
        random_filename = self.generate_random_string()
        project_path = ProjectController().get_project_path(project_id=project_id)
        cleaned_filename = self.get_clean_filename(original_filename=original_filename)
        new_file_path = os.path.join(project_path, random_filename + "_" + cleaned_filename)

        while os.path.exists(new_file_path):
            random_filename = self.generate_random_string()
            new_file_path = os.path.join(project_path, random_filename + "_" + cleaned_filename)

        return new_file_path, random_filename + "_" + cleaned_filename

    def get_clean_filename(self, original_filename: str):
        cleaned_filename = re.sub(r'[^\w.]', '', original_filename.strip())
        cleaned_filename = cleaned_filename.replace(" ", "_")
        return cleaned_filename
    
