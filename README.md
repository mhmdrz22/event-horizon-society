# University Scientific Association Management System

This is a comprehensive management system for a university's scientific association, built with a modern tech stack. The platform allows students and faculty to engage with the association's activities, including news, events, and article submissions.

## Features

- **User Authentication**: Secure user registration and login.
- **Role-Based Access Control**: Different roles for Students, Association Members, and Admins.
- **News and Announcements**: Admins and members can publish news and announcements.
- **Event Management**: Create and manage events, with user registration functionality.
- **Article Submissions**: Users can submit articles for review by the association.
- **Commenting System**: Users can comment on news and events.
- **Admin Dashboard**: A dedicated dashboard for admins to manage users, content, and submissions.

## Tech Stack

- **Frontend**: React, Vite, TypeScript, Shadcn/ui, Tailwind CSS
- **Backend**: FastAPI, Python
- **Database**: PostgreSQL (production), SQLite (development)
- **ORM**: SQLAlchemy

## Getting Started

### Prerequisites

- Node.js (v18.18+ or v20+)
- Python 3.10+
- Poetry (for Python dependency management)

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/event-horizon-society.git
    cd event-horizon-society
    ```

2.  **Setup Backend:**
    ```bash
    # Navigate to the backend directory
    cd app

    # Create a virtual environment
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

    # Install Python dependencies
    pip install -r requirements.txt
    ```

3.  **Setup Frontend:**
    ```bash
    # Navigate back to the root directory
    cd ..

    # Install frontend dependencies
    npm install
    ```

4.  **Environment Variables:**
    - Create a `.env` file in the root directory by copying `.env.example`.
    - Fill in the necessary environment variables, especially the `SECRET_KEY` for JWT. For local development with SQLite, no other database variables are needed.

### Running the Application

1.  **Run the Backend Server:**
    ```bash
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```
    The API will be available at `http://localhost:8000`.

2.  **Run the Frontend Development Server:**
    ```bash
    npm run dev
    ```
    The frontend will be available at `http://localhost:5173`.

## Project Structure

```
/
├── app/                  # FastAPI backend
│   ├── core/             # Core logic, settings
│   ├── db/               # Database session, base model
│   ├── models/           # SQLAlchemy models
│   ├── routers/          # API routers
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic services
│   └── main.py           # Main FastAPI app
├── public/               # Public assets
├── src/                  # React frontend source
│   ├── components/       # Reusable components
│   ├── contexts/         # React contexts (e.g., Auth)
│   ├── hooks/            # Custom React hooks
│   ├── pages/            # Page components
│   ├── schemas/          # TypeScript types/interfaces
│   ├── services/         # API service layer
│   └── App.tsx           # Main App component with routing
├── .env.example          # Example environment variables
├── package.json
└── ...
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License.
