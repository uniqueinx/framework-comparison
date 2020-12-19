setup-test:
	docker pull loadimpact/k6

server-fastapi:
	docker-compose -f test-fastapi/docker-compose.yml up --build

server-flask:
	docker-compose -f test-flask/docker-compose.yml up --build

bench:
	docker run --network host  -i loadimpact/k6 run - < k6.js