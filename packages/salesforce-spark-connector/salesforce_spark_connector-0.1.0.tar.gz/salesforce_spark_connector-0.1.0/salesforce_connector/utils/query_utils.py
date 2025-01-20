import re
from typing import List, Tuple, Any, Union
from datetime import datetime

def parse_salesforce_datetime(dt_str: str) -> datetime:
    """Parse Salesforce datetime string to Python datetime."""
    # Remove the timezone offset and 'Z' if present
    dt_str = re.sub(r'[+-]\d{4}$', 'Z', dt_str)
    try:
        return datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S.%f%z')
    except ValueError:
        # Try without milliseconds
        return datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S%z')

def create_partition_ranges(
    field_type: str,
    min_val: Any,
    max_val: Any,
    num_partitions: int
) -> List[Tuple[str, str]]:
    """
    Create partition ranges based on field type.
    
    Args:
        field_type: Type of the field ('datetime', 'number', 'id', or 'string')
        min_val: Minimum value in the range
        max_val: Maximum value in the range
        num_partitions: Number of partitions to create
        
    Returns:
        List of tuples containing (start_range, end_range) as strings
        
    Raises:
        ValueError: If range creation fails for the given field type
    """
    if not min_val or not max_val:
        return []

    try:
        if field_type == 'datetime':
            min_date = parse_salesforce_datetime(min_val)
            max_date = parse_salesforce_datetime(max_val)
            delta = (max_date - min_date) / num_partitions
            
            ranges = []
            for i in range(num_partitions):
                start_date = min_date + (delta * i)
                end_date = min_date + (delta * (i + 1))
                start_str = start_date.strftime('%Y-%m-%dT%H:%M:%S.000Z')
                end_str = end_date.strftime('%Y-%m-%dT%H:%M:%S.000Z')
                ranges.append((start_str, end_str))
            return ranges
                
        elif field_type == 'number':
            min_num = float(min_val)
            max_num = float(max_val)
            step = (max_num - min_num) / num_partitions
            return [
                (str(min_num + (step * i)), str(min_num + (step * (i + 1))))
                for i in range(num_partitions)
            ]
                
        elif field_type == 'id':
            # For Salesforce IDs, use the actual min and max IDs from the query
            id_length = len(min_val)  # Usually 15 or 18 characters
            # Create ranges based on the actual IDs
            min_int = int(min_val, 36)
            max_int = int(max_val, 36)
            step = (max_int - min_int) // num_partitions
            
            ranges = []
            for i in range(num_partitions):
                start_id = min_int + (step * i)
                end_id = min_int + (step * (i + 1))
                # Convert back to base-36 and pad with zeros
                start_str = format(start_id, '036x')[-id_length:]
                end_str = format(end_id, '036x')[-id_length:]
                ranges.append((start_str, end_str))
            return ranges
                
        else:  # string type
            # For non-ID string fields
            chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
            step = len(chars) // num_partitions
            ranges = []
            for i in range(0, len(chars), step):
                start_char = chars[i]
                end_char = chars[min(i + step, len(chars) - 1)]
                ranges.append((start_char, end_char))
            return ranges

    except Exception as e:
        raise ValueError(f"Failed to create ranges for {field_type}: {str(e)}")

def get_object_name(query: str) -> str:
    """
    Extract object name from SOQL query.
    
    Args:
        query: SOQL query string
        
    Returns:
        Name of the Salesforce object
        
    Raises:
        ValueError: If object name cannot be determined from query
    """
    match = re.search(r'FROM\s+(\w+)', query, re.IGNORECASE)
    if not match:
        raise ValueError("Could not determine object name from query")
    return match.group(1)

def get_sobject(sf: Any, object_name: str) -> Any:
    """
    Get SObject from Salesforce connection.
    
    Args:
        sf: Salesforce connection object
        object_name: Name of the Salesforce object
        
    Returns:
        Salesforce object instance
    """
    return getattr(sf, object_name) 