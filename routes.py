"""
FastAPI route handlers for all endpoints.
"""
from fastapi import APIRouter, Request, HTTPException, Depends
import requests
from typing import Dict, Any, List

from models import (
    CancelAppointmentParams,
    GetAvailableSlotsParams,
    GetUpcomingAppointmentsParams,
    CreateBookingParams,
    GetEventTypesParams
)
from utils import success_response, error_response
from calcom_client import CalComClient
from auth import verify_token

router = APIRouter()
client = CalComClient()


@router.post("/cancel-appointment")
async def cancel_appointment_endpoint(request: Request, authenticated: bool = Depends(verify_token)):
    """Cancel an appointment."""
    try:
        payload = await request.json()
        params = CancelAppointmentParams(**payload)

        data = client.cancel_appointment(
            booking_id=params.booking_id,
            cancellation_reason=params.cancellation_reason
        )

        if data.get("status") != "success":
            error_response("Cancellation failed - API did not return success")

        booking = data.get("data", {})
        return success_response({
            "id": booking.get("id"),
            "uid": booking.get("uid"),
            "status": booking.get("status"),
            "title": booking.get("title"),
            "message": "Appointment successfully cancelled"
        })

    except requests.RequestException as e:
        error_response(f"Cancellation failed: {str(e)}")
    except ValueError as ve:
        error_response(f"Invalid input: {str(ve)}", 422)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/get-available-slots")
async def get_available_slots_endpoint(request: Request, authenticated: bool = Depends(verify_token)):
    """Get available slots for an event type."""
    try:
        payload = await request.json()
        params = GetAvailableSlotsParams(**payload)

        data = client.get_available_slots(
            event_type_id=params.event_type_id,
            start_date=params.start_date,
            end_date=params.end_date,
            time_zone=params.time_zone,
            username=params.username,
            format=params.format,
            duration=params.duration
        )

        if data.get("status") != "success":
            error_response("API returned non-success status")

        slots = data.get("data", {})
        return success_response({
            "slots": slots,
            "total_dates": len(slots)
        })

    except requests.RequestException as e:
        error_response(f"Request failed: {str(e)}")
    except ValueError as ve:
        error_response(f"Invalid input: {str(ve)}", 422)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/get-upcoming-appointments")
async def get_upcoming_appointments_endpoint(request: Request, authenticated: bool = Depends(verify_token)):
    """Get upcoming appointments for a patient."""
    try:
        payload = await request.json()
        params = GetUpcomingAppointmentsParams(**payload)

        data = client.get_upcoming_appointments(
            patient_email=params.patient_email,
            limit=params.limit,
            after=params.after
        )

        if data.get("status") != "success":
            error_response("API returned non-success status")

        bookings_raw = data.get("data", [])
        appointments: List[Dict[str, Any]] = []
        for b in bookings_raw:
            appointments.append({
                "id": b.get("id"),
                "uid": b.get("uid"),
                "title": b.get("title"),
                "start": b.get("start"),
                "end": b.get("end"),
                "status": b.get("status"),
                "eventTypeId": b.get("eventTypeId"),
                "description": b.get("description"),
                "attendees": [
                    {"name": a.get("name"), "email": a.get("email"), "timeZone": a.get("timeZone")}
                    for a in b.get("attendees", [])
                ],
                "createdAt": b.get("createdAt")
            })

        return success_response({
            "appointments": appointments,
            "total_found": len(appointments)
        })

    except requests.RequestException as e:
        error_response(f"Request failed: {str(e)}")
    except ValueError as ve:
        error_response(f"Invalid input: {str(ve)}", 422)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create-booking")
async def create_booking_endpoint(request: Request, authenticated: bool = Depends(verify_token)):
    """Create a new booking."""
    try:
        payload = await request.json()
        params = CreateBookingParams(**payload)

        data = client.create_booking(
            event_type_id=params.event_type_id,
            start=params.start,
            attendee_name=params.attendee_name,
            attendee_email=params.attendee_email,
            additional_notes=params.additional_notes
        )

        if data.get("status") != "success":
            error_response("Booking failed - API did not return success")

        booking = data.get("data", {})
        return success_response({
            "message": "Appointment successfully booked",
            "booking": {
                "uid": booking.get("uid"),
                "id": booking.get("id"),
                "start": booking.get("start"),
                "end": booking.get("end"),
                "title": booking.get("title"),
                "status": booking.get("status"),
                "attendee": {
                    "name": params.attendee_name,
                    "email": params.attendee_email
                }
            }
        })

    except requests.RequestException as e:
        error_response(f"Booking request failed: {str(e)}")
    except ValueError as ve:
        error_response(f"Invalid input: {str(ve)}", 422)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/get-event-types")
async def get_event_types_endpoint(request: Request, authenticated: bool = Depends(verify_token)):
    """Get event types for a team."""
    try:
        payload = await request.json()
        params = GetEventTypesParams(**payload)

        # Use team_id from request parameters
        data = client.get_event_types(team_id=params.team_id)

        event_types = data.get("data") or data.get("event_types") or []
        if not isinstance(event_types, list):
            error_response("Unexpected API response format")

        services = []
        for event in event_types:
            event_id = event.get("id")
            if event_id is None:
                continue
            services.append({
                "id": event_id,
                "lengthInMinutes": event.get("lengthInMinutes"),
                "title": event.get("title", "Unnamed service"),
                "slug": event.get("slug", ""),
                "description": event.get("description", "").strip() or ""
            })

        return success_response({
            "services": services,
            "total": len(services)
        })

    except requests.RequestException as e:
        error_response(f"API request failed: {str(e)}")
    except ValueError as ve:
        error_response(f"Invalid input: {str(ve)}", 422)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query-knowledge-base")
async def query_knowledge_base_endpoint(request: Request, authenticated: bool = Depends(verify_token)):
    """Query the knowledge base - returns content from knowledge_base.md file."""
    import os
    
    try:
        # Read the knowledge base markdown file
        kb_file_path = os.path.join(os.path.dirname(__file__), "knowledge_base.md")
        
        if not os.path.exists(kb_file_path):
            error_response(
                "Knowledge base file not found. Please create 'knowledge_base.md' in the project directory.",
                404
            )
        
        with open(kb_file_path, "r", encoding="utf-8") as f:
            knowledge_content = f.read()
        
        return success_response({
            "content": knowledge_content,
            "source": "knowledge_base.md"
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/clinic-info")
async def get_clinic_info(authenticated: bool = Depends(verify_token)):
    """Get current clinic information including date, time, and timezone."""
    from datetime import datetime
    from config import CLINIC_TIMEZONE
    import pytz
    
    try:
        # Get current time in clinic timezone
        clinic_tz = pytz.timezone(CLINIC_TIMEZONE)
        current_time = datetime.now(clinic_tz)
        
        return success_response({
            "current_datetime": current_time.strftime("%Y-%m-%d %H:%M:%S"),
            "timezone": CLINIC_TIMEZONE,
            "timezone_offset": current_time.strftime("%z"),
            "day_of_week": current_time.strftime("%A"),
            "formatted": current_time.strftime("%A, %B %d, %Y at %I:%M %p %Z")
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok", "version": "1.0.0"}
