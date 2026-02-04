


dev:
	set -o allexport && . ./.env && set +o allexport && ./mvnw spring-boot:run -Dspring-boot.run.profiles=dev


run:
	set -o allexport && . ./.env && set +o allexport && ./mvnw spring-boot:run
# 	@set -a && source ./.env && ./mvnw spring-boot:run





# 	export $(cat .env | xargs) 

# docker-run:
# 	docker build -t exalidraw-backend . && docker run exalidraw-backend