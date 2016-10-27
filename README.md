# cg-export-db

## Pre-Requisites
* `cf-download` Plugin


## Usage
```sh
# install cf-download if it was not downloaded before
cf install-plugin cf-download -r CF-Community

# Start and bind the database to your app.
cf push --no-start && cf bind-service export-db YOUR_SERVICE_NAME_HERE && cf start export-db

cf download export-db

# The file should be downloaded
ls export-db/app/db.sql
```

## Common Use Cases
### [wip] Migrating From EW to GovCloud
```sh
# Login into EW cloud.go
cf api https://api.cloud.gov
cf login --sso

# Go to your org and space

# clone this repo to your computer
git clone

# Start and bind the database to your app.
cf push --no-start && cf bind-service export-db YOUR_SERVICE_NAME_HERE && cf start export-db

# Download your backup
cf download export-db && ls export-db/app/db.sql

# Login into EW cloud.go
cf api https://api.fr.cloud.gov
cf login --sso

# TODO add documentation either
# 1) set a variable inside the downloaded droplet to make it restore instead of download a dump
# 2) create a separate app that handles the restore


```
