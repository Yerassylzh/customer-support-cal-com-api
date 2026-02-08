"""
Configuration management for Cal.com Integration API.
"""
import os
from typing import Dict

# Load environment variables
CALCOM_API_KEY = os.getenv("CALCOM_API_KEY")
if not CALCOM_API_KEY:
    raise ValueError("CALCOM_API_KEY environment variable is required")

# API Configuration
API_VERSION = "2024-09-04"
BASE_URL = "https://api.cal.com/v2"
CLINIC_TIMEZONE = "Asia/Almaty"


def get_headers() -> Dict[str, str]:
    """Get headers for Cal.com API requests."""
    return {
        "Authorization": f"Bearer {CALCOM_API_KEY}",
        "cal-api-version": API_VERSION,
        "Content-Type": "application/json",
    }
