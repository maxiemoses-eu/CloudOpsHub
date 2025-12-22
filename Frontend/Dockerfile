# Dockerfile.ui
# Use a multi-stage build: First, build the application (e.g., npm run build), 
# then serve the result using a light web server (Nginx).

# Stage 1: Build Stage (If using React/Vue)
# FROM node:18 as builder
# WORKDIR /app
# COPY package.json .
# RUN npm install
# COPY . .
# RUN npm run build

# Stage 2: Production Serving Stage
FROM nginx:alpine

# Copy the built static assets from the builder stage (or just copy placeholder files)
# COPY --from=builder /app/build /usr/share/nginx/html
COPY ui/ /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose the standard HTTP port
EXPOSE 80

# Nginx starts automatically
CMD ["nginx", "-g", "daemon off;"]
