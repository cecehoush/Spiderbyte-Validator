import pika
import json



def send_test_message(user_code, user_id, test_cases):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Prepare the JSON payload
    payload = {
        "usercode": user_code,
        "userid": user_id,
        "test_cases": test_cases
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
    {
        "userid": "user1",
        "usercode": "def multiply(x, y):\n    while(1==1):\n        k = 3+3\n    return x * y\nmultiply(input1, input2)",
        "test_cases": [
            {
                "inputs": ["3", "5"],
                "expected_output": "15"
            },
            {
                "inputs": ["7", "8"],
                "expected_output": "56"
            }
        ]
    },
    {
        "userid": "user1",
        "usercode": "def multiply(x, y):\n    return x * y\nmultiply(input1, input2)",
        "test_cases": [
            {
                "inputs": ["3", "5"],
                "expected_output": "15"
            },
            {
                "inputs": ["7", "8"],
                "expected_output": "56"
            }
        ]
    },
    {
        "userid": "user1",
        "usercode": "def two_sum(nums, target):\n    for i in range(len(nums)):\n        for j in range(i + 1, len(nums)):\n            if nums[i] + nums[j] == target:\n                return [i, j]\ntwo_sum(input1, input2)",
        "test_cases": [
            {
                "inputs": ["[2, 7, 11, 15]", "9"],
                "expected_output": "[0, 1]"
            },
            {
                "inputs": ["[3, 2, 4]", "6"],
                "expected_output": "[1, 2]"
            },
            {
                "inputs": ["[3, 3]", "6"],
                "expected_output": "[0, 1]"
            },
            {
                "inputs": ["[1, 2, 3, 4, 5]", "9"],
                "expected_output": "[3, 4]"
            }
        ]
    },
    {
        "userid": "user2",
        "usercode": "def is_palindrome(s):\n    if len(s) <= 1:\n        return True\n    elif s[0] != s[-1]:\n        return False\n    else:\n        return is_palindrome(s[1:-1])\nis_palindrome(input1)",
        "test_cases": [
            {
                "inputs": ["'racecar'"],
                "expected_output": "True"
            },
            {
                "inputs": ["'hello'"],
                "expected_output": "False"
            },
            {
                "inputs": ["'madam'"],
                "expected_output": "True"
            },
            {
                "inputs": ["'a'"],
                "expected_output": "True"
            },
            {
                "inputs": ["''"],
                "expected_output": "True"
            }
        ]
    },
    {
        "userid": "user3",
        "usercode": "def length_of_longest_substring(s):\n    char_map = {}\n    left = 0\n    max_length = 0\n    for right in range(len(s)):\n        if s[right] in char_map:\n            left = max(left, char_map[s[right]] + 1)\n        char_map[s[right]] = right\n        max_length = max(max_length, right - left + 1)\n    return max_length\nlength_of_longest_substring(input1)",
        "test_cases": [
            {
                "inputs": ["'abcabcbb'"],
                "expected_output": "3"
            },
            {
                "inputs": ["'bbbbb'"],
                "expected_output": "1"
            },
            {
                "inputs": ["'pwwkew'"],
                "expected_output": "3"
            },
            {
                "inputs": ["'dvdf'"],
                "expected_output": "3"
            },
            {
                "inputs": ["'anviaj'"],
                "expected_output": "5"
            },
            {
                "inputs": ["''"],
                "expected_output": "0"
            },
            {
                "inputs": ["'a'"],
                "expected_output": "1"
            }
        ]
    },
    {
        "userid": "user4",
        "usercode": "def word_break(s, wordDict):\n    dp = [False] * (len(s) + 1)\n    dp[0] = True\n    word_set = set(wordDict)\n    for i in range(1, len(s) + 1):\n        for j in range(i):\n            if dp[j] and s[j:i] in word_set:\n                dp[i] = True\n                break\n    return dp[len(s)]\nword_break(input1, input2)",
        "test_cases": [
            {
                "inputs": ["'leetcode'", "['leet', 'code']"],
                "expected_output": "True"
            },
            {
                "inputs": ["'applepenapple'", "['apple', 'pen']"],
                "expected_output": "True"
            },
            {
                "inputs": ["'catsandog'", "['cats', 'dog', 'sand', 'and', 'cat']"],
                "expected_output": "False"
            },
            {
                "inputs": ["'pineapplepenapple'", "['apple', 'pen', 'pine', 'pineapple']"],
                "expected_output": "True"
            },
            {
                "inputs": ["'catsanddogs'", "['cats', 'cat', 'and', 'dogs']"],
                "expected_output": "True"
            },
            {
                "inputs": ["'aaaaaaa'", "['aaa', 'aaaa']"],
                "expected_output": "False"
            },
            {
                "inputs": ["''", "['a', 'b', 'c']"],
                "expected_output": "True"
            }
        ]
    },
    {
        "userid": "user6",
        "usercode": "def findMedianSortedArrays(nums1, nums2):\n    merged = nums1 + nums2\n    merged.sort()\n    length = len(merged)\n    if length % 2 == 1:\n        return merged[length // 2]\n    else:\n        return (merged[length // 2 - 1] + merged[length // 2]) / 2\nfindMedianSortedArrays(input1, input2)",
        "test_cases": [
            {
                "inputs": ["[1,3]", "[2]"],
                "expected_output": "2"
            },
            {
                "inputs": ["[1,2]", "[3,4]"],
                "expected_output": "2.5"
            },
            {
                "inputs": ["[0,0]", "[0,0]"],
                "expected_output": "0.0"
            },
            {
                "inputs": ["[]", "[1]"],
                "expected_output": "1"
            },
            {
                "inputs": ["[2]", "[]"],
                "expected_output": "2"
            }
        ]
    }
]
    for submission in user_submissions:
        send_test_message(submission["usercode"], submission["userid"], submission["test_cases"])
