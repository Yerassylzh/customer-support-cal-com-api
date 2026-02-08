# Cal.com API - Quick Usage Guide

## Running the Server

```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Start server
python main.py
```

Server runs at: `http://localhost:8000`  
API Docs: `http://localhost:8000/docs`

---

## 🔒 Authentication Required

**All API endpoints require bearer token authentication.**

Add this header to every request:
```
Authorization: Bearer your_secure_token_here
```

**Setup:**
1. Set `API_AUTH_TOKEN` in your `.env` file
2. Add the same token to Vapi custom tool headers

See [AUTH_SETUP.md](AUTH_SETUP.md) for detailed instructions.

---

## Request Format

Send parameters directly in the request body:

```json
{
  "team_id": 189647,
  ...other parameters
}
```

> **Important:** All endpoints require `team_id` parameter for multi-business support.

---

## Endpoints

### 1. Get Event Types (Services)

**Endpoint:** `POST /get-event-types`

```json
{
  "team_id": 189647
}
```

**Response:**
```json
{
  "success": true,
  "services": [...],
  "total": 5
}
```

---

### 2. Get Available Slots

**Endpoint:** `POST /get-available-slots`

```json
{
  "team_id": 189647,
  "event_type_id": 12345,
  "start_date": "2026-02-10",
  "end_date": "2026-02-17",
  "time_zone": "Asia/Almaty",
  "format": "time"
}
```

**Optional parameters:** `username`, `duration`

---

### 3. Get Upcoming Appointments

**Endpoint:** `POST /get-upcoming-appointments`

```json
{
  "team_id": 189647,
  "patient_email": "patient@example.com",
  "limit": 10
}
```

**Optional parameters:** `after` (ISO date)

---

### 4. Create Booking

**Endpoint:** `POST /create-booking`

```json
{
  "team_id": 189647,
  "event_type_id": 12345,
  "start": "2026-02-15T10:00:00.000Z",
  "attendee_name": "John Doe",
  "attendee_email": "john@example.com"
}
```

**Optional parameters:** `additional_notes`

---

### 5. Cancel Appointment

**Endpoint:** `POST /cancel-appointment`

```json
{
  "team_id": 189647,
  "booking_id": "abc-123-def",
  "cancellation_reason": "Patient requested reschedule"
}
```

---

## Testing with cURL

```bash
curl -X POST http://localhost:8000/get-event-types \
  -H "Authorization: Bearer your_secure_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "team_id": 189647
  }'
```

---

## Environment Variables

Create `.env` file:
```
CALCOM_API_KEY=cal_live_your_api_key_here
API_AUTH_TOKEN=your_secure_token_here
```

**Notes:** 
- `TEAM_ID` is no longer in `.env` - it comes from request parameters
- `API_AUTH_TOKEN` is required for authentication - see [AUTH_SETUP.md](AUTH_SETUP.md)
