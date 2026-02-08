"""
Helper utilities for the Cal.com Integration API.
"""
import json
from typing import Dict, Any, List
from fastapi.responses import JSONResponse


def vapi_response(tool_call_id: str, result: Dict[str, Any]) -> Dict[str, List[Dict[str, str]]]:
    """Format response for Vapi custom tool."""
    return {
        "results": [
            {
                "toolCallId": tool_call_id,
                "result": json.dumps(result)  # Return as JSON string for easy LLM parsing
            }
        ]
    }


def handle_error(tool_call_id: str, error_msg: str, status_code: int = 400) -> JSONResponse:
    """Handle errors uniformly."""
    return JSONResponse(
        vapi_response(tool_call_id, {"success": False, "error": error_msg}),
        status_code=status_code
    )
