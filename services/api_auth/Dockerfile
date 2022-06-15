FROM node:16

ENV API_AUTH_HOST="0.0.0.0"
ENV API_AUTH_PORT="8000"
ENV API_AUTH_JWT_SECRET="q@M&P8gXLJrh47&d"
ENV API_DB_HOST="0.0.0.0"
ENV API_DB_USER="sifu"
ENV API_DB_PASSWORD="sifu"
ENV API_DB_DATABASE="dojo"
ENV API_DB_CONNECTION_LIMIT=10

# Create app directory
WORKDIR /usr/src/app

# Install app dependencies
# A wildcard is used to ensure both package.json AND package-lock.json are copied
# where available (npm@5+)
COPY package*.json ./

RUN npm install
# If you are building your code for production
# RUN npm ci --only=production

# Bundle app source
COPY . .

EXPOSE 8000
CMD [ "npm", "start" ]
