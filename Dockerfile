# Use the Python image
FROM python:3.9.19-slim-bullseye

# Set working directory in the container
WORKDIR /chatbot

# Copy the Python scripts and other files to the container
COPY . .

# Install dependencies
RUN pip install update
RUN pip install -r requirements.txt

# Set environment variables
ENV TELEGRAM_TOKEN=6755513596:AAHEFApbZrhkyneepW34zCuIgMgKu2y2o2g
ENV BASICURL=https://chatgpt.hkbu.edu.hk/general/rest
ENV MODELNAME=gpt-4-turbo
ENV APIVERSION=2024-02-15-preview
ENV ACCESS_TOKEN=8cf0d9c3-f999-4b89-a780-6aab50d039c6

# Set the entrypoint
CMD python bot.py
