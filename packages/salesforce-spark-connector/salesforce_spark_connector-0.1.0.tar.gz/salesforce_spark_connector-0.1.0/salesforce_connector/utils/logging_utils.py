import logging
import os
from typing import Optional
from datetime import datetime

def setup_logging(log_level: str = 'INFO', 
                 log_file: Optional[str] = None,
                 log_format: Optional[str] = None,
                 set_spark_logging: bool = True) -> logging.Logger:
    """Set up logging configuration.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file. If None, logs only to console
        log_format: Custom log format string. If None, uses default format
        set_spark_logging: Whether to set Spark's log level (default: True)
        
    Returns:
        Logger instance
    """
    # Create logger
    logger = logging.getLogger('ScalableSalesforceConnector')
    
    # Set log level
    level = getattr(logging, log_level.upper(), logging.INFO)
    logger.setLevel(level)
    
    # Set root logger level as well
    logging.getLogger().setLevel(level)
    
    # Default format if none provided
    if not log_format:
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(log_format)
    
    # Clear any existing handlers
    if logger.handlers:
        logger.handlers.clear()
    
    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)
    logger.addHandler(console_handler)
    
    # File Handler (if log_file provided)
    if log_file:
        # Create log directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        # Add timestamp to log filename if not provided
        if not os.path.splitext(log_file)[1]:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            log_file = f"{log_file}_{timestamp}.log"
            
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(level)
        logger.addHandler(file_handler)
    
    # Set Spark logging level if requested
    if set_spark_logging:
        try:
            from pyspark.sql import SparkSession
            if SparkSession._instantiatedSession:
                spark = SparkSession._instantiatedSession
                # Convert Python logging level to Spark logging level
                spark_level = {
                    logging.DEBUG: 'DEBUG',
                    logging.INFO: 'INFO',
                    logging.WARNING: 'WARN',
                    logging.ERROR: 'ERROR',
                    logging.CRITICAL: 'ERROR'
                }.get(level, 'INFO')
                spark.sparkContext.setLogLevel(spark_level)
                logger.debug(f"Set Spark log level to {spark_level}")
        except ImportError:
            logger.debug("PySpark not available, skipping Spark log level setting")
        except Exception as e:
            logger.debug(f"Failed to set Spark log level: {str(e)}")
    
    logger.propagate = False
    return logger 