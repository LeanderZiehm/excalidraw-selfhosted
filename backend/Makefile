


dev:
	set -o allexport && . ./.env && set +o allexport && ./mvnw spring-boot:run -Dspring-boot.run.profiles=dev


run:
	set -o allexport && . ./.env && set +o allexport && ./mvnw spring-boot:run

docker-run:
	docker build -t excalidraw-selfhosted . && docker rm -f excalidraw-selfhosted 2>/dev/null || true && docker run --env-file .env -p 8800:8800 --name excalidraw-selfhosted excalidraw-selfhosted

podman-run:
	podman build -t excalidraw-selfhosted . && podman rm -f excalidraw-selfhosted 2>/dev/null || true && podman run --env-file .env -p 8800:8800 --name excalidraw-selfhosted excalidraw-selfhosted -d

docker-compose:
	docker compose -f docker-compose.no-db.yml up 

podman-compose:
	podman-compose -f docker-compose.no-db.yml up -d


# 	@set -a && source ./.env && ./mvnw spring-boot:run





# 	export $(cat .env | xargs) 

# docker-run:
# 	docker build -t exalidraw-backend . && docker run exalidraw-backend