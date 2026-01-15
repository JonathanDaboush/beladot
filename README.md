# DivinaPopinaV2

## Project Overview

DivinaPopinaV2 is a full-stack mock e-commerce platform designed to demonstrate professional-grade architecture, code quality, and deployment hygiene. This project is intended for client demonstration and technical review, not for production use.

**Key Features:**
- Modern React frontend with API-only data access
- Python backend (Quart, SQLAlchemy) with clear domain boundaries
- Explicit mock boundaries for all financial, payment, and shipment operations
- Professional .gitignore and repo hygiene
- Demonstrates error handling, loading/empty states, and maintainable structure

---

## Mock Project Notice

> **All financial, shipment, and payment operations in this project are mocked.**
>
> - No real money, payment, or shipment transactions occur.
> - Domain logic is real; all external side effects are simulated.
> - This is intentional for demonstration and client review purposes.

---

## Repository Structure

```
divinaPopinaV2/
├── backend/           # Python backend (Quart, SQLAlchemy)
│   ├── app.py         # Main backend app
│   ├── controller/    # (Ready for real controllers)
│   ├── model/         # Domain models
│   ├── persistance/   # Database persistence logic
│   ├── repository/    # Data access repositories
│   ├── service/       # Business logic services
│   ├── services/      # Utility and mock services
│   └── ...
├── frontend/          # React frontend
│   ├── public/
│   ├── src/
│   │   ├── api/       # All data access (no direct fetch in components)
│   │   ├── hooks/     # Custom hooks for data/state
│   │   ├── pages/     # Page components (thin, orchestrate only)
│   │   └── ...
│   ├── .gitignore     # Excludes node_modules, build, etc.
│   └── ...
├── .gitignore         # Excludes Python, OS, and editor artifacts
└── README.md          # This file
```

---

## .gitignore Hygiene

- **frontend/.gitignore** excludes:
  - `/node_modules` (never committed)
  - `/build`, `/coverage`, and environment files
- **.gitignore** (root) excludes:
  - Python bytecode, venv, OS/editor files, logs, and Jupyter checkpoints
- **Best Practice:**
  - Always run `npm install` in frontend and `pip install -r requirements.txt` in backend after cloning.

---

## How to Add Details / Configure

### Frontend
- All data must come from `src/api/` services.
- Add new API endpoints in `src/api/` and corresponding hooks in `src/hooks/`.
- Never use inline mock data or hardcoded arrays in components/pages.
- Handle loading, error, and empty states in every page.
- To add a new page:
  1. Create a new file in `src/pages/`
  2. Use hooks for data fetching
  3. Render only based on `{ data, loading, error }`

### Backend
- Add new domain models in `backend/model/`.
- Add new business logic in `backend/service/`.
- Add new API endpoints in `backend/app.py` or in `backend/controller/` (if using blueprints).
- All payment/finance/shipment logic is mocked in `backend/services/payment_service_mock.py`.
- To add a real integration, create a new service and update the dependency injection in the app.

---

## Deployment & Local Setup

1. **Clone the repo:**
   ```sh
   git clone <repo-url>
   cd divinaPopinaV2
   ```
2. **Install backend dependencies:**
   ```sh
   cd backend
   pip install -r requirements.txt
   ```
3. **Install frontend dependencies:**
   ```sh
   cd ../frontend
   npm install
   ```
4. **Run backend:**
   ```sh
   cd ../backend
   quart run --reload
   ```
5. **Run frontend:**
   ```sh
   cd ../frontend
   npm start
   ```

---

## Professional Review Checklist

- [x] No node_modules or build artifacts in repo
- [x] .gitignore covers all environments
- [x] Mock boundaries are explicit and documented
- [x] API layer is the only data entry for frontend
- [x] No inline mock data or hardcoded arrays in components
- [x] All pages handle loading, error, and empty states
- [x] Folder names and structure are correct and professional

---

## For Clients & Reviewers

This project is intentionally structured to demonstrate:
- Clean separation of concerns
- Professional repo hygiene
- Explicit mock boundaries
- Readiness for real-world extension

If you have questions or want to see a real integration, please contact the maintainer.
