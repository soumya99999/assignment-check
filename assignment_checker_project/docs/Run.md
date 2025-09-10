# How to Run

## 1. Running Redis Server using Docker
Start Redis server using Docker:
- If the container doesn't exist: `docker run --name my-redis-server -d -p 6379:6379 redis`
- If the container already exists: `docker start my-redis-server`

## 2. Install Dependencies
Navigate to the backend directory:
```bash
cd assignment_checker_project
```

Activate the virtual environment:
- Windows: `myenv\Scripts\activate`
- macOS/Linux: `source myenv/bin/activate`

Install dependencies:
```bash
pip install -r requirements.txt
```

## 3. Set up PostgreSQL Database
Install PostgreSQL:
- Windows: Download and install from [PostgreSQL official website](https://www.postgresql.org/download/windows/)
- macOS: Use Homebrew: `brew install postgresql`
- Linux: Use package manager: `sudo apt install postgresql`

Create database in PostgreSQL and update the database configuration in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Run database migrations:
```bash
python manage.py migrate
```

## 4. Set up Environment Variables
Create a `.env` file in the backend directory with necessary environment variables:
```bash
# Example .env file
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost:5432/db_name
REDIS_URL=redis://localhost:6379/0
GEMINI_API_KEY=your-gemini-api-key
```

## 5. Install Tesseract OCR (Required for PDF processing)
Install Tesseract OCR engine:
- Windows: Download from [GitHub releases](https://github.com/UB-Mannheim/tesseract/wiki)
- macOS: `brew install tesseract`
- Linux: `sudo apt install tesseract-ocr`

## 6. Start Celery Worker
Navigate to the backend directory and start Celery worker:
```bash
cd assignment_checker_project
# Activate virtual environment (Windows)
myenv\Scripts\activate
# Or for macOS/Linux: source myenv/bin/activate

celery -A assignment_checker_project worker --loglevel=info --pool=solo
```

## 7. Start Django Development Server
In a new terminal, navigate to the backend directory and start the Django server:
```bash
cd assignment_checker_project
# Activate virtual environment (Windows)
myenv\Scripts\activate
# Or for macOS/Linux: source myenv/bin/activate

python manage.py runserver
```
