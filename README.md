# cg-migrate-db

`cg-migrate-db` is a Cloud Foundry CLI Plugin for migrating the data of services.

## Installation
- Windows 32Bit: `cf.exe install-plugin https://github.com/18F/cg-migrate-db/releases/download/v0.0.3/windows-32-cg-migrate-db.exe`
- Windows 64Bit: `cf.exe install-plugin https://github.com/18F/cg-migrate-db/releases/download/v0.0.3/windows-64-cg-migrate-db.exe`
- Mac OS X: `cf install-plugin https://github.com/18F/cg-migrate-db/releases/download/v0.0.3/mac-cg-migrate-db`
- Linux 32Bit: `cf install-plugin https://github.com/18F/cg-migrate-db/releases/download/v0.0.3/linux-32-cg-migrate-db`
- Linux 64Bit: `cf install-plugin https://github.com/18F/cg-migrate-db/releases/download/v0.0.3/linux-64-cg-migrate-db`

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

### `cf export-data`
**Creates a backup your data**

Interactively creates an application, binds to your
service, streams the data from your service to a S3 bucket.

**Usage**:

```sh
cf export-data
```

**Note**

You will need to already have the S3 bucket created.
If you do not have it, you can do so by running:
```sh
cf create-service s3 basic YourS3BackupNameHere
```

### `cf import-data`
**Restores a backup of your data**

Interactively creates an application, binds to your
new service, streams the data from the S3 bucket to the new service.

**Usage:**
```sh
cf import-data
```

### `cf download-backup-data`
**Download a backup to your local computer**

Interactively selects the backup data from an
existing exported data dump (must run `cf export-data` first) and downloads it
locally to your computer.

**Usage:**
```sh
cf download-backup-data
```

### `cf upload-backup-data`
**Uploads a backup from your local computer**

Uploads a local file into an existing exported data dump
(must run `cf export-data` first). It will get renamed appropriately upon
upload automatically.

**Usage:**
```sh
cf upload-backup-data -p <file_path> [-store <name_of_s3_service]
```

*Note: Providing the optional `-store` flag will run this command in
non-interactive mode.*

### `cf clean-export-config`
**Cleans your config file and create a new one.**

**Usage:**
```sh
cf clean-export-config
```

## Common Use Cases
### 1. Migrating From EW to GovCloud in 4 Steps!
#### Pre-Reqs
In E/W, you need to have:

1. A S3 bucket already created to stream the dump in the same space as your database.
  - If you do not have a S3 bucket, you can create one with `cf create-service s3 basic MyS3Bucket`.
2. A MySQL or Postgres database already created in your space.

In GovCloud:

1. A MySQL or Postgres database already created in your space.

#### Migrating Data From EW To GovCloud
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
