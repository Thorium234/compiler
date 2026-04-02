# Campus Code Lab

Campus Code Lab is a lightweight, offline-friendly coding platform designed for universities with limited infrastructure.

It allows students to write and execute Python code from low-end devices while the heavy computation runs on a campus-hosted server.

## Problem

Many students in African universities lack:

- Personal laptops
- Powerful smartphones
- Stable internet access
- Proper development environments

Existing tools assume strong internet and modern devices. This system is built for the opposite.

## Solution

A mobile-first, browser-based coding platform with:

- Local code editing (works offline)
- Server-side execution (runs on campus server)
- Minimal data usage
- Lecturer-controlled assignments

## Core Features (v1)

### Student

- Write Python code in browser
- Auto-save locally (offline support)
- Provide input via input box
- Run code and view output
- Submit assignment

### Lecturer

- Create assignments
- Define input and expected output
- View submissions
- See pass/fail results

## Architecture

### Backend

- Django (monolithic application)
- Handles users, assignments, submissions
- API endpoints for execution

### Execution Engine

- Docker containers
- Runs untrusted Python code safely
- Enforces:
  - Time limits
  - Memory limits
  - CPU limits

### Frontend

- Simple mobile-first interface
- Runs in browser
- Uses IndexedDB for offline storage

### Storage

- SQLite (v1, simple deployment)
- IndexedDB (client-side)

## How It Works

1. Student writes code in browser
2. Code is saved locally
3. Student clicks "Run"
4. Code is sent to backend
5. Backend runs code in Docker container
6. Output is returned and displayed
7. Student submits solution

## Deployment (v1 Goal)

- Single server (campus machine)
- Docker installed
- One command to start system

## Tech Stack

- Backend: Django
- Execution: Docker
- Language: Python
- Frontend: HTML, minimal JS (upgrade later)

## Future Improvements

- Multi-language support
- Offline sync system
- Plagiarism detection
- Real-time collaboration
- Better mobile UI

## Philosophy

Build for:

- Low bandwidth
- Cheap devices
- Real classrooms

Not for:

- Perfect architecture
- Fancy features