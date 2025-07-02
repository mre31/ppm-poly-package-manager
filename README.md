# Poly Package Manager (PPM)

PPM is a powerful, command-line package manager for the Poly shell. It allows you to easily find, install, update, and manage plugins from a central repository, extending the functionality of your Poly environment.

## Features

- **Install & Uninstall:** Easily add and remove plugins from your Poly setup.
- **Update:** Keep your plugins up-to-date with the latest versions from the repository.
- **Search:** Find new and useful plugins by searching names and descriptions.
- **Enable & Disable:** Temporarily turn plugins on or off without deleting them.
- **Secure:** Verifies the integrity of every downloaded plugin using SHA256 hashes to prevent corruption and tampering.
- **Health Checks:** Includes a `doctor` command to diagnose and fix common issues with your setup.

## Installation

1.  Download the `package_manager.py` file from this repository.
2.  Place the file in your Poly plugins directory, which is typically located at `~/.plplugins/`.
3.  You may need to create this directory if it does not already exist.
4.  Restart the Poly application. The `ppm` command will now be available.

## Usage

PPM provides a simple and intuitive command-line interface.

### Command Overview

| Command                           | Alias | Description                                                  |
| --------------------------------- | ----- | ------------------------------------------------------------ |
| `ppm help`                        |       | Shows the help message with all available commands.          |
| `ppm install <plugin_name>`       | `i`   | Downloads and installs a plugin.                             |
| `ppm uninstall <plugin_name>`     | `un`  | Removes a plugin from your system.                           |
| `ppm update <plugin_name\|--all>` | `up`  | Updates a specific plugin or all installed plugins.          |
| `ppm list`                        | `ls`  | Lists all available plugins in the remote repository.        |
| `ppm list -i`                     | `ls -i` | Lists all locally installed plugins and their status.        |
| `ppm search <keyword>`            |       | Searches for plugins by name or description.                 |
| `ppm info <plugin_name>`          |       | Shows detailed information about a specific plugin.          |
| `ppm enable <plugin_name>`        |       | Enables a disabled plugin.                                   |
| `ppm disable <plugin_name>`       |       | Disables an installed plugin without deleting it.            |
| `ppm doctor`                      |       | Checks your PPM setup for potential issues.                  |

## For Plugin Developers

To make your Poly plugins available through PPM, you need to create a GitHub repository with the following structure:

```
.
├── plugins.json
└── plugins/
    ├── your-plugin-one.py
    └── your-plugin-two.py
```

The `plugins.json` file acts as a manifest that lists all available plugins. It must contain a "plugins" object where each key is the installable name of your plugin.

Each plugin object must have the following fields:

-   `file`: The full path to the plugin file within the repository (e.g., "plugins/your-plugin.py").
-   `author`: Your name or username.
-   `description`: A short, one-line description of the plugin.
-   `version`: The version number of your plugin (e.g., "1.0.0").
-   `sha256`: The SHA256 hash of the plugin's `.py` file. This is crucial for security.

#### Example `plugins.json`:

```json
{
  "plugins": {
    "my-cool-plugin": {
      "file": "plugins/my-cool-plugin.py",
      "author": "YourName",
      "description": "A very cool plugin that does things.",
      "version": "1.0.0",
      "sha256": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6"
    }
  }
}
```

You can generate the SHA256 hash for your file using standard command-line tools:

-   **Linux/macOS:** `shasum -a 256 /path/to/your/plugin.py`
-   **Windows (CMD):** `certutil -hashfile C:\path\to\your\plugin.py SHA256`

## License

This project is licensed under the MIT License.
