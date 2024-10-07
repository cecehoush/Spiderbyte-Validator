To Run:

MAKE A VENV
INSTALL ALL REQUIREMENTS
pip install -r requirements.txt

Open Docker Desktop
docker start rabbitmq
python manager.py
python test_submit.py in different terminal

You can go to http://localhost:15672/ to see the queue working
Username and password are 'guest'