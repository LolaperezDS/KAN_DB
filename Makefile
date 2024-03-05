dotenv:
	touch .env
	echo "IS_PRODUCTION_MODE=1" > .env
	echo "TELEGRAM_BOT_TOKEN=" > .env
	echo "DB_HOST=" > .env
	echo "DB_PORT=" > .env
	echo "DB_NAME=" > .env
	echo "DB_USER=" > .env
	echo "DB_PASS=" > .env


install:
	sudo apt-get update
	sudo apt-get upgrade
	sudo apt install postgresql
	sudo apt-get install python3-pip
	pip3 install pyTelegramBotAPI
	pip3 install dotenv
	pip3 install sqlalchemy


run:
	python3 main.py
