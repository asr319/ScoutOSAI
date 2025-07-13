<!-- @format -->

# ScoutOSAI

## Setup

`docker-compose.yml` expects the database password in the `POSTGRES_PASSWORD`
environment variable. Set the variable before starting the stack:

```bash
export POSTGRES_PASSWORD=yourpassword
docker-compose up
```

The backend service uses this value when constructing `DATABASE_URL`.
