from fastapi import APIRouter, FastAPI, Depends, UploadFile, status
from fastapi.responses import JSONResponse
import os
from helpers.config import get_settings, settings
from controllers import DataController, ProjectController
import aiofiles
from models import ResponseEnum
import logging


logger = logging.getLogger("uvicorn.error") #the coming error details will be available for the developers only

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1_data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile, app_settings: settings = Depends(get_settings)):
    
    is_valid, message = DataController().validate_uploaded_file(file=file)
    #return {"is_valid": is_valid, "message": message}

    if not is_valid:
        return (
            JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": message}
            )
        )
    
    project_dir_path = ProjectController().get_project_path(project_id=project_id)
    file_path,file_id= DataController().generate_unique_file_path(original_filename=file.filename, project_id=project_id)

    try:
        async with aiofiles.open(file_path, 'wb') as f:
            while chunk:= await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)

    except Exception as e:

        logger.error(f"Error while uploading file: {e}")

        return (
            JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"message": ResponseEnum.FILE_UPLOADING_FAILED.value}
            )
        )

    return (
            JSONResponse(
                content={
                    "signal" : ResponseEnum.FILE_UPLOADED_SUCCESSFULLY.value,
                    "file_path": file_path,
                    "file_id": file_id
                }
            )
    )