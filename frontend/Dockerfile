FROM node:18-alpine AS base

WORKDIR /usr/src/app

# Install dependencies first for caching
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install --no-audit --no-fund

# Copy app (for production builds). In dev we will mount source.
COPY frontend ./

EXPOSE 3000

# Start dev server
CMD ["npm", "start"]
