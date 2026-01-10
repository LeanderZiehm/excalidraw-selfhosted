docker:
	docker build -t react-vite-nginx . && docker run -p 3000:80 react-vite-nginx