# Contributing

## Embedding Resources

The key to the plugin is the ability to embed static resources.
Whenever you modify/add static resources, you need to re-run
`go-bindata`.

Please follow the [instructions](https://github.com/jteeuwen/go-bindata)
 for how to install `go-bindata`.

Once you have `go-bindata`, run `make build`. It will re-generate the
`bindata.go` and then build the project.

### Embedded Binaries

Currently, the MySQL and PostgreSQL client binaries are among the
resources embedded into the final plugin.

- [PostgreSQL-Client 9.4](http://security.debian.org/pool/updates/main/p/postgresql-9.4/postgresql-client-9.4_9.4.9-0+deb8u1_amd64.deb)
- [MySQL-Client 5.5](http://security.debian.org/pool/updates/main/m/mysql-5.5/mysql-client-5.5_5.5.53-0+deb7u1_amd64.deb)
- [Redis CLI 2.8.17](http://security.debian.org/pool/updates/main/r/redis/redis-tools_2.8.17-1+deb8u5_amd64.deb) 

*TODO:* Find a mirror that uses **HTTPS**

Once you download that, run `dpkg -x <THE .DEB file you download> <Destination Folder>` and you will find the binaries in the folder.


## Building

```sh
# Get the dependencies
glide install

# Build only the go source
go build

# Build re-generate bindata.go and build the go source
make build
```

## Installing your local copy as a plugin

The following will uninstall the plugin, build your local version, and
install it.

```sh
make clean; make install
```

