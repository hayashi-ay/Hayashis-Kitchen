FROM node:12.16.1-alpine

# make the 'app' folder the current working directory
WORKDIR /app

# first copy both package.json and package-lock.json to take advantage of cached Docker layer
# the detail is http://bitjudo.com/blog/2014/03/13/building-efficient-dockerfiles-node-dot-js/
COPY package*.json ./

# install project dependencies
RUN npm install

# copy project files and folders to the current working directory
COPY . .

CMD [ "npm", "run", "serve" ]
