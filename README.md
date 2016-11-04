# cg-export-db

`cg-export-db` is a Cloud Foundry CLI Plugin for migrating the data of services.

## Pre-Reqs
### Supported Services
You **MUST** use one of these services in order to use this plugin to
dump/restore backups. The list of services is:
- AWS-RDS/MySQL
- AWS-RDS/Postgres(PSQL)

#### Supported Storage
You **MUST** be able to create one of these services in order to stream the backup.
The list of the services that can store the data is:
- S3

## Commands
There are five commands:

1. `cf export-data` - Interactively creates an application, binds to your
 service, streams the data from your service to a S3 bucket.
1. `cf import-data` - Interactively creates an application, binds to your
 new service, streams the data from the S3 bucket to the new service.
1. `cf download-backup-data` - Interactively selects the backup data from an
 existing exported data dump (must run `cf export-data` first) and downloads it
 locally to your computer.
1. `cf upload-backup-data [file]` - Uploads a local file into an existing
 exported data dump (must run `cf export-data` first).
1. `cf clean-export-config` will clean your config file and create a new one.

## Installation
- Windows 32Bit: `cf.exe install-plugin https://github.com/18F/cg-export-db/releases/download/v0.0.2/windows-32-cg-export-db.exe`
- Windows 64Bit: `cf.exe install-plugin https://github.com/18F/cg-export-db/releases/download/v0.0.2/windows-64-cg-export-db.exe`
- Mac OS X: `cf install-plugin https://github.com/18F/cg-export-db/releases/download/v0.0.2/mac-cg-export-db`
- Linux 32Bit: `cf install-plugin https://github.com/18F/cg-export-db/releases/download/v0.0.2/linux-32-cg-export-db`
- Linux 64Bit: `cf install-plugin https://github.com/18F/cg-export-db/releases/download/v0.0.2/linux-64-cg-export-db`

## Common Use Cases
### 1. Migrating From EW to GovCloud in 4 Steps!
#### Pre-Reqs
In E/W, you need to have:

1. A S3 bucket already created to stream the dump in the same space as your database.
  - If you do not have a S3 bucket, you can create one with `cf create-service s3 basic MyS3Bucket`.
2. A MySQL or Postgres database already created in your space.

In GovCloud:

1. A MySQL or Postgres database already created in your space.

#### Running
```sh
# Login into EW cloud.gov
cf api https://api.cloud.gov && cf login --sso

# Optionally, run this if you don't have a S3 bucket.
# cf create-service s3 basic MyS3Bucket

# Go and export your data
cf export-data

# Login into GovCloud cloud.gov
cf api https://api.fr.cloud.gov && cf login --sso

# Go and import your data
cf import-data
```
