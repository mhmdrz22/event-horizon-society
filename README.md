# University Scientific Association Management System

This is a comprehensive management system for a university's scientific association, built with a modern tech stack. The platform allows students and faculty to engage with the association's activities, including news, events, and article submissions.

## Features

- **User Authentication**: Secure user registration and login with JWT.
- **Role-Based Access Control**: Different roles for Students, Association Members, and Admins.
- **News and Announcements**: Admins and members can publish news and announcements.
- **Event Management**: Create and manage events, with user registration functionality.
- **Article Submissions**: Users can submit articles for review by the association.
- **Commenting System**: Users can comment on news and events.
- **Admin Dashboard**: A dedicated dashboard for admins to manage users, content, and submissions.

## Tech Stack

- **Frontend**: React, Vite, TypeScript, Shadcn/ui, Tailwind CSS
- **Backend**: FastAPI, Python
- **Database**: SQLite (for development), easily configurable for PostgreSQL.
- **ORM**: SQLAlchemy

## Getting Started

### Prerequisites

- **Node.js**: Version `18.18.0`, `20.0.0`, or `22.0.0`. We recommend using [nvm](https://github.com/nvm-sh/nvm) to manage Node.js versions.
- **Python**: Version 3.10+
- A virtual environment tool for Python (e.g., `venv`).

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/mhmdrz22/event-horizon-society.git
    cd event-horizon-society
    ```

2.  **Setup Backend:**
    - Navigate to the project root.
    - Create and activate a Python virtual environment:
      ```bash
      python -m venv venv
      source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
      ```
    - Install Python dependencies from the `requirements.txt` file:
      ```bash
      pip install -r requirements.txt
      ```

3.  **Setup Frontend:**
    - Make sure you are in the project root.
    - If you are using `nvm`, run `nvm use` to switch to the correct Node.js version specified in `package.json`.
    - Install frontend dependencies:
      ```bash
      npm install
      ```

4.  **Environment Variables:**
    - Create a `.env` file in the root directory by copying `.env.example`.
    - Generate a `SECRET_KEY` for JWT using a tool like `openssl rand -hex 32` and add it to your `.env` file.
    - For local development, no other variables are needed as the application defaults to using SQLite.

### Running the Application

You will need two separate terminals to run the backend and frontend servers concurrently.

1.  **Run the Backend Server (Terminal 1):**
    - Activate the virtual environment: `source venv/bin/activate`
    - Start the FastAPI server:
      ```bash
      uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
      ```
    - The API will be available at `http://localhost:8000/docs`.

2.  **Run the Frontend Development Server (Terminal 2):**
    - Start the Vite development server:
      ```bash
      npm run dev
      ```
    - The frontend will be available at `http://localhost:5173`.

## Project Structure

```
/
├── app/                  # FastAPI backend
│   ├── core/             # Core logic, settings
│   ├── db/               # Database session, base model
│   ├── models/           # SQLAlchemy models
│   ├── routers/          # API routers
│   ├── schemas/          # Pydantic schemas
│   └── services/         # Business logic services
│   └── main.py           # Main FastAPI app
├── public/               # Public assets
├── src/                  # React frontend source
│   ├── components/       # Reusable components
│   ├── contexts/         # React contexts
│   ├── hooks/            # Custom React hooks
│   ├── pages/            # Page components
│   └── ...
├── .env.example
├── package.json
├── requirements.txt      # Python dependencies
└── ...
```
