dotenv:
	touch .env


install:
	sudo apt-get update
	sudo apt-get upgrade
	sudo apt install postgresql
	sudo apt-get install python3-pip
	pip3 install pyTelegramBotAPI
	pip3 install python-dotenv
	pip3 install sqlalchemy


run:
	sudo touch kdb.pid
	sudo chmod 777 kdb.pid
	sudo python3 main.py &
	sudo echo $! > kdb.pid

