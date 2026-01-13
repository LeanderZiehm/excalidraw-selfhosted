# Stage 1: Build the React app
FROM node:20-alpine AS builder

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json* ./
RUN npm ci

COPY vite.config.ts ./
COPY tsconfig.json tsconfig.app.json tsconfig.node.json ./
COPY src ./src
COPY public ./public

COPY index.html ./index.html


RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:stable-alpine

# Remove default Nginx static files
RUN rm -rf /usr/share/nginx/html/*

# Copy built files from builder
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom Nginx config
COPY devops/nginx/default.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
