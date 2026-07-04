# SPAZIO — Shoppable AI Interior Designer

> **Final Year Project** | AI-powered room transformation with interactive e-commerce shopping.  
> Built with FastAPI · React.js · Gemini 1.5 Flash · Vertex AI Imagen 3 · Google Cloud Platform

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Tech Stack](#tech-stack)
4. [Project Structure](#project-structure)
5. [Quick Start (Local Development)](#quick-start)
6. [API Reference](#api-reference)
7. [Module Descriptions](#module-descriptions)
8. [Database Schema](#database-schema)
9. [Configuration](#configuration)
10. [Running Tests](#running-tests)
11. [Deployment (Google Cloud)](#deployment)
12. [Future Scope](#future-scope)

---

## Project Overview

SPAZIO addresses the **"imagination gap"** in home improvement — the disconnect between seeing an inspiring room design and being able to purchase the specific items that make it a reality.

### The Two-Phase Workflow

```
PHASE 1: Structure-Aware Generation
┌─────────────┐    ┌──────────────────┐    ┌───────────────┐    ┌──────────────┐
│ User uploads │ →  │ Gemini 1.5 Flash │ →  │ Architectural │ →  │ Imagen 3     │
│ room photo   │    │ (Vision Analysis)│    │ Constraints   │    │ (Redesign)   │
└─────────────┘    └──────────────────┘    └───────────────┘    └──────────────┘

PHASE 2: Interactive Shopping
┌─────────────┐    ┌──────────────────┐    ┌───────────────┐    ┌──────────────┐
│ User clicks  │ →  │ Coordinate crop  │ →  │ Gemini Vision │ →  │ Shopping     │
│ on item      │    │ (Pillow/Python)  │    │ (Identify)    │    │ Links        │
└─────────────┘    └──────────────────┘    └───────────────┘    └──────────────┘
```

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      React.js Frontend                       │
│   LandingPage │ DesignStudio │ ProjectsPage │ ProjectDetail  │
│   UploadZone │ StyleSelector │ InteractiveCanvas │ ProductCard│
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP / REST API
┌──────────────────────────▼──────────────────────────────────┐
│                    FastAPI Backend                            │
│  /api/vision/analyze    → Vision Analysis Router             │
│  /api/generate/room     → Generation Router                  │
│  /api/shopping/identify → Shopping Router                    │
│  /api/projects/         → Projects CRUD Router               │
└─────┬───────────────┬───────────────┬────────────────────────┘
      │               │               │
┌─────▼──────┐  ┌─────▼──────┐  ┌────▼────────────────────────┐
│ Gemini 1.5 │  │ Vertex AI  │  │ PostgreSQL / SQLite           │
│ Flash API  │  │ Imagen 3   │  │ (Users, Projects, Designs,   │
│ (Vision +  │  │ (Generate) │  │  IdentifiedItems)            │
│  Shopping) │  └────────────┘  └─────────────────────────────┘
└────────────┘
      │
┌─────▼──────────────────────────────────────────────────────┐
│              Google Cloud Storage (GCS)                     │
│  /uploads   - Original room photos                         │
│  /generated - Imagen 3 redesign renders                    │
│  /crops     - Furniture identification crops               │
└────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | React.js 18 + Vite | SPA with component-based UI |
| **Styling** | Tailwind CSS | Utility-first responsive design |
| **Routing** | React Router v6 | Client-side navigation |
| **HTTP Client** | Axios | API communication |
| **File Upload** | react-dropzone | Drag-and-drop image upload |
| **Notifications** | react-hot-toast | User feedback |
| **Backend** | FastAPI (Python) | High-performance async REST API |
| **ORM** | SQLAlchemy | Database abstraction |
| **Database** | SQLite (dev) / PostgreSQL (prod) | Relational data storage |
| **AI Vision** | Gemini 1.5 Flash | Room analysis + item identification |
| **AI Generation** | Vertex AI Imagen 3 | Photorealistic room redesign |
| **Image Processing** | Pillow (PIL) | Coordinate cropping |
| **Cloud** | Google Cloud Platform | Hosting + AI services |
| **Container** | Docker + Docker Compose | Environment consistency |
| **Testing** | pytest | Backend test suite |

---

## Project Structure

```
shoppable-ai-interior/
│
├── backend/
│   ├── main.py                     # FastAPI app entry point
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── start.sh
│   ├── .env.example
│   │
│   ├── models/
│   │   ├── database.py             # SQLAlchemy ORM models
│   │   └── schemas.py              # Pydantic request/response schemas
│   │
│   ├── routers/
│   │   ├── health.py               # Health check endpoint
│   │   ├── vision.py               # Phase 1: Upload & analyze
│   │   ├── generate.py             # Phase 2: Image generation
│   │   ├── shopping.py             # Phase 3: Click-to-shop
│   │   └── projects.py             # Project CRUD
│   │
│   ├── services/
│   │   ├── gemini_service.py       # Gemini 1.5 Flash integration
│   │   ├── imagen_service.py       # Vertex AI Imagen 3 integration
│   │   ├── image_service.py        # Pillow-based image processing
│   │   └── ecommerce_service.py    # Shopping URL generation
│   │
│   ├── tests/
│   │   └── test_backend.py         # Full pytest test suite
│   │
│   ├── uploads/                    # Raw user uploads (auto-created)
│   ├── generated/                  # Imagen 3 outputs (auto-created)
│   └── crops/                      # Shopping phase crops (auto-created)
│
├── frontend/
│   ├── index.html
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── package.json
│   ├── Dockerfile
│   ├── start.sh
│   ├── .env.example
│   │
│   └── src/
│       ├── main.jsx                # React entry point
│       ├── App.jsx                 # Router + Toaster setup
│       ├── index.css               # Design system + animations
│       │
│       ├── pages/
│       │   ├── LandingPage.jsx     # Marketing homepage
│       │   ├── DesignStudio.jsx    # Main studio workflow
│       │   ├── ProjectsPage.jsx    # Project gallery
│       │   └── ProjectDetail.jsx   # Single project view
│       │
│       ├── components/
│       │   ├── Navbar.jsx
│       │   ├── UploadZone.jsx      # Drag-and-drop upload
│       │   ├── StyleSelector.jsx   # 8-style grid selector
│       │   ├── InteractiveCanvas.jsx # Click-to-shop canvas
│       │   ├── StructuralAnalysisPanel.jsx
│       │   ├── ProductCard.jsx     # Shopping modal
│       │   └── LoadingSpinner.jsx
│       │
│       └── utils/
│           └── api.js              # Axios API client
│
├── docker-compose.yml
├── start.sh                        # Root launcher script
└── README.md
```

---

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+
- A [Gemini API Key](https://aistudio.google.com/app/apikey) (free tier works)

### 1. Clone and Navigate
```bash
git clone <your-repo-url>
cd shoppable-ai-interior
```

### 2. Configure Backend
```bash
cd backend
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
nano .env
```

### 3. Start Backend
```bash
# From /backend directory
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
Backend will be live at **http://localhost:8000**  
Interactive API docs at **http://localhost:8000/docs**

### 4. Start Frontend
```bash
# In a new terminal, from /frontend directory
cd frontend
npm install
npm run dev
```
Frontend will be live at **http://localhost:3000**

### One-Command Start (Both Services)
```bash
# From project root
bash start.sh
```

---

## API Reference

### Vision Analysis
```http
POST /api/vision/analyze
Content-Type: multipart/form-data

file: <image file>          # JPEG/PNG/WebP, max 20MB
room_name: "Living Room"    # optional
```
**Response:**
```json
{
  "project_id": "uuid",
  "original_img_url": "/uploads/upload_xxx.jpg",
  "analysis": {
    "room_type": "living room",
    "window_positions": ["left wall - large picture window"],
    "door_positions": ["north wall"],
    "ceiling_height": "standard (8-9 feet)",
    "floor_type": "hardwood",
    "lighting_conditions": "bright natural",
    "fixed_elements": ["fireplace on north wall"],
    "design_constraints": ["preserve window on left wall"],
    "summary": "..."
  }
}
```

### Generate Redesign
```http
POST /api/generate/room
Content-Type: application/json

{
  "project_id": "uuid-from-analysis",
  "style": "scandinavian"
}
```
**Response:**
```json
{
  "design_id": "uuid",
  "project_id": "uuid",
  "style": "scandinavian",
  "output_img_url": "/generated/design_xxx_scandinavian.jpg",
  "message": "Room successfully redesigned in Scandinavian style. Click any item to shop!"
}
```

### Identify & Shop
```http
POST /api/shopping/identify
Content-Type: application/json

{
  "design_id": "uuid-from-generation",
  "click_x": 452,
  "click_y": 310,
  "image_width": 900,
  "image_height": 600
}
```
**Response:**
```json
{
  "item_id": "uuid",
  "product_name": "Mid-Century Modern Walnut Lounge Chair",
  "product_description": "An elegant lounge chair...",
  "crop_url": "/crops/crop_abc123.jpg",
  "amazon_url": "https://amazon.com/s?k=mid+century+walnut+lounge+chair",
  "ikea_url": "https://ikea.com/us/en/search/?q=walnut+lounge+chair",
  "google_shopping_url": "https://google.com/search?q=...",
  "wayfair_url": "https://wayfair.com/keyword.php?keyword=..."
}
```

### Other Endpoints
| Method | Path | Description |
|---|---|---|
| `GET` | `/api/health` | System health + config status |
| `GET` | `/api/vision/styles` | Available design styles |
| `GET` | `/api/projects/` | List all projects |
| `GET` | `/api/projects/{id}` | Get project with designs |
| `DELETE` | `/api/projects/{id}` | Delete a project |
| `GET` | `/api/shopping/history/{design_id}` | Get identified items for a design |

---

## Module Descriptions

### Vision Analysis Module (VAM)
**File:** `services/gemini_service.py`  
The "Brain" of the system. Uses Gemini 1.5 Flash with structured JSON prompting to extract architectural metadata from room photos. Applies few-shot prompting to ensure consistent output format. Falls back to mock data in development mode.

### Generative Rendering Module (GRM)
**File:** `services/imagen_service.py`  
Interfaces with Vertex AI Imagen 3 for photorealistic room transformation. Constructs structure-aware prompts by combining the style keywords with architectural constraints from the VAM. Includes a PIL-based fallback for development environments without GCP credentials.

### Spatial Interaction Module (SIM)
**Files:** `services/image_service.py` + `components/InteractiveCanvas.jsx`  
Handles the shopping phase. Frontend captures `clientX/clientY` coordinates, normalizes them against the rendered image dimensions, and sends to the backend. Backend uses Pillow to crop a 300×300 pixel region centered on the click, then passes to Gemini for identification.

### E-Commerce Integration Module (EIM)
**File:** `services/ecommerce_service.py`  
Generates shopping URLs for 7 retailers (Amazon, IKEA, Wayfair, Houzz, Etsy, Overstock, Google Shopping) using URL-encoded search queries derived from the AI-identified product name and attributes.

---

## Database Schema

```sql
-- Users
CREATE TABLE users (
    user_id    TEXT PRIMARY KEY,
    email      TEXT UNIQUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Projects (one room = one project)
CREATE TABLE projects (
    project_id      TEXT PRIMARY KEY,
    user_id         TEXT,
    room_name       TEXT,
    original_img_url TEXT NOT NULL,
    structural_json  TEXT,           -- JSON from Gemini analysis
    created_at      TIMESTAMP DEFAULT NOW()
);

-- Generated Designs (multiple styles per project)
CREATE TABLE generated_designs (
    design_id      TEXT PRIMARY KEY,
    project_id     TEXT NOT NULL,   -- FK → projects
    style_tag      TEXT NOT NULL,
    output_img_url TEXT NOT NULL,
    prompt_used    TEXT,
    created_at     TIMESTAMP DEFAULT NOW()
);

-- Identified Items (shopping history per design)
CREATE TABLE identified_items (
    item_id          TEXT PRIMARY KEY,
    design_id        TEXT NOT NULL,  -- FK → generated_designs
    click_x          INTEGER NOT NULL,
    click_y          INTEGER NOT NULL,
    product_name     TEXT NOT NULL,
    product_description TEXT,
    crop_url         TEXT,
    shopping_url     TEXT NOT NULL,
    amazon_url       TEXT,
    ikea_url         TEXT,
    created_at       TIMESTAMP DEFAULT NOW()
);
```

---

## Configuration

### Backend `.env`
| Variable | Description | Required |
|---|---|---|
| `GEMINI_API_KEY` | From [Google AI Studio](https://aistudio.google.com) | ✅ For AI features |
| `GOOGLE_CLOUD_PROJECT` | GCP project ID for Imagen 3 | Optional (fallback used) |
| `VERTEX_LOCATION` | GCP region (default: `us-central1`) | Optional |
| `DATABASE_URL` | DB connection string | Optional (SQLite default) |

### Frontend `.env`
| Variable | Description |
|---|---|
| `VITE_API_URL` | Backend URL (empty = use Vite proxy for local dev) |

---

## Running Tests

```bash
cd backend

# Install test dependencies (included in requirements.txt)
pip install pytest httpx

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --tb=short

# Run specific test class
pytest tests/test_backend.py::TestCropRegion -v
pytest tests/test_backend.py::TestGenerateShoppingUrls -v
```

### Test Coverage
| Test Class | Area |
|---|---|
| `TestCropRegion` | Coordinate mapping, boundary clamping, normalization |
| `TestValidateImage` | Image quality validation |
| `TestOptimizeForAI` | Image resize optimization |
| `TestGenerateShoppingUrls` | URL generation, encoding, edge cases |
| `TestStructuralAnalysisSchema` | Pydantic schema validation |
| `TestHealthEndpoint` | API health check |
| `TestStylesEndpoint` | Styles listing |
| `TestProjectsEndpoint` | Project CRUD |
| `TestUploadEndpoint` | File upload validation |
| `TestShoppingEndpoint` | Shopping flow |
| `TestEdgeCases` | Boundary conditions, unicode, scaled coords |

---

## Deployment (Google Cloud)

### Backend → Cloud Run
```bash
# Build and push Docker image
cd backend
gcloud builds submit --tag gcr.io/YOUR_PROJECT/spazio-backend

# Deploy to Cloud Run
gcloud run deploy spazio-backend \
  --image gcr.io/YOUR_PROJECT/spazio-backend \
  --platform managed \
  --region us-central1 \
  --set-env-vars GEMINI_API_KEY=xxx,GOOGLE_CLOUD_PROJECT=xxx \
  --allow-unauthenticated
```

### Frontend → Firebase Hosting
```bash
cd frontend
npm run build

firebase init hosting
firebase deploy
```

### Database → Cloud SQL (PostgreSQL)
```bash
gcloud sql instances create spazio-db \
  --database-version=POSTGRES_15 \
  --region=us-central1 \
  --tier=db-f1-micro
```
Then update `DATABASE_URL` in Cloud Run environment variables.

---

## Future Scope

1. **AR Integration** — WebXR overlay of identified furniture in real space using USDZ/glTF models
2. **Conversational Design** — Multi-turn chat with Gemini to iteratively refine the design ("make the sofa blue")
3. **Budget Filtering** — Financial constraint layer to filter shopping results by price range
4. **Real-Time Inventory** — Direct retailer API integration (Amazon PA API, IKEA API) for live stock status
5. **Contractor Export** — PDF blueprint generation with HEX color codes for sharing with professionals
6. **Sustainability Mode** — AI-recommended eco-friendly, locally-sourced furniture alternatives

---

## Authors

Final Year B.Tech Project  
Department of Computer Science  
**Technology Stack:** FastAPI · React.js · Gemini 1.5 Flash · Vertex AI Imagen 3 · GCP

---

*"Bridging the gap between digital inspiration and retail acquisition."*
