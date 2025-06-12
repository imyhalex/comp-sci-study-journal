# Understanding Environment Variables in Django Projects

## Introduction

Environment variables are a crucial part of modern web application development, especially in Django projects. They allow you to:

1. **Keep sensitive information secure** (database credentials, API keys, secret tokens)
2. **Configure different environments** (development, testing, production)
3. **Avoid hardcoding values** in your source code
4. **Follow the [12-factor app methodology](https://12factor.net/config)** for better application design

This guide explains how to identify required environment variables in a Django project, how to set them up, and provides specific examples from the Chatbook backend project.

## How Django Projects Use Environment Variables

Django projects typically access environment variables in these ways:

1. **Direct access** using Python's `os.environ` dictionary:
   ```python
   import os
   secret_key = os.environ.get('SECRET_KEY', 'default-value')
   ```

2. **Using django-environ** (a third-party package) for more advanced features:
   ```python
   import environ
   env = environ.Env()
   environ.Env.read_env()  # Reads .env file
   secret_key = env('SECRET_KEY')
   ```

3. **Using python-dotenv** to load .env files:
   ```python
   from dotenv import load_dotenv
   load_dotenv()  # Loads .env file
   ```

## How to Identify Required Environment Variables

To identify what environment variables a Django project needs, I look at:

1. **Settings files** (settings.py, settings_dev.py, etc.)
   - Check for `os.environ.get()` calls
   - Look for django-environ usage
   - Identify hardcoded secrets that should be environment variables

2. **Example files** (.env.example, sample.env)
   - These are template files showing required variables

3. **Documentation** (README.md, docs/)
   - Project documentation often lists required environment variables

4. **Dependencies** (requirements.txt)
   - Check if packages like django-environ or python-dotenv are used

## Chatbook Backend Environment Variables

In the Chatbook backend project, I identified needed environment variables by:

1. Checking **requirements.txt** which includes:
   ```
   django-environ==0.12.0
   python-dotenv==1.1.0
   ```
   This indicates the project uses environment variables.

2. Looking at **settings.py** for hardcoded values that should be environment variables:
   ```python
   SECRET_KEY = 'django-insecure-k99^83^3e($2mlk8my-@n29uc*-3l(*840)d(u&=^lpia(1#*o'
   RECOVERY_TOKEN_HMAC_KEY = 'C$t3D-gH1kL2mN3p4R5s6T7v8W9xYz$AbCdEfGhIjK'
   DEBUG = True
   ```

3. Searching for direct environment variable usage:
   ```
   grep -r "os.environ" .
   grep -r "env(" .
   ```

4. Checking for references to `.env` files in documentation

### Minimum Required Variables

Based on the analysis, the minimum required variables for Chatbook backend are:

```
SECRET_KEY=django-insecure-k99^83^3e($2mlk8my-@n29uc*-3l(*840)d(u&=^lpia(1#*o
RECOVERY_TOKEN_HMAC_KEY=C$t3D-gH1kL2mN3p4R5s6T7v8W9xYz$AbCdEfGhIjK
DEBUG=True
```

### Additional Variables Based on Functionality

Depending on which features you're using:

1. **Database configuration** (if not using SQLite):
   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/chatbook
   ```

2. **Email configuration**:
   ```
   EMAIL_HOST=smtp.example.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=your-email@example.com
   EMAIL_HOST_PASSWORD=your-password
   EMAIL_USE_TLS=True
   ```

3. **Social authentication**:
   ```
   GOOGLE_CLIENT_ID=your-client-id
   GOOGLE_CLIENT_SECRET=your-client-secret
   ```

4. **Celery** (for background tasks):
   ```
   CELERY_BROKER_URL=redis://localhost:6379/0
   CELERY_RESULT_BACKEND=redis://localhost:6379/0
   ```

## Working with .env Files

### Creating and Editing .env Files

```bash
# Create a new .env file
touch .env

# Add a variable to .env
echo "VARIABLE_NAME=value" >> .env

# View contents of .env
cat .env

# Edit .env with a text editor
nano .env
# or
vim .env
# or
code .env  # if using VS Code
```

### Loading Environment Variables

In a Django project, environment variables from .env files are loaded in one of these ways:

1. **Using python-dotenv**:
   ```python
   # At the top of settings.py
   from dotenv import load_dotenv
   load_dotenv()
   ```

2. **Using django-environ**:
   ```python
   # At the top of settings.py
   import environ
   env = environ.Env()
   environ.Env.read_env()
   ```

## Security Best Practices

1. **Never commit .env files to version control**:
   - Add `.env` to your `.gitignore` file
   - Create `.env.example` with dummy values as a template

2. **Use different .env files for different environments**:
   - `.env.development` for development
   - `.env.test` for testing
   - `.env.production` for production

3. **Use strong, random values for secrets**:
   ```bash
   # Generate a secure random string in terminal
   python -c "import secrets; print(secrets.token_urlsafe(50))"
   ```

4. **Validate required environment variables**:
   ```python
   # In settings.py
   required_env_vars = ['SECRET_KEY', 'DATABASE_URL']
   for var in required_env_vars:
       if var not in os.environ:
           raise Exception(f"Required environment variable {var} is not set.")
   ```

## Common Django Environment Variables

| Variable | Purpose | Example Value |
|----------|---------|---------------|
| SECRET_KEY | Django's secret key for security | Random string |
| DEBUG | Enable/disable debug mode | True/False |
| ALLOWED_HOSTS | Hosts Django can serve | example.com,localhost |
| DATABASE_URL | Database connection string | postgresql://user:password@localhost/dbname |
| STATIC_URL | URL to serve static files | /static/ |
| MEDIA_URL | URL to serve media files | /media/ |
| DJANGO_SETTINGS_MODULE | Settings file to use | myproject.settings |
| EMAIL_* | Email configuration | smtp.gmail.com |
| CACHE_URL | Cache configuration | redis://localhost:6379/1 |

## Conclusion

Understanding how to work with environment variables is essential for Django development. By properly using environment variables, you keep your application secure, configurable, and following best practices.

In the Chatbook backend project, you should at minimum set up the SECRET_KEY, RECOVERY_TOKEN_HMAC_KEY, and DEBUG variables, and add others as you need them for specific functionality. 

# Real-World Example: Setting Up Chatbook Backend

This walkthrough provides a real-world example of setting up environment variables for the Chatbook backend project from scratch.

## Step 1: Analyzing the Project

First, let's understand what environment variables we need by examining the project:

```bash
# Check requirements for environment variable libraries
grep -E "environ|dotenv" requirements.txt
```

Output:
```
django-environ==0.12.0
python-dotenv==1.1.0
```

This confirms the project uses environment variable libraries.

## Step 2: Checking Settings Files

Next, look at the settings files:

```bash
# Look for hardcoded secrets in settings.py
grep -E "SECRET_KEY|KEY|PASSWORD" settings.py
```

This would show us:
```python
SECRET_KEY = 'django-insecure-k99^83^3e($2mlk8my-@n29uc*-3l(*840)d(u&=^lpia(1#*o'
RECOVERY_TOKEN_HMAC_KEY = 'C$t3D-gH1kL2mN3p4R5s6T7v8W9xYz$AbCdEfGhIjK'
```

## Step 3: Checking for Environment Variable Usage

```bash
# Look for direct environment variable access
grep -r "os.environ.get" .
```

This shows files that are already accessing environment variables, like:
```
./accounts/recovery.py:env_key = os.environ.get('RECOVERY_TOKEN_HMAC_KEY')
```

## Step 4: Creating the .env File

Now we'll create a .env file with necessary variables:

```bash
# Create .env file
touch .env

# Add basic environment variables
echo "# Django settings" >> .env
echo "SECRET_KEY='django-insecure-k99^83^3e($2mlk8my-@n29uc*-3l(*840)d(u&=^lpia(1#*o'" >> .env
echo "RECOVERY_TOKEN_HMAC_KEY='C$t3D-gH1kL2mN3p4R5s6T7v8W9xYz$AbCdEfGhIjK'" >> .env
echo "DEBUG=True" >> .env
echo "ALLOWED_HOSTS=localhost,127.0.0.1" >> .env

# Add database configuration (if using PostgreSQL)
# echo "DATABASE_URL=postgresql://user:password@localhost:5432/chatbook" >> .env

# Add email configuration
echo "" >> .env
echo "# Email settings" >> .env
echo "EMAIL_HOST=smtp.example.com" >> .env
echo "EMAIL_PORT=587" >> .env
echo "EMAIL_HOST_USER=your-email@example.com" >> .env
echo "EMAIL_HOST_PASSWORD=your-password" >> .env
echo "EMAIL_USE_TLS=True" >> .env

# Add social auth (if needed)
echo "" >> .env
echo "# Social authentication" >> .env
echo "GOOGLE_CLIENT_ID=your-client-id" >> .env
echo "GOOGLE_CLIENT_SECRET=your-client-secret" >> .env

# Add Celery configuration (if using)
echo "" >> .env
echo "# Celery settings" >> .env
echo "CELERY_BROKER_URL=redis://localhost:6379/0" >> .env
echo "CELERY_RESULT_BACKEND=redis://localhost:6379/0" >> .env
```

## Step 5: Checking If Environment Variables Are Loaded

To ensure Django is properly loading our environment variables, we need to verify how they're loaded in the settings.py file.

Since we don't see explicit dotenv loading code in the current settings.py file, we might need to add it.

### Option 1: Add to settings.py

Add this at the top of settings.py:

```python
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Then use them like this:
SECRET_KEY = os.environ.get('SECRET_KEY', 'default-fallback-key')
RECOVERY_TOKEN_HMAC_KEY = os.environ.get('RECOVERY_TOKEN_HMAC_KEY', 'default-recovery-key')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
```

### Option 2: Create a settings_env.py

Alternatively, create a new settings file that imports from the main one:

```bash
# Create settings_env.py
echo 'from settings import *' > settings_env.py
echo 'import os' >> settings_env.py
echo 'from dotenv import load_dotenv' >> settings_env.py
echo '' >> settings_env.py
echo '# Load environment variables' >> settings_env.py
echo 'load_dotenv()' >> settings_env.py
echo '' >> settings_env.py
echo '# Override settings with environment variables' >> settings_env.py
echo "SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY)" >> settings_env.py
echo "RECOVERY_TOKEN_HMAC_KEY = os.environ.get('RECOVERY_TOKEN_HMAC_KEY', RECOVERY_TOKEN_HMAC_KEY)" >> settings_env.py
echo "DEBUG = os.environ.get('DEBUG', 'False') == 'True'" >> settings_env.py
```

## Step 6: Running Django with Environment Variables

Now run Django using the settings that load environment variables:

```bash
# If you modified settings.py directly
python manage.py runserver

# If you created settings_env.py
python manage.py runserver --settings=settings_env
```

## Step 7: Verifying Environment Variables Are Loaded

To verify our environment variables are loaded, create a simple Django management command:

```bash
# Create directory for management commands
mkdir -p accounts/management/commands
touch accounts/management/commands/__init__.py
touch accounts/management/commands/check_env.py

# Create the command file
cat > accounts/management/commands/check_env.py << 'EOF'
from django.core.management.base import BaseCommand
import os

class Command(BaseCommand):
    help = 'Check environment variables'

    def handle(self, *args, **options):
        vars_to_check = [
            'SECRET_KEY',
            'RECOVERY_TOKEN_HMAC_KEY',
            'DEBUG',
            'EMAIL_HOST',
            'GOOGLE_CLIENT_ID',
        ]
        
        for var in vars_to_check:
            value = os.environ.get(var)
            if value:
                # Mask sensitive values
                if 'SECRET' in var or 'KEY' in var or 'PASSWORD' in var:
                    display = value[:5] + '...' + value[-5:] if len(value) > 10 else '***'
                else:
                    display = value
                self.stdout.write(self.style.SUCCESS(f'{var}: {display}'))
            else:
                self.stdout.write(self.style.WARNING(f'{var}: Not set'))
EOF
```

Run the command:

```bash
# Using default settings
python manage.py check_env

# Or with custom settings
python manage.py check_env --settings=settings_env
```

## Step 8: Create a .env.example File

As a best practice, create a .env.example file with dummy values:

```bash
# Create .env.example file
cat > .env.example << 'EOF'
# Django settings
SECRET_KEY=your-secret-key-here
RECOVERY_TOKEN_HMAC_KEY=your-recovery-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database settings
# DATABASE_URL=postgresql://user:password@localhost:5432/chatbook

# Email settings
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-password
EMAIL_USE_TLS=True

# Social authentication
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret

# Celery settings
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
EOF
```

## Step 9: Update .gitignore

Make sure .env files are in .gitignore:

```bash
# Check if .env is already in .gitignore
grep ".env" .gitignore

# If not, add it
echo "" >> .gitignore
echo "# Environment variables" >> .gitignore
echo ".env" >> .gitignore
echo ".env.*" >> .gitignore
echo "!.env.example" >> .gitignore
```

## Step 10: Document Environment Variables in README

Finally, update the project README to explain the environment variables:

```markdown
## Environment Variables

This project uses environment variables for configuration. Create a `.env` file in the project root with the following variables:

- `SECRET_KEY`: Django's secret key
- `RECOVERY_TOKEN_HMAC_KEY`: Key for recovery token HMAC operations
- `DEBUG`: Set to "True" for development, "False" for production
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DATABASE_URL`: Database connection string (optional, uses SQLite by default)
- `EMAIL_*`: Email configuration variables
- `GOOGLE_CLIENT_ID`/`GOOGLE_CLIENT_SECRET`: For social authentication
- `CELERY_*`: For background task processing

See `.env.example` for a template.
```

By following these steps, you'll have a properly configured environment variable setup for the Chatbook backend project that follows best practices for security and maintainability. 

# Basic Setup Guide for Chatbook Backend

This section provides a step-by-step guide for setting up the Chatbook Backend project from scratch on your local machine.

## Step 1: Clone the Repository

If you haven't already, clone the repository to your local machine:

```bash
# Navigate to your desired directory
cd ~/projects

# Clone the repository (replace with actual repository URL if different)
git clone https://github.com/yourusername/chatbook-backend.git
cd chatbook-backend
```

## Step 2: Create a Virtual Environment

Create and activate a Python virtual environment:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

## Step 3: Install Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

## Step 4: Set Up Environment Variables

Create a `.env` file with the necessary configuration:

```bash
# Create and open .env file
touch .env
nano .env  # or use any text editor
```

Add these basic variables:

```
SECRET_KEY='django-insecure-k99^83^3e($2mlk8my-@n29uc*-3l(*840)d(u&=^lpia(1#*o'
RECOVERY_TOKEN_HMAC_KEY='C$t3D-gH1kL2mN3p4R5s6T7v8W9xYz$AbCdEfGhIjK'
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

## Step 5: Set Up the Database

Run migrations to create the database schema:

```bash
python manage.py migrate
```

## Step 6: Create a Superuser

Create an admin user to access the Django admin panel:

```bash
# Option 1: Using Django's built-in command
python manage.py createsuperuser

# Option 2: Using the project's custom script
python create_superuser.py
```

## Step 7: Run the Development Server

Start the Django development server:

```bash
# Standard settings
python manage.py runserver

# Or with development settings
python manage.py runserver --settings=settings_dev
```

## Step 8: Access the Application

Once the server is running, you can access:

- Django Admin: http://127.0.0.1:8000/admin/
- API Endpoints: http://127.0.0.1:8000/api/

## Step 9: Explore the API with Postman (Optional)

The project includes Postman collection files for testing the API:

1. Import the collection file `chatbook_api_postman_collection.json` into Postman
2. Import the environment file `chatbook_postman_environment.json`
3. Select the environment in Postman
4. Use the collection to test API endpoints

## Step 10: Additional Components (Optional)

For full functionality, you may need to set up:

### Redis and Celery for Background Tasks

```bash
# Install Redis (Ubuntu)
sudo apt-get install redis-server

# Start Celery worker
celery -A celery worker --loglevel=info

# Start Celery beat for scheduled tasks
celery -A celery beat --loglevel=info
```

### Static Files

Collect static files for production:

```bash
python manage.py collectstatic
```

## Troubleshooting

If you encounter issues:

1. Check the Django debug page for detailed error information
2. Verify your virtual environment is activated
3. Ensure all migrations are applied
4. Check that your .env file has the correct settings
5. Look for any errors in the console output

By following these steps, you should have a working local development environment for the Chatbook Backend project. 