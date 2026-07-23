#Event Ticket Booking System — Backend

Django REST API backend for an event ticket booking platform.
Supports organizer-created events, tiered ticket types, 
real-time-safe bookings (no overselling), and JWT-based authentication with role-based access.

Live API: https://ticketbooking-backend-wvo2.onrender.com
API Docs: https://ticketbooking-backend-wvo2.onrender.com/api/docs/ 
Frontend: https://ticketbooking-frontend.vercel.app

#Tech Stack
Framework: Django + Django REST Framework
Auth: JWT via djangorestframework-simplejwt
Database: PostgreSQL
Docs: drf-spectacular (OpenAPI/Swagger)
Static files: WhiteNoise
Server: Gunicorn (production), Django dev server (local)
Containerization: Docker + Docker Compose
CI: GitHub Actions
Deployment: Render

#Project Objectives
Provide a secure, role-based backend for booking event tickets
Support organizers creating and managing their own events
Demonstrate a production-style workflow: containerization, CI/CD, feature-branch development

#Data Models (Schemas)
Model	Description
User	Custom user model (email login), roles: customer / organizer / admin
Venue	Physical location where events are hosted
Event	An event tied to a Venue and an organizing User
TicketType	A pricing tier for an Event (e.g. VIP, Regular) with stock tracking
Booking	A user's booking of a quantity of a TicketType
Payment	Payment record tied one-to-one with a Booking

#Authentication & Authorization
JWT access/refresh tokens via /api/auth/login/, /api/auth/register/, /api/auth/login/refresh/
Roles: customer, organizer, admin
Organizers can create/edit their own events; customers can only book and view their own bookings; 
admins have full access

#Key API Endpoints
Endpoint	Description
POST /api/auth/register/	Create an account
POST /api/auth/login/	Obtain JWT tokens
GET /api/events/	List all events (public)
POST /api/events/	Create an event (organizer only)
POST /api/bookings/	Book tickets (authenticated)
GET /api/bookings/mine/	View your own bookings

#Local Development
##Prerequisites
Docker + Docker Compose
Python 3.12 (for local venv work outside Docker, optional)
Setup
bash
git clone https://github.com/lysaomondi/ticketbooking-backend.git
cd ticketbooking-backend
cp .env.example .env   # fill in your own values
docker compose up

This starts Postgres, applies migrations, collects static files, 
and runs the Django dev server at http://localhost:8000.

#Create a superuser
bash
docker compose exec backend python manage.py createsuperuser
Useful commands
bash
docker compose up -d              # start in background
docker compose down                # stop everything
docker compose logs -f backend     # tail backend logs
docker compose exec backend python manage.py <command>

CI/CD

GitHub Actions (.github/workflows/backend.yml) runs on every push/PR to main: installs dependencies, 
runs Django system checks, and builds the Docker image.
Render auto-deploys from main on every successful merge.

