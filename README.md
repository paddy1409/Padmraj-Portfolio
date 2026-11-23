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

## Deploy the frontend to Cloudflare Workers

The root `wrangler.jsonc` configures Wrangler to install frontend dependencies, build the React app, and deploy `frontend/build` as an assets-only Worker. In Cloudflare, use the repository root and deploy command `npx wrangler deploy`; Wrangler runs the configured build command before deployment.

Set `REACT_APP_BACKEND_URL` in the Cloudflare Worker build environment to the public HTTPS origin of the separately hosted FastAPI backend (for example, `https://api.example.com`, without `/api`). Set the backend's `CORS_ORIGINS` to the deployed portfolio origin. Do not use the local `.env.example` values in production.

## Contact API

- `GET /api/` — API health response
- `POST /api/contact` — submit a contact form
- `GET /api/contact?limit=20` — retrieve recent messages for local verification
