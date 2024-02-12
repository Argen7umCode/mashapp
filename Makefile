up: 
	sudo docker compose -f docker-compose-local.yaml up -d

down:
	sudo docker compose -f docker-compose-local.yaml down && sudo docker network prune --force