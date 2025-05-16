import logging
import os
from pathlib import Path
from typing import List, Optional, Tuple

logger = logging.getLogger(__name__)

KNOWLEDGE_BASE_DIR = Path("knowledge")

class SchemaService:
    """Service for managing database schemas as DDL files."""

    def __init__(self):
        KNOWLEDGE_BASE_DIR.mkdir(parents=True, exist_ok=True)

    def get_ddl_file_path(self, schema_name: str) -> Path:
        """Get the full path to a DDL file."""
        if not schema_name.endswith(".sql"):
            schema_name += ".sql"
        return KNOWLEDGE_BASE_DIR / schema_name

    def save_schema_ddl(
        self,
        schema_name: str,
        ddl_content: str,
        overwrite: bool = False
    ) -> Tuple[bool, str]:
        """Save DDL content to a .sql file.

        Args:
            schema_name: The name of the schema (will be used as filename).
            ddl_content: The DDL content as a string.
            overwrite: If True, overwrite the file if it exists.

        Returns:
            A tuple (success: bool, message: str).
        """
        file_path = self.get_ddl_file_path(schema_name)

        if not overwrite and file_path.exists():
            message = f"Schema '{schema_name}' already exists. Set overwrite=True to replace."
            logger.warning(message)
            return False, message

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(ddl_content)
            message = f"Schema '{schema_name}' saved successfully to {file_path}."
            logger.info(message)
            return True, message
        except IOError as e:
            message = f"Error saving schema '{schema_name}' to {file_path}: {e}"
            logger.error(message, exc_info=True)
            return False, message

    def get_schema_ddl(self, schema_name: str) -> Tuple[Optional[str], str]:
        """Retrieve DDL content from a .sql file.

        Args:
            schema_name: The name of the schema file.

        Returns:
            A tuple (ddl_content: Optional[str], message: str).
        """
        file_path = self.get_ddl_file_path(schema_name)

        if not file_path.exists():
            message = f"Schema '{schema_name}' not found at {file_path}."
            logger.warning(message)
            return None, message

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                ddl_content = f.read()
            message = f"Schema '{schema_name}' retrieved successfully from {file_path}."
            logger.info(message)
            return ddl_content, message
        except IOError as e:
            message = f"Error retrieving schema '{schema_name}' from {file_path}: {e}"
            logger.error(message, exc_info=True)
            return None, message

    def list_schema_names(self) -> Tuple[List[str], str]:
        """List available .sql schema files in the knowledge directory.

        Returns:
            A tuple (schema_names: List[str], message: str).
        """
        try:
            schema_files = [f.name for f in KNOWLEDGE_BASE_DIR.glob("*.sql") if f.is_file()]
            message = f"Found {len(schema_files)} schema files."
            logger.info(message)
            return schema_files, message
        except Exception as e:
            message = f"Error listing schema files: {e}"
            logger.error(message, exc_info=True)
            return [], message

    def delete_schema_ddl(self, schema_name: str) -> Tuple[bool, str]:
        """Delete a DDL schema file.

        Args:
            schema_name: The name of the schema file to delete.

        Returns:
            A tuple (success: bool, message: str).
        """
        file_path = self.get_ddl_file_path(schema_name)

        if not file_path.exists():
            message = f"Schema '{schema_name}' not found at {file_path}. Cannot delete."
            logger.warning(message)
            return False, message

        try:
            os.remove(file_path)
            message = f"Schema '{schema_name}' deleted successfully from {file_path}."
            logger.info(message)
            return True, message
        except OSError as e:
            message = f"Error deleting schema '{schema_name}' from {file_path}: {e}"
            logger.error(message, exc_info=True)
            return False, message

# Create a singleton instance
schema_service = SchemaService()
