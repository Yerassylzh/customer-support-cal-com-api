"""
Cal.com API client for handling all API interactions.
"""
import requests
from typing import Dict, Any, Optional, List
from config import BASE_URL, get_headers, CLINIC_TIMEZONE


class CalComClient:
    """Client for interacting with Cal.com API."""
    
    def __init__(self):
        self.base_url = BASE_URL
        self.slots_headers = get_headers(isSlots=True)
        self.default_headers = get_headers(isSlots=False)
    
    def cancel_appointment(
        self, 
        booking_id: str | int, 
        cancellation_reason: str
    ) -> Dict[str, Any]:
        """Cancel a booking."""
        # Determine endpoint based on booking_id type
        if isinstance(booking_id, str) and ("-" in booking_id or any(c.isalpha() for c in booking_id)):
            endpoint = f"{self.base_url}/bookings/{booking_id}/cancel"
        else:
            booking_id_int = int(booking_id)
            endpoint = f"{self.base_url}/bookings/{booking_id_int}/cancel"
        
        body = {"cancellationReason": cancellation_reason}
        response = requests.post(endpoint, headers=self.default_headers, json=body, timeout=12)
        response.raise_for_status()
        return response.json()
    
    def get_available_slots(
        self,
        event_type_id: int,
        start_date: str,
        end_date: str,
        time_zone: Optional[str] = None,
        username: Optional[str] = None,
        format: str = "time",
        duration: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get available slots for an event type."""
        query_params = {
            "eventTypeId": event_type_id,
            "start": start_date,
            "end": end_date,
            "timeZone": time_zone or CLINIC_TIMEZONE,
            "format": format,
        }
        if username:
            query_params["username"] = username
        if duration:
            query_params["duration"] = duration
        
        url = f"{self.base_url}/slots"
        response = requests.get(url, headers=self.slots_headers, params=query_params, timeout=15)
        response.raise_for_status()
        return response.json()
    
    def get_upcoming_appointments(
        self,
        patient_email: str,
        limit: int = 10,
        after: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get upcoming appointments for a patient."""
        query_params = {
            "status": "upcoming",
            "attendeeEmail": patient_email.strip(),
            "take": limit,
            "skip": 0
        }
        if after:
            query_params["afterStart"] = after
        
        response = requests.get(
            f"{self.base_url}/bookings", 
            headers=self.default_headers, 
            params=query_params, 
            timeout=12
        )
        response.raise_for_status()
        return response.json()
    
    def create_booking(
        self,
        event_type_id: int,
        start: str,
        attendee_name: str,
        attendee_email: str,
        additional_notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new booking."""
        body = {
            "eventTypeId": event_type_id,
            "start": start,
            "attendee": {
                "name": attendee_name,
                "email": attendee_email,
                "timeZone": CLINIC_TIMEZONE
            }
        }
        # If you have custom fields for notes, add here (e.g., bookingFieldsResponses)
        
        response = requests.post(
            f"{self.base_url}/bookings", 
            headers=self.default_headers, 
            json=body, 
            timeout=15
        )
        response.raise_for_status()
        return response.json()
    
    def get_event_types(self, team_id: int) -> Dict[str, Any]:
        """Get event types for a specific team."""
        url = f"{self.base_url}/teams/{team_id}/event-types"
        response = requests.get(url, headers=self.default_headers, timeout=10)
        response.raise_for_status()
        return response.json()
