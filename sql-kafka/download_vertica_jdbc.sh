#!/bin/bash

# URL to download the Vertica JDBC driver
VERTICA_JDBC_URL="https://www.vertica.com/client_drivers/vertica-jdbc-12.0.0-0.jar"

# Directory to place the downloaded driver
PLUGINS_DIR="./plugins"

# Create the plugins directory if it doesn't exist
mkdir -p $PLUGINS_DIR

# Download the Vertica JDBC driver
curl -o $PLUGINS_DIR/vertica-jdbc.jar $VERTICA_JDBC_URL

echo "Vertica JDBC driver downloaded and placed in $PLUGINS_DIR"
