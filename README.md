# Introduction 
This is the Implementation JWT in FastAPI app using fastapi-jwt-auth

##  :beginner: About
This is a simple API using FastAPI for managing user's links. A postgreSQL database was used for persistence via an Asyncpg. The primary objective of this repo is to help beginners learn and use JWT replace query on database.

## :zap: Usage
###  :electric_plug: Installation
- Clone the Github repository 
- Change Postgres settings in `.env` file
- Change env file in config directory
- For change KEY_TOKEN in `config/.env` file using `Cryptography` lib
- Create new authentication key use <ssh-keygen> in jwt_token directory
- Run below Command 
```bash
$ docker-compose up --build
```

###  :zap: Run the app 
> The application and Documentation can be accessed on http://localhost:8080
