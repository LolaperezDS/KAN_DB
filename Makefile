list:
	docker images
	docker ps -a

stop:
	docker-compose stop

up:
	docker-compose -f docker-compose.yml up

remove_containers:
	docker-compose rm

clear_db:
	sudo rm -rf pgdata/

rm: stop remove_containers clear_db

rebuild: remove_containers
	docker-compose -f docker-compose.yml up --force-recreate --build

recreate: rm rebuild
