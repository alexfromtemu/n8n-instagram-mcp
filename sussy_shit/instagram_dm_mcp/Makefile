.PHONY: build run stop logs clean help

# Default target
help:
	@echo "Instagram DM MCP Server - Docker Commands"
	@echo ""
	@echo "Available commands:"
	@echo "  make build    - Build the Docker image"
	@echo "  make run      - Start the container using docker-compose"
	@echo "  make stop     - Stop the container"
	@echo "  make logs     - View container logs"
	@echo "  make clean    - Remove container and volumes"
	@echo "  make shell     - Open a shell in the running container"
	@echo ""

build:
	docker-compose build

run:
	@mkdir -p sessions downloads
	docker-compose up -d
	@echo "Container started. Use 'make logs' to view logs."

stop:
	docker-compose down

logs:
	docker-compose logs -f

clean:
	docker-compose down -v
	docker rmi instagram-dm-mcp 2>/dev/null || true
	@echo "Cleaned up containers and images"

shell:
	docker exec -it instagram-dm-mcp /bin/bash

rebuild:
	docker-compose build --no-cache
	@echo "Image rebuilt. Use 'make run' to start."

