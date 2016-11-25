build:
				go-bindata import/... export/... pycommon/...
				go build
clean:
				cf uninstall-plugin cg-migrate-db
install: build
				cf install-plugin -f cg-migrate-db
