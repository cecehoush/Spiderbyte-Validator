import pika
import docker
import os
import uuid  # For generating unique container names
import json
import time

client = docker.from_env()

# Pre-built base Docker image for running user code, speeds up building new containers
BASE_IMAGE = "baseimage"

# execution timeout limit (in seconds)
CONTAINER_TIMEOUT = 10

def print_header(message):
    print("\n" + "=" * 70)
    print(f"### {message.upper()} ###")

def print_divider():
    print("\n" + "-" * 60)

def execute_user_code(user_code, user_id):
    # Generate a unique script file name for each user code
    container_name = f"container_{uuid.uuid4().hex}"
    script_filename = f"script_{container_name}.py"

    print(f"USER: {user_id} | CONTAINER: {container_name}")

    # Write the user code to a script file
    with open(script_filename, "w") as script_file:
        script_file.write(user_code)

    print(f"✅ User script {script_filename} created for user {user_id}.")

    container = None
    try:
        # Run the Docker container using the pre-built base image and mounting the script file
        print(f"🚀 Running Docker container {container_name} for user {user_id}...")
        container = client.containers.run(
            image=BASE_IMAGE,  # Use the pre-built base image
            command="python /code/script.py",  # This will execute the user code
            detach=True,  # Run the container asynchronously (in the background)
            network_mode="none",  # Disable network for security
            mem_limit="512m",  # Limit memory
            cpu_quota=50000,  # Limit CPU usage
            volumes={os.path.abspath(script_filename): {'bind': '/code/script.py', 'mode': 'ro'}},  # Mount user script
        )

        # Wait for the container to finish with a timeout
        start_time = time.time()
        while time.time() - start_time < CONTAINER_TIMEOUT:
            container_status = container.wait(timeout=1)  # Polling every 1 second
            if container_status['StatusCode'] == 0:
                break

        # If the container has not finished within the timeout, kill it
        if time.time() - start_time >= CONTAINER_TIMEOUT:
            print(f"⏰ Timeout reached for user {user_id}. Killing container {container_name}...")
            container.kill()
            output = f"User {user_id}'s code was killed after exceeding the timeout limit of {CONTAINER_TIMEOUT} seconds."
        else:
            output = container.logs().decode('utf-8')

        print_divider()
        print(f"📝 Output from user {user_id}:\n{output}")
        print_divider()

    except docker.errors.ContainerError as e:
        error_message = e.stderr.decode('utf-8')
        print_divider()
        print(f"❌ Error from user {user_id}:\n{error_message}")
        print_divider()
    except Exception as e:
        print_divider()
        print(f"❌ An unexpected error occurred for user {user_id}: {e}")
        print_divider()
    finally:
        # Clean up the container and the temporary user script file
        if container:
            print(f"🧹 Stopping and removing container {container_name} for user {user_id}...")
            container.remove(force=True)  # Remove container, force stop if necessary
        if os.path.exists(script_filename):
            os.remove(script_filename)
        print(f"🧹 Cleaned up resources for user {user_id}.")
        print(f"FINISHED EXECUTION FOR USER: {user_id} | CONTAINER: {container_name}")

def callback(ch, method, properties, body):
    """Callback function to process incoming messages from RabbitMQ"""
    try:
        message = json.loads(body.decode('utf-8'))
        user_code = message['usercode']
        user_id = message['userid']
        print_header(f"RECEIVED CODE TO EXECUTE FOR USER: {user_id}")

        execute_user_code(user_code, user_id)
    except json.JSONDecodeError:
        print("❌ Received an invalid JSON message.")
    except KeyError as e:
        print(f"❌ Missing expected key in JSON message: {e}")
    except Exception as e:
        print(f"❌ An error occurred while processing the message: {e}")
    finally:
        # Acknowledge message after processing
        ch.basic_ack(delivery_tag=method.delivery_tag)

def start_microservice():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare the queue (it will be created if it doesn't exist)
    channel.queue_declare(queue='code_queue')

    # Set up a consumer on the queue
    channel.basic_consume(queue='code_queue', on_message_callback=callback)

    print_header("WAITING FOR MESSAGES. TO EXIT PRESS CTRL+C")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print_header("SHUTTING DOWN...")
        channel.stop_consuming()
    finally:
        connection.close()

if __name__ == "__main__":
    start_microservice()
