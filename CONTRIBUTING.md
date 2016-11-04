# Contributing

## Embedding Resources

The key to the plugin is the ability to embed static resources.
Whenever you modify/add static resources, you need to re-run `go-bindata`. 

Please follow the [instructions](https://github.com/jteeuwen/go-bindata) for how to install `go-bindata`.

Currently, only the `import` and `export` folders are embedded via:
```sh
go-bindata import/... export/...
```

## Building

```sh
# Get the dependencies
glide install

# Build
go build
```


