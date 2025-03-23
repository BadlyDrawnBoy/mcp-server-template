# GhidraMCP

## Features

## Installing
Go to Claude > Settings > Developer > Edit Config > claude_desktop_config.json

/Users/YOUR_USER/Library/Application Support/Claude/claude_desktop_config.json

{
  "mcpServers": {
    "ghidra": {
      "command": "python",
      "args": [
        "ABSOLUTE_PATH_TO/bridge_mcp_ghidra.py"
      ]
    }
  }
}

Import the plugin from the releases page into Ghidra

* Make sure Ghidra is installed
  https://ghidra-sre.org/
* Install the extension
  * Start Ghidra
  * Open `File->Install Extensions...`
  * Press the `+` icon found in the top right of the `Install Extensions` window
  * Navigate to the file location where you downloaded the extension zip file
    above and select it
  * Press `OK`
  * You will be prompted to restart Ghidra for the changes to take effect

## Building
mvn clean package assembly:single
