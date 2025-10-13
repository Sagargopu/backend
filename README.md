# BuildBuzz API Backend

A FastAPI-based backend service for the BuildBuzz construction management application.

## Features

- **Users Management** - User authentication and profile management
- **Projects Management** - Construction project tracking and management
- **Documents Management** - Document storage and organization
- **Finance Management** - Financial tracking and reporting
- **Payroll Management** - Employee payroll and timesheet management

## Technology Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - SQL toolkit and ORM
- **PostgreSQL** - Database (via psycopg)
- **Uvicorn** - ASGI server for running the application

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── database.py          # Database configuration
│   ├── users/               # User management module
│   ├── projects/            # Project management module
│   ├── documents/           # Document management module
│   ├── finance/             # Finance management module
│   └── payroll/             # Payroll management module
├── requirements.txt         # Python dependencies
├── app.yaml                # Google Cloud App Engine configuration
└── README.md               # Project documentation
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd buildBuzz/backend
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   # source .venv/bin/activate  # On Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Development Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive API Documentation**: http://localhost:8000/docs
- **Alternative API Documentation**: http://localhost:8000/redoc

### Production Deployment

This application is configured for Google Cloud App Engine deployment using the `app.yaml` configuration file.

## API Endpoints

The API includes the following main endpoint groups:

- `/users/*` - User management endpoints
- `/projects/*` - Project management endpoints
- `/documents/*` - Document management endpoints
- `/finance/*` - Finance management endpoints
- `/payroll/*` - Payroll and timesheet endpoints

For detailed API documentation, visit http://localhost:8000/docs when the server is running.

## Development

### Database

The application uses SQLAlchemy for database operations. Models are defined in each module's `models.py` file.

### Adding New Modules

1. Create a new directory under `app/`
2. Add `models.py`, `schemas.py`, `crud.py`, and `api.py`
3. Import and include the router in `app/main.py`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test your changes
5. Submit a pull request

## License

This project is private and proprietary.