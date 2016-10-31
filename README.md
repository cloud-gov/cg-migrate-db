# cg-export-db

There are two main commands:

- `cf export-data` - Interactively creates an application, binds to your
 service, streams the data from your service to a S3 bucket.
- `cf import-data` - Interactively creates an application, binds to your
 new service, streams the data from the S3 bucket to the new service.

## Installation
- Windows 32Bit: `cf.exe install-plugin https://github.com/18F/cg-export-db/releases/download/v0.0.1/windows-32-cg-export-db.exe`
- Windows 64Bit: `cf.exe install-plugin https://github.com/18F/cg-export-db/releases/download/v0.0.1/windows-64-cg-export-db.exe`
- Mac OS X: `cf install-plugin https://github.com/18F/cg-export-db/releases/download/v0.0.1/mac-cg-export-db`
- Linux 32Bit: `cf install-plugin https://github.com/18F/cg-export-db/releases/download/v0.0.1/linux-32-cg-export-db`
- Linux 64Bit: `cf install-plugin https://github.com/18F/cg-export-db/releases/download/v0.0.1/linux-64-cg-export-db`

## Common Use Cases
### Migrating From EW to GovCloud in 4 Steps!
#### Pre-Reqs
In E/W, you need to have:
1. An S3 bucket already created to stream the dump in the same space as your database.
1. A MySQL database already created in your space.

In GovCloud:
1. A MySQL database already created in your space.

#### Running
```sh
# Login into EW cloud.gov
cf api https://api.cloud.gov && cf login --sso

# Go and export your data
cf export-data

# Login into GovCloud cloud.go
cf api https://api.fr.cloud.gov && cf login --sso

# Go and import your data
cf import-data
```
