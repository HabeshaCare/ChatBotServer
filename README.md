# Enderase LLM-Server

Welcome to the Enderase LLM-Server repository! This server, built using Flask, is the backbone of the Enderase chatbot, responsible for handling user queries and delivering relevant answers along with context. Below, you'll find guidance on setting up and using this server.

## Overview

The Enderase LLM-Server acts as the central engine for the Enderase chatbot. It utilizes generative AI models and ensures the seamless retrieval of legal information.

## Running the Container

You can easily run the Enderase backend using Docker. Here are the steps:

1. **Build the Container:**

   - Use the following command to build the Docker container:
     ```
     docker build --tag enderase-docker .
     ```

2. **Run the Container:**
   - Run the container with the following command:
     ```
     docker run -e FLASK_APP=main.py -e PALM_API_KEY=<your_palm_api_key> enderase-docker
     ```
     Replace `<your_palm_api_key>` with your actual Palm API key.

## Configuration

Before running the container, ensure you configure the necessary environment variables, including your Palm API key, in the `.env` file.
