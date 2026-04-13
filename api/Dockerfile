# Dockerfile for the FastAPI backend
#
# A Dockerfile is a recipe. Each line is a step.
# Docker reads this top-to-bottom and builds an "image" --
# a snapshot of a mini computer with everything your app needs.
#
# When you "run" that image, it becomes a "container" --
# a live, isolated process running your app.

# STEP 1: Start from a base image
# This is a minimal Linux machine with Python 3.12 pre-installed.
# "slim" means it's stripped down (no GUI, no extras) -- smaller = faster to build.
FROM python:3.12-slim

# STEP 2: Set the working directory inside the container
# All following commands run from /app inside the container.
# Think of it like "cd /app" on the mini Linux machine.
WORKDIR /app

# STEP 3: Copy requirements.txt first (before the rest of the code)
# WHY? Docker caches each step. If requirements.txt hasn't changed,
# Docker skips "pip install" on rebuilds. This saves minutes.
COPY requirements.txt .

# STEP 4: Install Python dependencies
# --no-cache-dir: don't save pip's download cache (keeps image smaller)
RUN pip install --no-cache-dir -r requirements.txt

# STEP 5: Copy the rest of the application code
COPY app/ ./app/

# STEP 6: Tell Docker what port this app listens on
# This is just documentation -- it doesn't actually open the port.
# The port is opened when you run the container.
EXPOSE 8000

# STEP 7: The command to run when the container starts
# This is the same uvicorn command you ran manually in Phase 1,
# but without --reload (no auto-restart in production).
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
