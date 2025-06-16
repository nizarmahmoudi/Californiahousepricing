# Start from a lightweight base image
FROM python:3.7-slim


# 2. Set working directory
WORKDIR /app

# 3. Copy requirements first (for faster builds when deps don't change often)
COPY requirements.txt .

# 4. Install required packages
RUN pip install --no-cache-dir -r requirements.txt

# 5. Then copy all files
COPY . .

# 6. Expose port 5000 (Flask's port by default)
EXPOSE 5000

# 7. Run the application
CMD ["python", "app.py"]

