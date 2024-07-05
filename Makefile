dotenv:
	sudo touch .env
	sudo chmod 777 .env


install:
	sudo apt-get update
	sudo apt-get upgrade
	sudo apt install postgresql
	sudo apt-get install python3-pip
	pip3 install pyTelegramBotAPI
	pip3 install python-dotenv
	pip3 install sqlalchemy
	pip install asyncpg


run:
	sudo python3 api/main.py &
	sudo echo $! > kdb.pid

