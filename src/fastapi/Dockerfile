FROM mcr.microsoft.com/playwright:v1.42.0-jammy

WORKDIR /app

# Install curl for healthchecks
RUN apt install curl

RUN apt-get update \
 && apt-get install --assume-yes --no-install-recommends --quiet \
        python3 \
        python3-pip \
        curl \
 && apt-get clean all

# Setup a nonroot user for security
# RUN adduser --disabled-password nonroot
# USER nonroot

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir --progress-bar off --upgrade -r requirements.txt
RUN python3 -m playwright install chromium

# Copy the app
COPY main.py /app/main.py

# Expose the app's port
EXPOSE 8000

# Run the FastAPI server
ENTRYPOINT ["python3", "-m"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
