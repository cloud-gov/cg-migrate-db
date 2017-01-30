build:
				go get github.com/ArthurHlt/rutil && GOOS=linux GOARCH=amd64 go build -v github.com/ArthurHlt/rutil && mv rutil resources/bin/rutil
				go-bindata resources/...
				go build
clean:
				cf uninstall-plugin cg-migrate-db
install: build
				cf install-plugin -f cg-migrate-db
