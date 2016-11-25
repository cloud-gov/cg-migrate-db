#!/usr/bin/env bash
PLUGIN_PATH=$GOPATH/src/github.com/18F/cg-migrate-db
PLUGIN_NAME=$(basename $PLUGIN_PATH)

rm -rf $PLUGIN_PATH/releases
mkdir -p $PLUGIN_PATH/releases
GOOS=linux GOARCH=amd64 go build -o $PLUGIN_PATH/releases/linux-64-${PLUGIN_NAME}
GOOS=linux GOARCH=386 go build -o $PLUGIN_PATH/releases/linux-32-${PLUGIN_NAME}
GOOS=windows GOARCH=amd64 go build -o $PLUGIN_PATH/releases/windows-64-${PLUGIN_NAME}.exe
GOOS=windows GOARCH=386 go build -o $PLUGIN_PATH/releases/windows-32-${PLUGIN_NAME}.exe
GOOS=darwin GOARCH=amd64 go build -o $PLUGIN_PATH/releases/mac-${PLUGIN_NAME}
