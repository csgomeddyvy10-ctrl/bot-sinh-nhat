FROM python:3.11-slim

WORKDIR /app

# Cài dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY . .

# Expose port cho Render (bắt buộc)
EXPOSE 10000

# Chạy cả bot + web server
CMD ["python", "server.py"]