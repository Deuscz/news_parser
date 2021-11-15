run:
	sudo docker-compose up


rund:
	sudo docker-compose up -d

build:
	sudo docker-compose up -d
	sudo chmod -R a+w pgadmin
	sudo chmod -R a+w rabbitmq


ls:
	sudo docker container ls -a
	sudo docker image ls -a

recreate:
	sudo docker rmi news_parser_web -f
	sudo docker-compose build


clear:
	sudo docker-compose down


stop:
	sudo docker-compose stop


connect:
	sudo docker exec -it flask_app bash


set_hook:
	sudo pip install black pylint
	sudo echo "" > .git/hooks/pre-commit
	sudo echo "#/bin/sh" >> .git/hooks/pre-commit
	sudo echo "sudo black ." >> .git/hooks/pre-commit
	sudo echo "sudo python3 lint.py -p ./web/ -t 5" >> .git/hooks/pre-commit
	sudo chmod +x .git/hooks/pre-commit

create_db:
	sudo docker exec -it flask_app python3 manage.py create_db


load_init_db:
	sudo docker exec -it flask_app python3 manage.py load_init_db

run_parse:
	sudo docker exec -it flask_app python3 manage.py run_parse


test_empty: create_db load_init_db
	sudo docker exec -it flask_app pytest parser/tests.py -v -m empty

test_not_empty: run_parse
	sudo sleep 5
	sudo docker exec -it flask_app pytest parser/tests.py -v -m "not empty"

test: test_empty test_not_empty

file_access:
	sudo chmod -R a+w web