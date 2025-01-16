# Use the official Python 3.8.10 image from the Docker Hub

FROM python:3.8.10-slim

# Set the working directory

WORKDIR /app

ENV PYTHONPATH=/app

# Copy the requirements file

COPY requirements.txt .

# Install dependencies

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code

COPY . .

RUN python /app/scripts/tscript.py
# Expose the port your Gradio app runs on

EXPOSE 7860

# Command to run your Gradio app

CMD ["python", "scripts/run_app.py"] # Replace 'app.py' with the name of your Gradio app script
