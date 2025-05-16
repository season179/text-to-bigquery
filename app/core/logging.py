import logging
import sys
import json
from datetime import datetime, timezone
from typing import Any, Dict, Optional
import structlog
from app.core.config import settings

def add_timestamp(_, __, event_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Add timestamp to log entries."""
    event_dict["timestamp"] = datetime.now(timezone.utc).isoformat()
    return event_dict

def configure_logging():
    """Configure structured logging for the application."""
    # Configure the root logger level
    root_logger = logging.getLogger()
    root_logger.setLevel(settings.LOG_LEVEL.upper())
    
    # Remove any existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Configure console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(settings.LOG_LEVEL.upper())
    
    # Configure formatter
    if settings.DEBUG:
        # Pretty print for development
        formatter = structlog.dev.ConsoleRenderer(
            pad_event=30,
            colors=True,
        )
    else:
        # JSON formatter for production
        formatter = structlog.processors.JSONRenderer(
            serializer=lambda x: json.dumps(x, ensure_ascii=False)
        )
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.PositionalArgumentsFormatter(),
            add_timestamp,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Configure the root logger
    handler = logging.StreamHandler()
    handler.setFormatter(
        structlog.stdlib.ProcessorFormatter(
            processor=formatter,
            foreign_pre_chain=[],
        )
    )
    
    root_logger.addHandler(handler)
    
    # Set up logging for uvicorn
    for _log in ["uvicorn", "uvicorn.error"]:
        logging.getLogger(_log).handlers.clear()
        logging.getLogger(_log).propagate = True
    
    # Set the log level for uvicorn loggers
    logging.getLogger("uvicorn").setLevel(settings.LOG_LEVEL.upper())
    logging.getLogger("uvicorn.error").setLevel(settings.LOG_LEVEL.upper())
    logging.getLogger("uvicorn.access").handlers.clear()
    logging.getLogger("uvicorn.access").propagate = True
    
    logger = structlog.get_logger(__name__)
    logger.info("Logging configured", log_level=settings.LOG_LEVEL)
