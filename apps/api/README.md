# Recruity AI API

This FastAPI project provides backend APIs for Recruity AI. Use Poetry for dependency management.

## Development

1. Install dependencies:
   ```bash
   poetry install
   ```
2. Run the application:
   ```bash
   poetry run uvicorn app.main:app --reload
   ```

The API exposes versioned routes under `/api/v1`. A hello endpoint can be
accessed at:

```bash
curl http://localhost:8000/api/v1/hello
```
