# ---------- build stage ----------
FROM eclipse-temurin:25-jdk AS build

WORKDIR /app

# copy wrapper and pom first (better caching)
COPY mvnw .
COPY .mvn .mvn
COPY pom.xml .

RUN chmod +x mvnw
RUN ./mvnw -B -q dependency:go-offline

# copy sources and build
COPY src src
RUN ./mvnw -B clean package -DskipTests

# ---------- runtime stage ----------
FROM eclipse-temurin:25-jre

WORKDIR /app

COPY --from=build /app/target/*.jar app.jar

ENTRYPOINT ["java", "-jar", "app.jar"]
