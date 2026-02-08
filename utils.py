"""
Helper utilities for the Cal.com Integration API.
"""
from typing import Dict, Any
from fastapi import HTTPException


def success_response(data: Dict[str, Any]) -> Dict[str, Any]:
    """Return successful response."""
    return {"success": True, **data}


def error_response(error_msg: str, status_code: int = 400):
    """Raise HTTP exception with error message."""
    raise HTTPException(status_code=status_code, detail=error_msg)
