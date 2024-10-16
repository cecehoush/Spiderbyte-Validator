
---

# **Project Setup Guide**

This guide explains how to set up and run the project, including managing Python dependencies, setting up RabbitMQ with Docker, and executing the RabbitMQ consumer and producer scripts.

## **Prerequisites**

Before you begin, ensure you have the following installed on your system:

1. **Python** (3.8+)
2. **Docker Desktop**

## **Step-by-Step Instructions**

### **1. Set Up the Virtual Environment**

It is recommended to create a virtual environment for managing Python dependencies:

1. Open your terminal or command prompt.
2. Navigate to the root directory of the project.
3. Create a virtual environment by running the following command:

   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:
   - **On Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **On macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

### **2. Install Python Dependencies**

After activating the virtual environment, install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

This will install all necessary packages, including the `pika` library (RabbitMQ client) and Docker dependencies.

### **3. Set Up Docker**

#### **A. Open Docker Desktop**

Ensure Docker Desktop is running. You can verify it's running by checking the system tray (Docker logo) or using the following command in your terminal:

```bash
docker info
```

#### **B. Build the Base Docker Image**

This project uses Docker containers to execute user-submitted code. To do this efficiently, you'll need to build a base image (only needs to be done once):

```bash
docker build -t baseimage .
```

This command will build the Docker image from the provided `Dockerfile` located in the project root directory.

#### **C. Set Up RabbitMQ with Docker**

1. Pull the official RabbitMQ image (only needs to be done once):

   ```bash
   docker pull rabbitmq
   ```

2. Run RabbitMQ in a Docker container:

   ```bash
   docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq
   ```

   This command starts RabbitMQ in a Docker container, mapping:
   - Port `5672` for communication between your Python scripts and RabbitMQ.
   - Port `15672` for accessing the RabbitMQ Management Dashboard.

#### **D. Start RabbitMQ (If Stopped)**

If the RabbitMQ container is stopped, you can start it again with:

```bash
docker start rabbitmq
```

### **4. Run the Project**

#### **A. Run the RabbitMQ Manager**

The `manager.py` script listens for messages from RabbitMQ and runs user-submitted Python code inside a Docker container. Open a terminal and run:

```bash
python manager.py
```

#### **B. Submit Code via RabbitMQ**

Open a new terminal (while keeping `manager.py` running) and run the `test_submit.py` script to send user code to the RabbitMQ queue:

```bash
python test_submit.py
```

This script sends predefined Python code snippets to RabbitMQ, which will be picked up by the `manager.py` script.

### **5. Monitor the RabbitMQ Queue**

RabbitMQ provides a web-based management dashboard for monitoring queues, exchanges, and messages. To access the dashboard:

1. Open your browser and go to:
   ```
   http://localhost:15672
   ```

2. Log in with the default credentials:
   - **Username**: `guest`
   - **Password**: `guest`

From here, you can monitor the `code_queue` and see messages being processed by the manager.

### **6. Stopping the Services**

- **Stop the Manager**: To stop the `manager.py` script, press `Ctrl + C` in the terminal where it's running.
- **Stop RabbitMQ**: You can stop the RabbitMQ container if needed by running:

  ```bash
  docker stop rabbitmq
  ```

## **Summary of Commands**

1. **Create and activate the virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Or `venv\Scripts\activate` on Windows
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Build the Docker base image**:
   ```bash
   docker build -t baseimage .
   ```

4. **Set up RabbitMQ**:
   ```bash
   docker pull rabbitmq
   docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq
   ```

5. **Start the RabbitMQ container** (if stopped):
   ```bash
   docker start rabbitmq
   ```

6. **Run the manager**:
   ```bash
   python manager.py
   ```

7. **Submit code to RabbitMQ**:
   ```bash
   python test_submit.py
   ```

8. **Access the RabbitMQ Management Dashboard**:
   ```
   http://localhost:15672
   ```

---

### **Troubleshooting**

- **RabbitMQ not starting**: Ensure that Docker Desktop is running. Use `docker ps` to check that the RabbitMQ container is active.
- **Cannot access RabbitMQ management dashboard**: Verify that port `15672` is correctly mapped. Restart the container if needed using `docker start rabbitmq`.
- **Dependency Issues**: If there are issues installing dependencies, ensure your virtual environment is activated and try running `pip install -r requirements.txt` again.

---
