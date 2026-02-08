# Authentication & CORS Setup

## Overview

✅ **Bearer Token Authentication** - Protects all API endpoints  
✅ **CORS Enabled** - Allows all origins (fixes Vapi network errors)  
✅ **Health Check Public** - No auth required for `/health`

## Configuration

### 1. Set Your Auth Token

Edit `.env`:
```bash
CALCOM_API_KEY=cal_live_xxxxxxxx
API_AUTH_TOKEN=your_secure_token_here  # ← Change this!
```

**Generate a secure token:**
```bash
# Option 1: Random string
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Option 2: Use any strong password/token
```

### 2. Add to Render (When Deploying)

In Render dashboard → Environment variables:
- Key: `API_AUTH_TOKEN`
- Value: `your_secure_token_here`

## Using Authentication

### All API Requests Must Include Bearer Token

**Header Format:**
```
Authorization: Bearer your_secure_token_here
```

### cURL Example

```bash
curl -X POST https://your-api.onrender.com/get-event-types \
  -H "Authorization: Bearer your_secure_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "toolCallId": "test-123",
    "parameters": {"team_id": 189647}
  }'
```

### Vapi Configuration

In Vapi custom tools, add Server URL Authorization:

**Settings:**
- **Server URL:** `https://your-api.onrender.com/get-event-types`
- **Headers:**
  - Key: `Authorization`
  - Value: `Bearer your_secure_token_here`

OR set at assistant level for all tools.

### Python Example

```python
import requests

headers = {
    "Authorization": "Bearer your_secure_token_here",
    "Content-Type": "application/json"
}

response = requests.post(
    "https://your-api.onrender.com/get-event-types",
    headers=headers,
    json={
        "toolCallId": "call-123",
        "parameters": {"team_id": 189647}
    }
)
```

## CORS Configuration

**Current Settings:** Allow all origins/methods/headers

This is configured in `main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # All origins
    allow_credentials=True,
    allow_methods=["*"],  # All methods
    allow_headers=["*"],  # All headers
)
```

**Why:** Vapi requests come from various origins, so we allow all to prevent network errors.

## Security Notes

🔒 **Keep your API_AUTH_TOKEN secret** - don't commit to git  
🔒 **The `/health` endpoint is public** - no auth required  
🔒 **Invalid tokens return HTTP 401 Unauthorized**  
✅ **CORS is permissive** - authentication provides the security layer

## Testing Authentication

### Valid Token (Success)
```bash
curl -H "Authorization: Bearer your_secure_token_here" \
     http://localhost:8000/health
# Returns: {"status": "ok", "version": "1.0.0"}
```

### Invalid Token (Fails)
```bash
curl -H "Authorization: Bearer wrong-token" \
     -X POST http://localhost:8000/get-event-types \
     -d '{"toolCallId": "t1", "parameters": {"team_id": 189647}}'
# Returns: 401 Unauthorized
```

### No Token (Fails)
```bash
curl -X POST http://localhost:8000/get-event-types
# Returns: 401 Unauthorized
```
