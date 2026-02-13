"""
Pydantic models for request validation.
"""
from typing import Optional, Union
from pydantic import BaseModel, Field, field_validator
from utils import to_int


class CancelAppointmentParams(BaseModel):
    """Parameters for canceling an appointment."""
    team_id: int = Field(..., description="Team ID for the business")
    booking_id: str | int = Field(..., description="The booking ID or UID to cancel")
    cancellation_reason: str = Field(..., description="Reason for cancellation")
    
    @field_validator('team_id', mode='before')
    @classmethod
    def convert_team_id(cls, v):
        """Convert string to int for team_id."""
        return to_int(v, 'team_id')


class GetAvailableSlotsParams(BaseModel):
    """Parameters for getting available slots."""
    team_id: int = Field(..., description="Team ID for the business")
    event_type_id: int = Field(..., description="ID of the event type")
    start_date: str = Field(..., description="Start date in ISO format (e.g., '2026-02-01')")
    end_date: str = Field(..., description="End date in ISO format (e.g., '2026-02-07')")
    time_zone: Optional[str] = Field(None, description="IANA timezone")
    username: Optional[str] = Field(None, description="Optional username filter")
    format: str = Field("time", description="'time' or 'range'")
    duration: Optional[int] = Field(None, description="Optional duration in minutes")
    
    @field_validator('team_id', mode='before')
    @classmethod
    def convert_team_id(cls, v):
        """Convert string to int for team_id."""
        return to_int(v, 'team_id')
    
    @field_validator('event_type_id', mode='before')
    @classmethod
    def convert_event_type_id(cls, v):
        """Convert string to int for event_type_id."""
        return to_int(v, 'event_type_id')
    
    @field_validator('duration', mode='before')
    @classmethod
    def convert_duration(cls, v):
        """Convert string to int for duration (optional field)."""
        return to_int(v, 'duration')


class GetUpcomingAppointmentsParams(BaseModel):
    """Parameters for getting upcoming appointments."""
    team_id: int = Field(..., description="Team ID for the business")
    patient_email: str = Field(..., description="Patient's email to filter bookings")
    limit: Optional[int] = Field(10, description="Max number of bookings to return")
    after: Optional[str] = Field(None, description="Show only after this ISO date")
    
    @field_validator('team_id', mode='before')
    @classmethod
    def convert_team_id(cls, v):
        """Convert string to int for team_id."""
        return to_int(v, 'team_id')
    
    @field_validator('limit', mode='before')
    @classmethod
    def convert_limit(cls, v):
        """Convert string to int for limit (optional field)."""
        return to_int(v, 'limit')


class CreateBookingParams(BaseModel):
    """Parameters for creating a booking."""
    team_id: int = Field(..., description="Team ID for the business")
    event_type_id: int = Field(..., description="ID of the event type")
    start: str = Field(..., description="Start time in ISO UTC format (e.g., '2026-02-09T04:45:00.000Z')")
    attendee_name: str = Field(..., description="Attendee's full name")
    attendee_email: str = Field(..., description="Attendee's email")
    additional_notes: Optional[str] = Field(None, description="Optional notes")
    
    @field_validator('team_id', mode='before')
    @classmethod
    def convert_team_id(cls, v):
        """Convert string to int for team_id."""
        return to_int(v, 'team_id')
    
    @field_validator('event_type_id', mode='before')
    @classmethod
    def convert_event_type_id(cls, v):
        """Convert string to int for event_type_id."""
        return to_int(v, 'event_type_id')


class GetEventTypesParams(BaseModel):
    """Parameters for getting event types."""
    team_id: int = Field(..., description="Team ID for the business")
    
    @field_validator('team_id', mode='before')
    @classmethod
    def convert_team_id(cls, v):
        """Convert string to int for team_id."""
        return to_int(v, 'team_id')
