# GearGuard - Maintenance Management System

A comprehensive maintenance management system built with FastAPI, SQLite, and modern web technologies.

## Features

- **Equipment Management**: Create, read, update, and delete equipment with full details
- **Maintenance Teams**: Manage teams and assign equipment to teams
- **Maintenance Requests**: Track corrective and preventive maintenance requests
- **Kanban Board**: Drag-and-drop workflow management for maintenance requests
- **Calendar View**: Visual calendar for preventive maintenance scheduling
- **Overdue Detection**: Automatic detection and highlighting of overdue requests
- **Smart Auto-fill**: Equipment team automatically fills when creating requests

## Tech Stack

- **Backend**: Python 3.8+, FastAPI
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Database**: SQLite with SQLAlchemy ORM
- **Styling**: Bootstrap 5.3.0
- **Architecture**: MVC pattern

## Project Structure

```
gearGuard/
├── backend/
│   ├── main.py          # FastAPI application entry point
│   ├── models.py        # SQLAlchemy database models
│   ├── routes.py        # API routes and endpoints
│   └── database.py      # Database configuration
├── frontend/
│   ├── templates/       # HTML templates
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── equipment.html
│   │   ├── kanban.html
│   │   └── calendar.html
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           ├── main.js
│           ├── equipment.js
│           ├── kanban.js
│           └── calendar.js
├── requirements.txt
└── README.md
```

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. **Clone or navigate to the project directory**
   ```bash
   cd gearGuard
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   
   On Windows:
   ```bash
   venv\Scripts\activate
   ```
   
   On Linux/Mac:
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

6. **Run the application**
   ```bash
   python run.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn backend.main:app --reload
   ```

7. **Seed sample data (optional)**
   ```bash
   python backend/seed_data.py
   ```
   This will create sample teams, equipment, and maintenance requests for testing.

8. **Access the application**
   - Open your browser and navigate to: `http://localhost:8000`
   - The API documentation is available at: `http://localhost:8000/docs`

### Quick Start (After Downloading from GitHub)

If you just downloaded the project, simply:

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python run.py
   ```

3. **Open browser to:** `http://localhost:8000`

**If you get "localhost refused to connect":**
- See `SETUP.md` for detailed troubleshooting
- Make sure dependencies are installed
- Check that the server started successfully (look for "Uvicorn running" message)

## Usage Guide

### 1. Create Maintenance Teams
- Navigate to Equipment page
- Teams are created automatically when you assign equipment (or you can use the API)

### 2. Add Equipment
- Click "Add Equipment" button
- Fill in all required fields
- Select a maintenance team
- Save the equipment

### 3. Create Maintenance Requests
- Go to Kanban Board
- Click "Create Request"
- Select equipment (team auto-fills)
- Choose request type (Corrective/Preventive)
- Set scheduled date for preventive maintenance
- Save the request

### 4. Manage Requests via Kanban
- Drag and drop requests between status columns
- Status automatically updates
- Overdue requests are highlighted in red

### 5. View Calendar
- Navigate to Calendar page
- See all preventive maintenance scheduled for the month
- Click on events to view details
- Overdue items are highlighted

## API Endpoints

### Equipment
- `GET /api/equipment` - List all equipment
- `GET /api/equipment/{id}` - Get equipment by ID
- `POST /api/equipment` - Create new equipment
- `PUT /api/equipment/{id}` - Update equipment
- `DELETE /api/equipment/{id}` - Delete equipment

### Teams
- `GET /api/teams` - List all teams
- `GET /api/teams/{id}` - Get team by ID
- `POST /api/teams` - Create new team
- `PUT /api/teams/{id}` - Update team
- `DELETE /api/teams/{id}` - Delete team

### Maintenance Requests
- `GET /api/maintenance-requests` - List all requests
- `GET /api/maintenance-requests/{id}` - Get request by ID
- `POST /api/maintenance-requests` - Create new request
- `PUT /api/maintenance-requests/{id}` - Update request
- `DELETE /api/maintenance-requests/{id}` - Delete request

## Status Colors

- **New**: Blue (#0d6efd)
- **In Progress**: Yellow (#ffc107)
- **Repaired**: Green (#198754)
- **Scrap**: Gray (#6c757d)
- **Overdue**: Red (#dc3545)

## Business Logic

1. **Auto-fill Team**: When creating a maintenance request, selecting equipment automatically fills the team field
2. **Scrap Status**: Marking a request as "Scrap" automatically marks the associated equipment as scrapped
3. **Overdue Detection**: Requests with scheduled dates in the past (and not completed) are marked as overdue
4. **Preventive Maintenance**: Only preventive requests appear in the calendar view

## Database

The application uses SQLite database (`gearGuard.db`) which is automatically created on first run. The database includes:

- `equipment` table
- `maintenance_teams` table
- `maintenance_requests` table

## Development

To modify the application:

1. Backend changes: Edit files in `backend/`
2. Frontend changes: Edit files in `frontend/templates/` and `frontend/static/`
3. Database changes: Modify models in `backend/models.py`

## Troubleshooting

- **Port already in use**: Change the port in `backend/main.py` or use `--port` flag with uvicorn
- **Database errors**: Delete `gearGuard.db` to reset the database
- **Static files not loading**: Ensure the `frontend/static/` directory structure is correct

## License

This project is open source and available for use.

## Support

For issues or questions, please check the code comments or API documentation at `/docs` endpoint.

