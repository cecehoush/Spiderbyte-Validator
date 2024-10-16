import pika
import docker
import os
import uuid  # For generating unique container names if needed

# Docker client setup
client = docker.from_env()

# Pre-built base Docker image
BASE_IMAGE = "baseimage"

def execute_user_code(user_code, container_name):
    # Generate a unique script file name for each user code
    script_filename = f"script_{container_name}.py"

    # Write the user code to a script file
    with open(script_filename, "w") as script_file:
        script_file.write(user_code)

    print(f"User script {script_filename} created.")

    try:
        # Run the Docker container using the pre-built base image and mounting the script file
        print(f"Running Docker container for {container_name}...")
        container = client.containers.run(
            image=BASE_IMAGE,  # Use the pre-built base image
            command="python /code/script.py",  # This will execute the user code
            detach=False,  # Run the container synchronously
            network_mode="none",  # Disable network for security
            mem_limit="512m",  # Limit memory
            cpu_quota=50000,  # Limit CPU usage
            volumes={os.path.abspath(script_filename): {'bind': '/code/script.py', 'mode': 'ro'}},  # Mount user script
            remove=True  # Automatically remove the container after it finishes
        )
        print(f"Output from {container_name}: {container.decode('utf-8')}")
    except docker.errors.ContainerError as e:
        print(f"Error from {container_name}: {e.stderr.decode('utf-8')}")
    finally:
        # Clean up the temporary user script file
        if os.path.exists(script_filename):
            os.remove(script_filename)

def callback(ch, method, properties, body):
    """Callback function to process incoming messages from RabbitMQ"""
    user_code = body.decode('utf-8')
    container_name = f"user_{method.delivery_tag}"
    print(f"Received code to execute: {user_code}")
    execute_user_code(user_code, container_name)
    # Acknowledge message after processing
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_microservice():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare the queue (it will be created if it doesn't exist)
    channel.queue_declare(queue='code_queue')

    # Set up a consumer on the queue
    channel.basic_consume(queue='code_queue', on_message_callback=callback)

    print("Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    start_microservice()
