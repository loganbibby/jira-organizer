docker_build:
	docker-compose build

docker_run:
	docker-compose up -d

docker_stop:
	docker-compose stop

docker_rebuild: docker_stop docker_build docker_run

run:
	flask --app jira_organizer:app run

debug:
	flask --app jira_organizer:app --debug run
