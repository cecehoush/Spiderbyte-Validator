import pika
import json

def send_test_message(user_code, user_id):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare the queue (it will be created if it doesn't exist)
    channel.queue_declare(queue='code_queue')

    # Prepare the JSON payload
    payload = {
        "usercode": user_code,
        "userid": user_id
    }

    # Convert the payload to JSON and publish it to the queue
    channel.basic_publish(exchange='',
                          routing_key='code_queue',
                          body=json.dumps(payload))
    print(f"Sent code for user {user_id}")
    connection.close()

if __name__ == "__main__":
    # Example user code submissions
    user_submissions = [
        {"usercode": "print('Hello from user 1!')", "userid": "user1"},
        {"usercode": "x = 10\nprint(x ** 3)", "userid": "user3"},
        {"usercode": "print('Hello from user 1!')", "userid": "user1"},
        {"usercode": "x = 10\nprint(x ** 3)", "userid": "user3"},
        {"usercode": "print('Hello from user 1!')", "userid": "user1"},
        {"usercode": "x = 10\nprint(x ** 3)", "userid": "user3"},
        {"usercode": "print('Hello from user 1!')", "userid": "user1"},
        {"usercode": "x = 10\nprint(x ** 3)", "userid": "user3"},
        {"usercode": "print('Hello from user 1!')", "userid": "user1"},
        {"usercode": "x = 10\nprint(x ** 3)", "userid": "user3"},
        {"usercode": "print('Hello from user 1!')", "userid": "user1"},
        {"usercode": "x = 10\nprint(x ** 3)", "userid": "user3"},
        {"usercode": "print('Hello from user 1!')", "userid": "user1"},
        {"usercode": "x = 10\nprint(x ** 3)", "userid": "user3"},
        {"usercode": "print('Hello from user 1!')", "userid": "user1"},
        {"usercode": "x = 10\nprint(x ** 3)", "userid": "user3"},
        {"usercode": "print('Hello from user 1!')", "userid": "user1"},
        {"usercode": "x = 10\nprint(x ** 3)", "userid": "user3"},
        {"usercode": "print('Hello from user 1!')", "userid": "user1"},
        {"usercode": "x = 10\nprint(x ** 3)", "userid": "user3"},
        {"usercode": "print('Hello from user 1!')", "userid": "user1"},
        {"usercode": "x = 10\nprint(x ** 3)", "userid": "user3"},
        {"usercode": "print('Hello from user 1!')", "userid": "user1"},
        {"usercode": "x = 10\nprint(x ** 3)", "userid": "user3"},
        {"usercode": "print('Hello from user 1!')", "userid": "user1"},
        {"usercode": "x = 10\nprint(x ** 3)", "userid": "user3"},
        {"usercode": "print('Hello from user 1!')", "userid": "user1"},
        {"usercode": "x = 10\nprint(x ** 3)", "userid": "user3"},
        {"usercode": "print('Hello from user 1!')", "userid": "user1"},
        {"usercode": "x = 10\nprint(x ** 3)", "userid": "user3"},
        {"usercode": "print('Hello from user 1!')", "userid": "user1"},
        {"usercode": "x = 10\nprint(x ** 3)", "userid": "user3"},
        {"usercode": "print('Hello from user 1!')", "userid": "user1"},
        {"usercode": "x = 10\nprint(x ** 3)", "userid": "user3"},
        {"usercode": "while(1 == 1):\n    print('Hello from user 2!')", "userid": "user2"},
        {"usercode": "print('Hello from user 1!')", "userid": "user1"},
        {"usercode": "x = 10\nprint(x ** 3)", "userid": "user3"},
        {"usercode": "print('Hello from user 1!')", "userid": "user1"},
        {"usercode": "x = 10\nprint(x ** 3)", "userid": "user3"},
        {"usercode": "print('Hello from user 1!')", "userid": "user1"},
        {"usercode": "x = 10\nprint(x ** 3)", "userid": "user3"},
        {"usercode": "print('Hello from user 1!')", "userid": "user1"},
        {"usercode": "x = 10\nprint(x ** 3)", "userid": "user3"},
        {"usercode": "print('Hello from user 1!')", "userid": "user1"},
        {"usercode": "x = 10\nprint(x ** 3)", "userid": "user3"},
        {"usercode": "print('Hello from user 1!')", "userid": "user1"},
        {"usercode": "x = 10\nprint(x ** 3)", "userid": "user3"},
        {"usercode": "print('Hello from user 1!')", "userid": "user1"},
        {"usercode": "x = 10\nprint(x ** 3)", "userid": "user3"},
        {"usercode": "print('Hello from user 1!')", "userid": "user1"},
        {"usercode": "x = 10\nprint(x ** 3)", "userid": "user3"},
        {"usercode": "print('Hello from user 1!')", "userid": "user1"},
        {"usercode": "x = 10\nprint(x ** 3)", "userid": "user3"},
        {"usercode": "print('Hello from user 1!')", "userid": "user1"},
        {"usercode": "x = 10\nprint(x ** 3)", "userid": "user3"},
        {"usercode": "print('Hello from user 1!')", "userid": "user1"},
        {"usercode": "x = 10\nprint(x ** 3)", "userid": "user3"},
        {"usercode": "print('Hello from user 1!')", "userid": "user1"},
        {"usercode": "x = 10\nprint(x ** 3)", "userid": "user3"},
        {"usercode": "print('Hello from user 1!')", "userid": "user1"},
        {"usercode": "x = 10\nprint(x ** 3)", "userid": "user3"},
        {"usercode": "print('Hello from user 1!')", "userid": "user1"},
        {"usercode": "x = 10\nprint(x ** 3)", "userid": "user3"},
        {"usercode": "print('Hello from user 1!')", "userid": "user1"},
        {"usercode": "x = 10\nprint(x ** 3)", "userid": "user3"},
        {"usercode": "print('Hello from user 1!')", "userid": "user1"},
        {"usercode": "x = 10\nprint(x ** 3)", "userid": "user3"},
        {"usercode": "print('Hello from user 1!')", "userid": "user1"},
        {"usercode": "x = 10\nprint(x ** 3)", "userid": "user3"},
        {"usercode": "while(1 == 1):\n    print('Hello from user 2!')", "userid": "user2"},
    ]

    for submission in user_submissions:
        send_test_message(submission["usercode"], submission["userid"])
