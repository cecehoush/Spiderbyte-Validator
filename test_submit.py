import pika

def send_test_message(user_code):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare the queue (it will be created if it doesn't exist)
    channel.queue_declare(queue='code_queue')

    # Publish the user code to the queue
    channel.basic_publish(exchange='',
                          routing_key='code_queue',
                          body=user_code)
    print(f"Sent code: {user_code}")
    connection.close()

if __name__ == "__main__":
    # Example user code submissions
    user_codes = [
        "print('Hello from user 1!')",
        "print('Hello from user 2!')",
        "x = 10\nprint(x ** 3)",
        "print('Hello from user 1!')",
        "print('Hello from user 2!')",
        "x = 10\nprint(x ** 3)",
        "print('Hello from user 1!')",
        "print('Hello from user 2!')",
        "x = 10\nprint(x ** 3)",
        "print('Hello from user 1!')",
        "print('Hello from user 2!')",
        "x = 10\nprint(x ** 3)",
        "print('Hello from user 1!')",
        "print('Hello from user 2!')",
        "x = 10\nprint(x ** 3)",
        "print('Hello from user 1!')",
        "print('Hello from user 2!')",
        "x = 10\nprint(x ** 3)",
        "print('Hello from user 1!')",
        "print('Hello from user 2!')",
        "x = 10\nprint(x ** 3)",
        "print('Hello from user 1!')",
        "print('Hello from user 2!')",
        "x = 10\nprint(x ** 3)",
        "print('Hello from user 1!')",
        "print('Hello from user 2!')",
        "x = 10\nprint(x ** 3)",
        "print('Hello from user 1!')",
        "print('Hello from user 2!')",
        "x = 10\nprint(x ** 3)",
        "print('Hello from user 1!')",
        "print('Hello from user 2!')",
        "x = 10\nprint(x ** 3)",
        "print('Hello from user 1!')",
        "print('Hello from user 2!')",
        "x = 10\nprint(x ** 3)",
        "print('Hello from user 1!')",
        "print('Hello from user 2!')",
        "x = 10\nprint(x ** 3)",
        "print('Hello from user 1!')",
        "print('Hello from user 2!')",
        "x = 10\nprint(x ** 3)",
        "print('Hello from user 1!')",
        "print('Hello from user 2!')",
        "x = 10\nprint(x ** 3)",
        "print('Hello from user 1!')",
        "print('Hello from user 2!')",
        "x = 10\nprint(x ** 3)",
        "print('Hello from user 1!')",
        "print('Hello from user 2!')",
        "x = 10\nprint(x ** 3)",
        "print('Hello from user 1!')",
        "print('Hello from user 2!')"
    ]

    for code in user_codes:
        send_test_message(code)
