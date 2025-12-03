# EileenClassRoom Project Guidelines (Updated)

## Project Context

**Purpose**: Class management webapp for preschool parents (4-year-olds class)

- Calendar with events and snack-day assignments
- Messaging between parents
- Broadcast announcements
- ~50 users
- Mobile-first (PWA)
- Self-hosted on VPS with Docker + Caddy + CI/CD

**Primary Goal**: Learn modern web development with a clean, maintainable architecture.

---

## Tech Stack (Final)

### Backend
- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy 2.x ORM** (typed models with `Mapped[...]`)
- **Alembic** migrations
- **Pydantic v2** schemas
- **WebSockets** for real-time message updates

### Frontend
- **React 18 + TypeScript**
- **Vite**
- **React Router**
- **TanStack Query**
- **TailwindCSS**
- **Vite PWA plugin** (later; add once basic app works)

### Authentication
- **JWT (access token)** for API auth
- Password hashing with **bcrypt** (`passlib[bcrypt]`)
- Optional later: refresh tokens

### Deployment
- Docker containers
- Caddy reverse proxy
- PostgreSQL container (separate)
- Images published to GHCR and deployed via GitHub Actions

---

# Backend Guidelines (FastAPI + SQLAlchemy 2.x)

## Core Principles

- Prefer **clarity** over cleverness (small project, long-lived)
- Keep endpoints thin: **routes call services**
- Services operate on **DB sessions** and return ORM objects
- API layer converts ORM → Pydantic schemas (response models)

## Project Structure


### Update the project structure (around line 46):

Add both `core/` and `utils/`:

```python
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                      # Create FastAPI app, include routers, middleware
│   ├── config.py                    # Pydantic v2 Settings (env vars)
│   ├── db.py                        # engine + Base + get_db() dependency
│   │
│   ├── models/                      # SQLAlchemy ORM models (SQLAlchemy 2.x typed style)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── event.py
│   │   ├── message.py
│   │   └── snack_assignment.py
│   │
│   ├── schemas/                     # Pydantic v2 schemas (request/response DTOs)
│   │   ├── __init__.py
│   │   ├── user.py                  # UserCreate, UserRead, UserUpdate, Token, etc.
│   │   ├── event.py                 # EventCreate, EventRead, EventUpdate
│   │   ├── message.py               # MessageCreate, MessageRead
│   │   └── snack_assignment.py       # SnackAssignCreate, SnackAssignRead
│   │
│   ├── api/                         # FastAPI routers + dependency wiring
│   │   ├── __init__.py
│   │   ├── deps.py                  # get_db re-export, get_current_user, require_admin, etc.
│   │   ├── auth.py                  # /api/auth/* (login, refresh, logout, me)
│   │   ├── users.py                 # /api/users/*
│   │   ├── events.py                # /api/events/*
│   │   ├── messages.py              # /api/messages/* (REST history/post)
│   │   └── ws.py                    # /api/ws/* (websocket endpoints)
│   │
│   ├── services/                    # Business logic (DB operations, rules)
│   │   ├── __init__.py
│   │   ├── auth_service.py          # authenticate(), issue tokens, etc.
│   │   ├── user_service.py          # create_user(), list_users(), etc.
│   │   ├── event_service.py         # create/list/update events
│   │   ├── message_service.py       # post message, list channel history
│   │   └── snack_service.py         # assign snacks rules, rotation checks
│   │
│   ├── security/                    # Security primitives (no FastAPI here)
│   │   ├── __init__.py
│   │   ├── passwords.py             # hash_password(), verify_password()
│   │   └── jwt.py                   # create_access_token(), decode_token()
│   │
│   ├── core/                        # Cross-cutting app concerns (optional)
│   │   ├── __init__.py
│   │   ├── logging.py               # logging config
│   │   └── errors.py                # custom exceptions
│   │
│   └── utils/                       # Utility functions and helpers
│       └── __init__.py
│
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       └── .gitkeep
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                  # test db/session fixtures
│   ├── test_auth.py
│   ├── test_users.py
│   ├── test_events.py
│   └── test_messages.py
│
├── pyproject.toml                   # tooling config (ruff, mypy, pytest, etc.)
├── requirements.txt                 # Python deps (or switch to requirements.in/uv/poetry later)
├── Dockerfile
├── .env.example                     # sample env vars (no secrets)
└── README.md
```

### Naming conventions
- `models/` = database models
- `schemas/` = input/output DTOs
- `api/` = FastAPI routers
- `services/` = business logic
- `security/` = hashing/JWT
- `core/` = cross-cutting concerns (logging, errors, config)
- `utils/` = helper functions

---

## SQLAlchemy 2.x Setup (Recommended)

### `app/db.py`
Use SQLAlchemy 2.x style base and session dependency:

```python
from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, DeclarativeBase

from app.config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

class Base(DeclarativeBase):
    pass

def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
```

- No `SessionLocal` required unless you want global session defaults.
- `Depends(get_db)` ensures session cleanup after each request.

---

## ORM Models: Typed `Mapped[...]` style

### Example `User` model (recommended style)
```python
from datetime import datetime
from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )
```

---

## Query style (SQLAlchemy 2.x)

Avoid legacy:

```python
db.query(Event).filter(...).all()  # legacy style
```

Prefer:

```python
from sqlalchemy import select

events = db.scalars(select(Event).order_by(Event.event_date.desc())).all()
```

- `db.scalars(select(...))` returns ORM instances.
- This is the SQLAlchemy 2.x idiomatic approach.

---

## Pydantic v2 Schemas

Use separate schemas for Create/Update/Read.

```python
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class UserBase(BaseModel):
    email: str
    full_name: str = Field(min_length=1, max_length=255)

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=100)

class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime
```

Notes:
- In Pydantic v2, prefer `ConfigDict(from_attributes=True)` over `class Config`.
- Use `*Read` naming to make response schemas explicit.

---

## Services: business logic lives here

Guidelines:
- Services take `db: Session`
- Services **typically commit** for writes and return ORM objects
- Services raise domain errors / `HTTPException` (either is fine, pick one style and stick to it)

Example:

```python
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.user import UserCreate
from app.security.passwords import hash_password

class UserService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_user(self, data: UserCreate) -> User:
        existing = self.db.scalar(select(User).where(User.email == data.email))
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )
        user = User(
            email=data.email,
            full_name=data.full_name,
            hashed_password=hash_password(data.password),
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
```

---

## API Routers

Keep routers thin: validation + dependency wiring only.

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import UserService

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("", response_model=UserRead)
def create_user(payload: UserCreate, db: Session = Depends(get_db)) -> UserRead:
    return UserService(db).create_user(payload)
```

---

## WebSockets (real-time messaging)

Use REST for:
- message history (`GET /api/messages`)
- posting messages (`POST /api/messages`) OR WS send

Use WebSocket for:
- live “new message” events broadcast to connected clients

Recommended WS endpoint:
- `GET ws(s)://<host>/api/ws/messages?channel=general`

---

## Async vs Sync decision (important)

For this project, prefer **sync SQLAlchemy** + sync endpoints for database operations.

**Pattern:**
- Use `def` (sync) for endpoints that use database sessions
- Use `async def` for simple endpoints without DB operations (health checks, static responses)
- FastAPI runs sync functions in a threadpool automatically

**Why sync for DB:**
- Simpler to understand and debug
- Plenty fast for ~50 users
- Less boilerplate code
- Better for learning fundamentals

**Example:**
```python
@router.get("/health")
async def health_check():  # async - no DB
    return {"status": "ok"}

@router.get("/users")
def get_users(db: Session = Depends(get_db)):  # sync - uses DB
    return db.query(User).all()

---

## Testing
- Write tests for all service layer methods
- Use **pytest** with **pytest-asyncio**
- Mock external dependencies
- Test both success and failure cases

---

<!-- # React Frontend Guidelines

### Code Style
- Use **TypeScript** strictly (no `any` types)
- Use **functional components** with hooks (no class components)
- Use **Prettier** for formatting
- Use **ESLint** for linting
- Maximum line length: **100 characters**

### Project Structure
```
frontend/
├── public/
│   ├── manifest.json        # PWA manifest
│   └── icons/
├── src/
│   ├── main.tsx             # App entry point
│   ├── App.tsx              # Root component
│   ├── components/          # Reusable components
│   │   ├── common/          # Generic components (Button, Card, etc.)
│   │   ├── layout/          # Layout components (Header, Sidebar)
│   │   └── features/        # Feature-specific components
│   │       ├── calendar/
│   │       ├── messages/
│   │       └── auth/
│   ├── pages/               # Page components (routes)
│   │   ├── HomePage.tsx
│   │   ├── CalendarPage.tsx
│   │   ├── MessagesPage.tsx
│   │   └── LoginPage.tsx
│   ├── hooks/               # Custom hooks
│   │   ├── useAuth.ts
│   │   ├── useEvents.ts
│   │   └── useMessages.ts
│   ├── services/            # API communication
│   │   ├── api.ts           # Axios instance
│   │   ├── authService.ts
│   │   ├── eventService.ts
│   │   └── messageService.ts
│   ├── types/               # TypeScript types
│   │   ├── event.ts
│   │   ├── message.ts
│   │   └── user.ts
│   ├── utils/               # Utilities
│   │   ├── dateFormat.ts
│   │   └── validation.ts
│   └── styles/
│       └── index.css        # Tailwind imports
├── tests/
├── package.json
├── tsconfig.json
├── vite.config.ts
└── Dockerfile
```

### React Patterns

**1. Component Structure**
```typescript
import { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { eventService } from '@/services/eventService';
import { Event } from '@/types/event';

interface EventListProps {
  filterType?: string;
  onEventClick?: (event: Event) => void;
}

/**
 * Displays a list of class events with optional filtering.
 */
export function EventList({ filterType, onEventClick }: EventListProps) {
  const { data: events, isLoading, error } = useQuery({
    queryKey: ['events', filterType],
    queryFn: () => eventService.getEvents({ type: filterType }),
  });

  if (isLoading) {
    return <div className="text-center py-8">Loading events...</div>;
  }

  if (error) {
    return (
      <div className="text-red-600 py-4">
        Error loading events. Please try again.
      </div>
    );
  }

  if (!events || events.length === 0) {
    return <div className="text-gray-500 py-4">No events found.</div>;
  }

  return (
    <div className="space-y-4">
      {events.map((event) => (
        <EventCard
          key={event.id}
          event={event}
          onClick={() => onEventClick?.(event)}
        />
      ))}
    </div>
  );
}
```

**2. Custom Hooks**
```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { eventService } from '@/services/eventService';
import { Event, EventCreate } from '@/types/event';

/**
 * Hook for managing events data and operations.
 */
export function useEvents(filterType?: string) {
  const queryClient = useQueryClient();

  const {
    data: events,
    isLoading,
    error,
  } = useQuery({
    queryKey: ['events', filterType],
    queryFn: () => eventService.getEvents({ type: filterType }),
  });

  const createMutation = useMutation({
    mutationFn: (newEvent: EventCreate) => eventService.createEvent(newEvent),
    onSuccess: () => {
      // Invalidate and refetch events
      queryClient.invalidateQueries({ queryKey: ['events'] });
    },
  });

  return {
    events,
    isLoading,
    error,
    createEvent: createMutation.mutate,
    isCreating: createMutation.isPending,
  };
}
```

**3. TypeScript Types**
```typescript
/**
 * Represents a calendar event or snack assignment.
 */
export interface Event {
  id: number;
  title: string;
  description?: string;
  eventDate: string; // ISO 8601 format
  eventType: 'snack' | 'activity' | 'meeting' | 'other';
  assignedParentId?: number;
  assignedParentName?: string;
  createdAt: string;
  updatedAt: string;
}

/**
 * Data required to create a new event.
 */
export interface EventCreate {
  title: string;
  description?: string;
  eventDate: string;
  eventType: 'snack' | 'activity' | 'meeting' | 'other';
  assignedParentId?: number;
}
```

**4. API Service**
```typescript
import axios from 'axios';
import { Event, EventCreate } from '@/types/event';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

/**
 * Service for event-related API calls.
 */
export const eventService = {
  /**
   * Fetch all events with optional filtering.
   */
  async getEvents(params?: { type?: string }): Promise<Event[]> {
    const response = await api.get<Event[]>('/api/events', { params });
    return response.data;
  },

  /**
   * Create a new event.
   */
  async createEvent(event: EventCreate): Promise<Event> {
    const response = await api.post<Event>('/api/events', event);
    return response.data;
  },

  /**
   * Delete an event by ID.
   */
  async deleteEvent(id: number): Promise<void> {
    await api.delete(`/api/events/${id}`);
  },
};
```

### Mobile-First Styling (TailwindCSS)
```tsx
// Always start with mobile, then add larger breakpoints
<div className="
  p-4           /* Mobile: small padding */
  md:p-6        /* Tablet: medium padding */
  lg:p-8        /* Desktop: large padding */
  grid
  grid-cols-1   /* Mobile: 1 column */
  md:grid-cols-2 /* Tablet: 2 columns */
  lg:grid-cols-3 /* Desktop: 3 columns */
  gap-4
">
  {/* Content */}
</div>

// Use touch-friendly sizes (min 44x44px for buttons)
<button className="
  px-6 py-3      /* Large touch target */
  text-lg        /* Readable text size */
  font-semibold
  bg-blue-500
  text-white
  rounded-lg
  active:bg-blue-600 /* Touch feedback */
  transition-colors
">
  Add Event
</button>
```

### State Management
- Use **TanStack Query** for server state (API data)
- Use **useState** for local component state
- Use **Context API** for global app state (auth, theme)
- Avoid Redux unless app grows significantly complex

### Performance
- Use **React.memo** for expensive components
- Lazy load routes with **React.lazy**
- Optimize images (WebP format, responsive sizes)
- Use **Suspense** for loading states

---

## General Best Practices

### Naming Conventions
- **Python**: `snake_case` for functions/variables, `PascalCase` for classes
- **TypeScript**: `camelCase` for functions/variables, `PascalCase` for components/types
- **Files**: `kebab-case` for utilities, `PascalCase` for React components
- **Constants**: `UPPER_SNAKE_CASE`

### Comments & Documentation
- Write docstrings for all public functions/classes
- Use JSDoc comments for TypeScript functions
- Explain **why**, not **what** (code should be self-documenting)
- Keep comments up-to-date with code changes

### Git Workflow
- Commit messages: `feat:`, `fix:`, `docs:`, `refactor:`, `test:` prefixes
- Keep commits small and focused
- Write descriptive commit messages

### Environment Variables
- **Backend**: Use `.env` file, load with `python-dotenv`
- **Frontend**: Use `.env` file, prefix with `VITE_`
- Never commit `.env` files (add to `.gitignore`)

### Security
- **Never** store passwords in plain text
- Use **JWT tokens** with short expiration (1 hour)
- Implement **refresh tokens** for session management
- Validate **all** user input on backend
- Use **HTTPS** in production
- Implement **CORS** properly
- Rate limit API endpoints

---

## PWA Configuration

### Manifest File
```json
{
  "name": "EileenClassRoom",
  "short_name": "ClassRoom",
  "description": "Class management for parents",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#3b82f6",
  "icons": [
    {
      "src": "/icons/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

### Service Worker Strategy
- Cache API responses for offline access
- Cache static assets (JS, CSS, images)
- Use "Network First" strategy for dynamic content
- Use "Cache First" for static assets -->

---

## Development Workflow

### Initial Setup
1. Create virtual environment for Python
2. Install dependencies: `pip install -r requirements.txt`
3. Set up PostgreSQL database
4. Run migrations: `alembic upgrade head`
5. Install Node dependencies: `npm install`
6. Start backend: `uvicorn app.main:app --reload`
7. Start frontend: `npm run dev`

### Before Committing
1. Run Python linters: `black .`, `isort .`, `mypy .`
2. Run Python tests: `pytest`
3. Run TypeScript checks: `npm run type-check`
4. Run ESLint: `npm run lint`
5. Test on mobile device or browser DevTools mobile mode

---

## Questions to Address During Development

- [ ] Authentication: Email/password or magic links?
- [ ] Notification system: Email, push notifications, or both?
- [ ] File uploads: Allow parents to share photos?
- [ ] Snack assignment: Manual or automatic rotation?
- [ ] Message history: Keep forever or delete after X months?
- [ ] Admin role: Who can create events and assign snacks?