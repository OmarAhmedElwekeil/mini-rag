from enum import Enum

class ResponseEnum(Enum):
    FILE_TYPE_NOT_ALLOWED = "File type not allowed"
    FILE_SIZE_EXCEEDS_LIMIT = "File size exceeds limit"
    FILE_IS_VALID = "File is valid"
    FILE_UPLOADING_FAILED = "File uploading failed"
    FILE_UPLOADED_SUCCESSFULLY = "File uploaded successfully"
    FILE_VALIDATED_SUCCESSFULLY = "File validated successfully"