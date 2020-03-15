# Hayashis-Kitchen
## Overview
Welcome to Hayashi's Kitchen project.  
This is a kind of a reservation management system for my dinning table.

The backend is deployed on Heroku and you can see it by accesssing http://hayashis-kitchen-api.herokuapp.com/.  
The frontend is currently under construction, but it will be soon hosted on Heroku.

## Getting Started
The system is containerized by Docker and you need to run following command to start with

```
# build images
docker-compose build

# run images
docker-compose up -d
```

Then, you can see both backend and frontend on following urls

 - backend: http://0.0.0.0:8081/
 - frontend: http://0.0.0.0:3001/

At the very first run, tables are not yet created on postgresql, so you need to run `flask db_drop_and_create_all`.

## API Document
APIs are documented with Swagger UI and available at http://hayashis-kitchen-api.herokuapp.com/ - You can also test APIs there.

### RBAC
Note: this section will be transition to the swagger documentaion in the future.  

The system has two roles:
 - Owner  
 It's me. I am the owner of Hayashi's Kitchen and I can do every action.
 - User  
 User is guests of my dinner table. They can book slots and see slot information.

## Deployment
Before running the following command, you need to ensure that you're successfuly loged in to both `docker` and `heroku`.

```
docker tag <docker_image_id> registry.heroku.com/hayashis-kitchen-api/web
docker push registry.heroku.com/hayashis-kitchen-api/web
heroku container:release web --app=hayashis-kitchen-api
```
