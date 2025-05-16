from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional, Any, Union
from enum import Enum

class ColumnType(str, Enum):
    """Supported column types for the schema."""
    STRING = "STRING"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    NUMERIC = "NUMERIC"
    BOOLEAN = "BOOLEAN"
    TIMESTAMP = "TIMESTAMP"
    DATE = "DATE"
    TIME = "TIME"
    DATETIME = "DATETIME"
    RECORD = "RECORD"  # For nested/repeated fields

class RelationshipType(str, Enum):
    """Types of relationships between tables."""
    ONE_TO_ONE = "one-to-one"
    ONE_TO_MANY = "one-to-many"
    MANY_TO_MANY = "many-to-many"

class ColumnSchema(BaseModel):
    """Schema for a single column in a table."""
    name: str = Field(..., description="Name of the column")
    type: Union[ColumnType, str] = Field(..., description="Data type of the column")
    description: Optional[str] = Field(None, description="Description of the column")
    is_nullable: bool = Field(True, description="Whether the column can be NULL")
    is_primary_key: bool = Field(False, description="Whether the column is part of the primary key")
    is_required: bool = Field(False, description="Whether the column is required (not null)")
    default_value: Optional[Any] = Field(None, description="Default value for the column")
    max_length: Optional[int] = Field(None, description="Maximum length for string types")
    precision: Optional[int] = Field(None, description="Precision for numeric types")
    scale: Optional[int] = Field(None, description="Scale for numeric types")
    sample_data: Optional[List[Any]] = Field(None, description="Sample data for the column")
    
    @validator('type')
    def validate_column_type(cls, v):
        """Validate that the column type is one of the supported types."""
        if isinstance(v, str):
            v = v.upper()
            try:
                return ColumnType(v)
            except ValueError:
                # If it's not a standard type, allow it as a string
                return v
        return v

class TableSchema(BaseModel):
    """Schema for a single table in the database."""
    name: str = Field(..., description="Name of the table")
    description: Optional[str] = Field(None, description="Description of the table")
    columns: Dict[str, ColumnSchema] = Field(default_factory=dict, description="Dictionary of columns in the table")
    primary_key: List[str] = Field(default_factory=list, description="List of column names that form the primary key")
    sample_queries: List[str] = Field(default_factory=list, description="Example queries that use this table")
    row_count: Optional[int] = Field(None, description="Approximate number of rows in the table")
    last_updated: Optional[str] = Field(None, description="Timestamp when the table was last updated")
    
    @validator('primary_key')
    def validate_primary_key(cls, v, values):
        """Validate that primary key columns exist in the table."""
        if 'columns' in values:
            for col in v:
                if col not in values['columns']:
                    raise ValueError(f"Primary key column '{col}' not found in table columns")
        return v

class RelationshipSchema(BaseModel):
    """Schema for relationships between tables."""
    name: str = Field(..., description="Name of the relationship")
    type: RelationshipType = Field(..., description="Type of relationship")
    source_table: str = Field(..., description="Name of the source table")
    source_columns: List[str] = Field(..., description="Columns in the source table that form the relationship")
    target_table: str = Field(..., description="Name of the target table")
    target_columns: List[str] = Field(..., description="Columns in the target table that form the relationship")
    description: Optional[str] = Field(None, description="Description of the relationship")
    
    @validator('source_columns', 'target_columns')
    def validate_columns_non_empty(cls, v):
        """Validate that columns lists are not empty."""
        if not v:
            raise ValueError("At least one column must be specified")
        return v

class DatabaseSchema(BaseModel):
    """Complete database schema."""
    tables: Dict[str, TableSchema] = Field(
        default_factory=dict, 
        description="Dictionary of table schemas keyed by table name"
    )
    relationships: List[RelationshipSchema] = Field(
        default_factory=list, 
        description="List of relationships between tables"
    )
    description: Optional[str] = Field(None, description="Description of the database schema")
    version: str = Field("1.0.0", description="Version of the schema")
    created_at: Optional[str] = Field(None, description="Timestamp when the schema was created")
    updated_at: Optional[str] = Field(None, description="Timestamp when the schema was last updated")
