# Stage 1: Runtime
FROM nginxinc/nginx-unprivileged:alpine

# Remove default nginx static assets
RUN rm -rf /usr/share/nginx/html/*

# Copy static UI files (index.html, css, js)
COPY ui/ /usr/share/nginx/html

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 8080 (Unprivileged Nginx uses 8080 by default)
EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]