# Backend (FastAPI)
FROM python:3.9-slim-buster as backend

WORKDIR /app

# Copy the backend source code
COPY api /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Frontend (React)
FROM node:14 as frontend

WORKDIR /app

# Copy the frontend source code
COPY web /app

# Install dependencies and build the React app
RUN npm ci --silent
RUN npm run build

# Final image
FROM python:3.9-slim-buster

WORKDIR /app

# Copy the built React app from the frontend stage
COPY --from=web /app/build /app/build

# Copy the backend source code
COPY api /app

# Install backend dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variables
ENV DATABASE_URL=sqlite:///app.db
ENV SECRET_KEY=your-secret-key
ENV ACCESS_TOKEN_EXPIRE_MINUTES=30

# Expose the port for the FastAPI application
EXPOSE 8000

# Run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
