# Recruity AI API

Tenant‑aware FastAPI application. Dependencies are managed with Poetry.

## Development

1. Install dependencies
   ```bash
   poetry install
   ```
2. Start the server
   ```bash
   poetry run uvicorn app:app --reload
   ```

`RECRUITY_TENANT_HEADER` can be set to change the tenant header name.
