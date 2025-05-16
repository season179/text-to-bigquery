from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime

from app.models import DatabaseSchema, TableSchema, ColumnSchema, RelationshipSchema
from app.services.schema_service import schema_service

router = APIRouter()
logger = logging.getLogger(__name__)

class SchemaUpdateRequest(BaseModel):
    """Request model for updating the database schema."""
    schema_data: DatabaseSchema = Field(..., description="The complete database schema to store")

@router.put(
    "/{schema_name}",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload or Update a DDL Schema File",
    description="Uploads or updates a DDL schema file in the knowledge base. The schema name should not include '.sql'."
)
async def upload_or_update_schema_ddl(
    schema_name: str = FastApiPath(
        ..., 
        description="The name of the schema (e.g., 'my_database_schema'). Extension '.sql' will be added automatically.",
        min_length=1
    ),
    ddl_content: str = Body(
        ..., 
        media_type="text/plain",
        description="The DDL content for the schema as a plain string."
    ),
    overwrite: bool = Query(
        False, 
        description="If true, overwrite the schema file if it already exists."
    )
):
    """
    Saves or updates a DDL schema file.
    - **schema_name**: Name of the schema file (without .sql extension).
    - **ddl_content**: The DDL (Data Definition Language) string.
    - **overwrite**: Boolean to allow overwriting an existing file.
    """
    logger.info(f"Request to save DDL for schema: '{schema_name}'. Overwrite: {overwrite}")
    
    success, message = schema_service.save_schema_ddl(schema_name, ddl_content, overwrite)
    
    if success:
        logger.info(f"DDL for schema '{schema_name}' saved successfully: {message}")
        return MessageResponse(message=message)
    else:
        logger.error(f"Failed to save DDL for schema '{schema_name}': {message}")
        # Determine appropriate status code based on message
        if "already exists" in message:
            status_code = status.HTTP_409_CONFLICT
        else:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(status_code=status_code, detail=message)

@router.get(
    "/{schema_name}", 
    response_class=PlainTextResponse,
    status_code=status.HTTP_200_OK,
    summary="Get DDL Schema Content",
    description="Retrieve the DDL content of a specific schema file.",
    responses={
        200: {"content": {"text/plain": {"example": "CREATE TABLE users (id INT, name VARCHAR(255));"}}},
        404: {"description": "Schema not found", "model": MessageResponse}
    }
)
async def get_schema_ddl_content(
    schema_name: str = FastApiPath(
        ..., 
        description="The name of the schema (e.g., 'my_database_schema'). Extension '.sql' can be omitted.",
        min_length=1
    )
):
    """
    Retrieves the DDL content for a given schema name.
    - **schema_name**: Name of the schema file.
    """
    logger.info(f"Request to get DDL content for schema: '{schema_name}'.")
    
    ddl_content, message = schema_service.get_schema_ddl(schema_name)
    
    if ddl_content is not None:
        logger.info(f"DDL content for schema '{schema_name}' retrieved successfully.")
        return PlainTextResponse(content=ddl_content)
    else:
        logger.warning(f"Schema '{schema_name}' not found: {message}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

@router.get(
    "/", 
    response_model=SchemaListResponse,
    status_code=status.HTTP_200_OK,
    summary="List Available DDL Schema Names",
    description="Retrieve a list of all available DDL schema file names."
)
async def list_available_schemas():
    """
    Lists all .sql files in the knowledge directory.
    """
    logger.info("Request to list available DDL schemas.")
    schema_names, message = schema_service.list_schema_names()
    return SchemaListResponse(schemas=schema_names, message=message)

@router.delete(
    "/{schema_name}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete DDL Schema File",
    description="Delete a specific DDL schema file from the knowledge base.",
    responses={
        404: {"description": "Schema not found", "model": MessageResponse}
    }
)
async def delete_schema_ddl_file(
    schema_name: str = FastApiPath(
        ..., 
        description="The name of the schema file to delete (e.g., 'my_database_schema'). Extension '.sql' can be omitted.",
        min_length=1
    )
):
    """
    Deletes a DDL schema file.
    - **schema_name**: Name of the schema file to delete.
    """
    logger.info(f"Request to delete DDL schema file: '{schema_name}'.")
    
    success, message = schema_service.delete_schema_ddl(schema_name)
    
    if success:
        logger.info(f"DDL schema file '{schema_name}' deleted successfully: {message}")
        return MessageResponse(message=message)
    else:
        logger.error(f"Failed to delete DDL schema file '{schema_name}': {message}")
        if "not found" in message:
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message)
