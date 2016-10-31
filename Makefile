build:
				go build
clean:
				cf uninstall-plugin cg-export-db
install: build
				cf install-plugin -f cg-export-db
