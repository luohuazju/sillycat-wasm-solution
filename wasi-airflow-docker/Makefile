IMAGE=sillycat/public
TAG=sillycat-airflow-2.0
NAME=sillycat-airflow-2.0


docker-context:

build: docker-context
	docker build  -t $(IMAGE):$(TAG) .

run:
	docker run -d -p 9090:8080 --name $(NAME) $(IMAGE):$(TAG)

clean:
	docker stop ${NAME}
	docker rm ${NAME}