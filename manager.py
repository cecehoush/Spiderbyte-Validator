import pika
import docker
import os

# Docker client setup
client = docker.from_env()

def execute_user_code(user_code, container_name):
    script_filename = f"script_{container_name}.py"
    dockerfile_name = f"Dockerfile_{container_name}"

    with open(script_filename, "w") as script_file:
        script_file.write(user_code)

    dockerfile_content = f"""
    FROM python:3.10-alpine
    RUN mkdir /code
    WORKDIR /code
    COPY {script_filename} /code/script.py
    """

    with open(dockerfile_name, "w") as dockerfile:
        dockerfile.write(dockerfile_content)

    try:
        image, _ = client.images.build(
            path=".",
            dockerfile=dockerfile_name,
            tag=f"user_code_image_{container_name}",
            rm=True,
        )
    except docker.errors.BuildError as e:
        print(f"Build Error for {container_name}: {str(e)}")
        return

    try:
        result = client.containers.run(
            image=f"user_code_image_{container_name}",
            command="python script.py",
            remove=True,
            network_mode="none",
            mem_limit="512m",
            cpu_quota=50000
        )
        print(f"Output from {container_name}: {result.decode('utf-8')}")
    except docker.errors.ContainerError as e:
        print(f"Error from {container_name}: {e.stderr.decode('utf-8')}")
    finally:
        if os.path.exists(script_filename):
            os.remove(script_filename)
        if os.path.exists(dockerfile_name):
            os.remove(dockerfile_name)

def callback(ch, method, properties, body):
    """Callback function to process incoming messages from RabbitMQ"""
    user_code = body.decode('utf-8')
    container_name = f"user_{method.delivery_tag}"
    print(f"Received code to execute: {user_code}")
    execute_user_code(user_code, container_name)
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
