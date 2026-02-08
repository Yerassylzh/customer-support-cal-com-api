"""
FastAPI route handlers for all endpoints.
"""
from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
import requests
from typing import Dict, Any, List

from models import (
    VapiRequest,
    CancelAppointmentParams,
    GetAvailableSlotsParams,
    GetUpcomingAppointmentsParams,
    CreateBookingParams,
    GetEventTypesParams
)
from utils import vapi_response, handle_error
from calcom_client import CalComClient
from auth import verify_token

router = APIRouter()
client = CalComClient()


@router.post("/cancel-appointment")
async def cancel_appointment_endpoint(request: Request, authenticated: bool = Depends(verify_token)):
    """Cancel an appointment."""
    try:
        payload = await request.json()
        vapi_req = VapiRequest(**payload)
        params = CancelAppointmentParams(**vapi_req.parameters)

        data = client.cancel_appointment(
            booking_id=params.booking_id,
            cancellation_reason=params.cancellation_reason
        )

        if data.get("status") != "success":
            return handle_error(vapi_req.toolCallId, "Cancellation failed - API did not return success")

        booking = data.get("data", {})
        result = {
            "success": True,
            "id": booking.get("id"),
            "uid": booking.get("uid"),
            "status": booking.get("status"),
            "title": booking.get("title"),
            "message": "Appointment successfully cancelled"
        }
        return vapi_response(vapi_req.toolCallId, result)

    except requests.RequestException as e:
        return handle_error(vapi_req.toolCallId if 'vapi_req' in locals() else "unknown", f"Cancellation failed: {str(e)}")
    except ValueError as ve:
        return handle_error(vapi_req.toolCallId if 'vapi_req' in locals() else "unknown", f"Invalid input: {str(ve)}", 422)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/get-available-slots")
async def get_available_slots_endpoint(request: Request, authenticated: bool = Depends(verify_token)):
    """Get available slots for an event type."""
    try:
        payload = await request.json()
        vapi_req = VapiRequest(**payload)
        params = GetAvailableSlotsParams(**vapi_req.parameters)

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
            return handle_error(vapi_req.toolCallId, "API returned non-success status")

        slots = data.get("data", {})
        result = {
            "success": True,
            "slots": slots,
            "total_dates": len(slots)
        }
        return vapi_response(vapi_req.toolCallId, result)

    except requests.RequestException as e:
        return handle_error(vapi_req.toolCallId if 'vapi_req' in locals() else "unknown", f"Request failed: {str(e)}")
    except ValueError as ve:
        return handle_error(vapi_req.toolCallId if 'vapi_req' in locals() else "unknown", f"Invalid input: {str(ve)}", 422)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/get-upcoming-appointments")
async def get_upcoming_appointments_endpoint(request: Request, authenticated: bool = Depends(verify_token)):
    """Get upcoming appointments for a patient."""
    try:
        payload = await request.json()
        vapi_req = VapiRequest(**payload)
        params = GetUpcomingAppointmentsParams(**vapi_req.parameters)

        data = client.get_upcoming_appointments(
            patient_email=params.patient_email,
            limit=params.limit,
            after=params.after
        )

        if data.get("status") != "success":
            return handle_error(vapi_req.toolCallId, "API returned non-success status")

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
                "eventTypeTitle": b.get("eventType", {}).get("title"),
                "description": b.get("description"),
                "attendees": [
                    {"name": a.get("name"), "email": a.get("email"), "timeZone": a.get("timeZone")}
                    for a in b.get("attendees", [])
                ],
                "createdAt": b.get("createdAt")
            })

        result = {
            "success": True,
            "appointments": appointments,
            "total_found": len(appointments)
        }
        return vapi_response(vapi_req.toolCallId, result)

    except requests.RequestException as e:
        return handle_error(vapi_req.toolCallId if 'vapi_req' in locals() else "unknown", f"Request failed: {str(e)}")
    except ValueError as ve:
        return handle_error(vapi_req.toolCallId if 'vapi_req' in locals() else "unknown", f"Invalid input: {str(ve)}", 422)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create-booking")
async def create_booking_endpoint(request: Request, authenticated: bool = Depends(verify_token)):
    """Create a new booking."""
    try:
        payload = await request.json()
        vapi_req = VapiRequest(**payload)
        params = CreateBookingParams(**vapi_req.parameters)

        data = client.create_booking(
            event_type_id=params.event_type_id,
            start=params.start,
            attendee_name=params.attendee_name,
            attendee_email=params.attendee_email,
            additional_notes=params.additional_notes
        )

        if data.get("status") != "success":
            return handle_error(vapi_req.toolCallId, "Booking failed - API did not return success")

        booking = data.get("data", {})
        result = {
            "success": True,
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
        }
        return vapi_response(vapi_req.toolCallId, result)

    except requests.RequestException as e:
        return handle_error(vapi_req.toolCallId if 'vapi_req' in locals() else "unknown", f"Booking request failed: {str(e)}")
    except ValueError as ve:
        return handle_error(vapi_req.toolCallId if 'vapi_req' in locals() else "unknown", f"Invalid input: {str(ve)}", 422)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/get-event-types")
async def get_event_types_endpoint(request: Request, authenticated: bool = Depends(verify_token)):
    """Get event types for a team."""
    try:
        payload = await request.json()
        vapi_req = VapiRequest(**payload)
        params = GetEventTypesParams(**vapi_req.parameters)

        # Use team_id from request parameters
        data = client.get_event_types(team_id=params.team_id)

        event_types = data.get("data") or data.get("event_types") or []
        if not isinstance(event_types, list):
            return handle_error(vapi_req.toolCallId, "Unexpected API response format")

        services = []
        for event in event_types:
            event_id = event.get("id")
            if event_id is None:
                continue
            services.append({
                "id": event_id,
                "lengthInMinutes": event.get("length"),
                "title": event.get("title", "Unnamed service"),
                "slug": event.get("slug", ""),
                "description": event.get("description", "").strip() or ""
            })

        result = {
            "success": True,
            "services": services,
            "total": len(services)
        }
        return vapi_response(vapi_req.toolCallId, result)

    except requests.RequestException as e:
        return handle_error(vapi_req.toolCallId if 'vapi_req' in locals() else "unknown", f"API request failed: {str(e)}")
    except ValueError as ve:
        return handle_error(vapi_req.toolCallId if 'vapi_req' in locals() else "unknown", f"Invalid input: {str(ve)}", 422)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok", "version": "1.0.0"}
