# SMTP Server Project

## Overview

This project provides a simple SMTP server implemented in Python using the `aiosmtpd` library. The server is designed to receive emails and print the details of the received messages, including any attachments. Additionally, the project includes a script for sending test emails to the server. Both the server and the email sender script are containerized using Docker for easy deployment and testing.

## Components

### 1. SMTP Server (`serv.py`)

The SMTP server is implemented using the `aiosmtpd` library. It listens for incoming emails and prints the details of each received message, including the sender, recipient, body, and any attachments.

#### Key Features

- **Asynchronous Handling**: Utilizes `asyncio` for handling incoming connections asynchronously.
- **Attachment Handling**: Prints details of any attachments in the received emails.

#### How to Run

1. **Directly with Python**:

    ```bash
    python serv.py
    ```

2. **Using Docker**:

    ```bash
    docker build -t smtp_server .
    docker run -p 1026:1026 smtp_server
    ```

### 2. Email Sender Script (`send_email.py`)

This script sends test emails to the SMTP server. It can be used to verify that the server is functioning correctly.

#### Key Features of the Project

- **Customizable Sender and Recipient**: Easily specify the sender and recipient email addresses.
- **Attachment Support**: Supports sending emails with attachments.

#### How to Run script

1. **Directly with Python**:

    ```bash
    python send_email.py
    ```

2. **Using Docker**:

    ```bash
    docker build -t email_sender -f Dockerfile.send_email .
    docker run email_sender
    ```

### 3. Docker Configuration

Docker is used to containerize both the SMTP server and the email sender script, making it easy to deploy and test the entire setup.

#### Dockerfiles

- **SMTP Server Dockerfile (`Dockerfile`)**:

    ```dockerfile
    FROM python:3.9-slim
    WORKDIR /app
    COPY . .
    RUN pip install -r requirements.txt
    EXPOSE 1026
    CMD ["python", "serv.py"]
    ```

- **Email Sender Dockerfile (`Dockerfile.send_email`)**:

    ```dockerfile
    FROM python:3.11-slim
    WORKDIR /app
    COPY . .
    RUN pip install -r requirements.txt
    CMD ["python", "send_email.py"]
    ```

## Troubleshooting

### Delayed Log Printing

If you notice that the SMTP server prints the email details only after stopping the container, this may be due to buffering issues. To resolve this, you can:

1. **Use Unbuffered Output**: Set the `PYTHONUNBUFFERED` environment variable to `1`.

    ```dockerfile
    ENV PYTHONUNBUFFERED=1
    ```

    or using `-u` parameter on runtime:

    ```Python
    python -u filename.py
    ```

2. **Ensure Logs Are Flushed**: Modify your logging configuration to explicitly flush the logs after each write.

### Viewing Real-Time Logs

To view logs in real-time, you can use the `docker logs` command with the `-f` (follow) flag:

```bash
docker logs -f <container_id>
```

### Using Logging Drivers

Docker supports various logging drivers that can be used to manage container logs more effectively. For more details, refer to the Docker Logging Documentation.

## Conclusion

This project provides a basic yet functional SMTP server setup with Docker, enabling easy deployment and testing. The provided scripts and Docker configurations ensure that you can quickly get the server up and running and send test emails to verify its functionality.

For any issues or contributions, please open an issue or submit a pull request on the project's GitHub repository.

## TODO

Safety first - presented security solutions aren't secure at all. Be carefull deploing this code with `{username:password}` stored as a list.
