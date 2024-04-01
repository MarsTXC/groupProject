# Use the Python image
FROM python

# Set working directory in the container
WORKDIR /chatbot

# Copy the Python scripts and other files to the container
COPY . ./chatbot

# Install dependencies
RUN pwd 
RUN ls
RUN pip install update
RUN pip install -r requirements.txt

# Set environment variables
ENV TELEGRAM_TOKEN=6953324907:AAHqJZf0lEo4zfbJPGSTmzKDOrbXazXj5Fo
ENV BASICURL=https://chatgpt.hkbu.edu.hk/general/rest
ENV MODELNAME=gpt-4-turbo
ENV APIVERSION=2024-02-15-preview
ENV chatGPT_access_token=7d00a1fc-01e5-4b8e-bb9c-56494b6581c5

# Set the entrypoint
CMD python chatbot.py
