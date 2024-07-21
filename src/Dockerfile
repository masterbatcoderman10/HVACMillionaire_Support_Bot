# Use an official lightweight Nginx image
FROM nginx:alpine

# Set the working directory in the container
WORKDIR /usr/share/nginx/html

# Remove the default nginx index page
RUN rm -rf ./*

# Copy the base.html into the container at /usr/share/nginx/html
COPY base.html .

# Copy the styles, scripts, and assets directories into the container
COPY styles styles/
COPY scripts scripts/
COPY assets assets/

# Expose port 5500
EXPOSE 5500

# Start Nginx and keep it running in the foreground
CMD ["nginx", "-g", "daemon off;"]