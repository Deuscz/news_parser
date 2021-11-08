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
	sudo echo "" > .git/hooks/pre-commit
	sudo echo "#/bin/sh" >> .git/hooks/pre-commit
	sudo echo "sudo black ." >> .git/hooks/pre-commit
	sudo echo "sudo python3 lint.py -p ./web/ -t 5" >> .git/hooks/pre-commit
	sudo chmod +x .git/hooks/pre-commit