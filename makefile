run:
	sudo docker-compose up -d
	sudo chmod -R a+w pgadmin
	sudo chmod -R a+w rabbitmq


stop:
	sudo docker-compose stop


connect:
	sudo docker exec -it flask_app bash


set_hook:
	sudo pip install black pylint
