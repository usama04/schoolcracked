# Base image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install --production

# Copy the application code
COPY public public
COPY src src

# Build the application
RUN npm run build

# Expose port 3000 for the frontend
EXPOSE 3000

# Start the application
CMD ["npm", "start"]