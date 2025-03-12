# Use an official Python runtime as a parent image
FROM python:3.11

# Set environment variables
ENV PORT=8080
ENV PYTHONUNBUFFERED=True

# Create a working directory inside the container
WORKDIR /app

# Copy only the necessary files
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory
COPY . .

# Expose the port that Streamlit runs on
EXPOSE 8080

# Run the application
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
