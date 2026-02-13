"""
Helper utilities for the Cal.com Integration API.
"""
from typing import Dict, Any, Union, Optional
from fastapi import HTTPException


def success_response(data: Dict[str, Any]) -> Dict[str, Any]:
    """Return successful response."""
    return {"success": True, **data}


def error_response(error_msg: str, status_code: int = 400):
    """Raise HTTP exception with error message."""
    raise HTTPException(status_code=status_code, detail=error_msg)


def to_int(value: Union[int, str, None], field_name: str = "field") -> Optional[int]:
    """
    Convert a value to integer, accepting both int and str inputs.
    
    Args:
        value: The value to convert (can be int, str, or None)
        field_name: Name of the field for error messages
    
    Returns:
        Integer value or None if input is None
        
    Raises:
        ValueError: If the string cannot be converted to integer
    """
    if value is None:
        return None
    
    if isinstance(value, int):
        return value
    
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            raise ValueError(f"{field_name} must be a valid integer, got '{value}'")
