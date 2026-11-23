# Padmraj Chougule Portfolio

Single-page React portfolio with a FastAPI contact endpoint and optional MongoDB persistence.

## Requirements

- Node.js 18 or newer
- Python 3.10 or newer
- MongoDB (optional; contact messages remain available in memory if MongoDB is not running)

## Run the frontend

```powershell
cd frontend
npm install
Copy-Item .env.example .env
npm start
```

The app runs at `http://localhost:3000`.

## Run the backend

In another terminal:

```powershell
cd backend
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python -m uvicorn server:app --reload --port 8001
```

The API runs at `http://localhost:8001`; interactive API documentation is at `http://localhost:8001/docs`.

The frontend's `frontend/.env.example` sets `REACT_APP_BACKEND_URL=http://localhost:8001`. Restart the frontend after changing this setting.

For persistent contact messages, start MongoDB and configure `MONGO_URL` and `DB_NAME` in `backend/.env`. Without MongoDB, the contact API uses an in-memory fallback for local testing.

## Contact API

- `GET /api/` — API health response
- `POST /api/contact` — submit a contact form
- `GET /api/contact?limit=20` — retrieve recent messages for local verification
