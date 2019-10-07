.PHONY: run build

build:
	docker build -t adritify:1.0.0 .

run:
	docker run -it --rm --name adritify-docker adritify:1.0.0

stop:
	@echo "Stopping adritify-docker..."
	docker stop adritify-docker
