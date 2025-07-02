"""
    Plugin Name: Poly Package Manager
    Description: A package manager for Poly to install plugins from a central repository.
    Author: mre31
    Version: 1.0
    Last Updated: July 2, 2025
"""

import os
import json
import urllib.request
from urllib.error import URLError, HTTPError
import hashlib

REPO_URL = "https://raw.githubusercontent.com/mre31/ppm-poly-package-manager/master/"
MANIFEST_FILE = "plugins.json"

def get_plugins_dir():
    """Returns the absolute path to the user's plplugins directory."""
    return os.path.join(os.path.expanduser("~"), "plplugins")

def ppm_install(tab, plugin_name):
    """
    Downloads and installs a plugin from the repository with hash verification.
    """
    if not plugin_name:
        tab.add("Usage: ppm install <plugin_name>")
        return

    manifest_url = REPO_URL + MANIFEST_FILE
    tab.add(f"Fetching plugin manifest from {manifest_url}...")

    try:
        with urllib.request.urlopen(manifest_url) as response:
            manifest_data = response.read().decode('utf-8')
            manifest = json.loads(manifest_data)
    except (HTTPError, URLError) as e:
        tab.add(f"Error: Could not fetch plugin manifest. {e}")
        return
    except json.JSONDecodeError:
        tab.add("Error: Could not parse plugin manifest.")
        return

    plugins = manifest.get("plugins", {})
    if plugin_name not in plugins:
        tab.add(f"Error: Plugin '{plugin_name}' not found in the repository.")
        return

    plugin_info = plugins[plugin_name]
    plugin_file = plugin_info.get("file")
    expected_hash = plugin_info.get("sha256")
    
    if not plugin_file or not expected_hash:
        tab.add(f"Error: Plugin '{plugin_name}' is missing 'file' or 'sha256' in manifest.")
        return

    plugin_url = REPO_URL + plugin_file
    tab.add(f"Downloading plugin '{plugin_name}' from {plugin_url}...")

    try:
        with urllib.request.urlopen(plugin_url) as response:
            plugin_content = response.read()
    except (HTTPError, URLError) as e:
        tab.add(f"Error: Could not download plugin file. {e}")
        return

    # Verify the hash
    actual_hash = hashlib.sha256(plugin_content).hexdigest()
    if actual_hash != expected_hash:
        tab.add("Error: Hash mismatch! The downloaded file may be corrupted or tampered with.")
        tab.add(f"  Expected: {expected_hash}")
        tab.add(f"  Actual:   {actual_hash}")
        return
    
    tab.add("Hash verification successful.")

    plugins_dir = get_plugins_dir()
    # The destination path should only be the filename, not the full path from the repo
    dest_filename = os.path.basename(plugin_file)
    plugin_path = os.path.join(plugins_dir, dest_filename)
    os.makedirs(plugins_dir, exist_ok=True)

    try:
        with open(plugin_path, 'wb') as f:
            f.write(plugin_content)
        tab.add(f"Successfully installed plugin '{plugin_name}' to {plugin_path}")
        tab.add("Please restart Poly to load the new plugin.")
    except IOError as e:
        tab.add(f"Error: Could not write plugin file. {e}")

def ppm_help(tab):
    """Displays the help message for ppm."""
    tab.add("Poly Package Manager (PPM) - Help")
    tab.add("Usage: ppm <command> [options]")
    tab.add("")
    tab.add("Commands:")
    tab.add("  install <plugin_name>   - Installs a plugin from the repository.")
    tab.add("  uninstall <plugin_name> - Uninstalls a plugin.")
    tab.add("  update <plugin_name|--all> - Updates one or all installed plugins.")
    tab.add("  list                      - Lists all available plugins in the repository.")
    tab.add("  list -i                   - Lists all installed plugins.")
    tab.add("  search <keyword>          - Searches for plugins by keyword.")
    tab.add("  help                      - Shows this help message.")

def ppm_list(tab, installed_only=False):
    """Lists available or installed plugins."""
    if installed_only:
        tab.add("Installed plugins:")
        plugins_dir = get_plugins_dir()
        if not os.path.exists(plugins_dir):
            tab.add("  No plugins installed.")
            return
        for fname in os.listdir(plugins_dir):
            if fname.endswith(".py"):
                tab.add(f"  - {os.path.splitext(fname)[0]}")
    else:
        tab.add("Available plugins from repository:")
        manifest_url = REPO_URL + MANIFEST_FILE
        try:
            with urllib.request.urlopen(manifest_url) as response:
                manifest_data = response.read().decode('utf-8')
                manifest = json.loads(manifest_data)
        except (HTTPError, URLError) as e:
            tab.add(f"  Error: Could not fetch plugin manifest. {e}")
            return
        except json.JSONDecodeError:
            tab.add("  Error: Could not parse plugin manifest.")
            return
        
        plugins = manifest.get("plugins", {})
        if not plugins:
            tab.add("  No plugins found in the repository.")
            return

        for name, info in plugins.items():
            tab.add(f"  - {name}: {info.get('description', 'No description')}")

def ppm_uninstall(tab, plugin_name):
    """Uninstalls a plugin."""
    if not plugin_name:
        tab.add("Usage: ppm uninstall <plugin_name>")
        return

    plugins_dir = get_plugins_dir()
    
    # Find the plugin file name from the manifest first
    manifest_url = REPO_URL + MANIFEST_FILE
    try:
        with urllib.request.urlopen(manifest_url) as response:
            manifest_data = response.read().decode('utf-8')
            manifest = json.loads(manifest_data)
    except (HTTPError, URLError, json.JSONDecodeError):
        # If we can't get the manifest, we can try to guess the filename
        plugin_file_name = f"{plugin_name}.py"
    else:
        plugins = manifest.get("plugins", {})
        plugin_info = plugins.get(plugin_name)
        if not plugin_info:
            tab.add(f"Warning: Plugin '{plugin_name}' not in manifest, attempting to remove anyway.")
            plugin_file_name = f"{plugin_name}.py"
        else:
            plugin_file_name = os.path.basename(plugin_info.get("file"))

    plugin_path = os.path.join(plugins_dir, plugin_file_name)

    if not os.path.exists(plugin_path):
        tab.add(f"Error: Plugin '{plugin_name}' is not installed.")
        return

    try:
        os.remove(plugin_path)
        tab.add(f"Successfully uninstalled plugin '{plugin_name}'.")
        tab.add("Please restart Poly for the change to take effect.")
    except OSError as e:
        tab.add(f"Error: Could not remove plugin file. {e}")

def ppm_search(tab, keyword):
    """Searches for plugins in the repository."""
    if not keyword:
        tab.add("Usage: ppm search <keyword>")
        return

    tab.add(f"Searching for plugins matching '{keyword}'...")
    manifest_url = REPO_URL + MANIFEST_FILE
    try:
        with urllib.request.urlopen(manifest_url) as response:
            manifest_data = response.read().decode('utf-8')
            manifest = json.loads(manifest_data)
    except (HTTPError, URLError) as e:
        tab.add(f"  Error: Could not fetch plugin manifest. {e}")
        return
    except json.JSONDecodeError:
        tab.add("  Error: Could not parse plugin manifest.")
        return

    plugins = manifest.get("plugins", {})
    matches = []
    for name, info in plugins.items():
        if keyword.lower() in name.lower() or keyword.lower() in info.get('description', '').lower():
            matches.append((name, info))

    if not matches:
        tab.add("No plugins found matching your search.")
        return

    for name, info in matches:
        tab.add(f"  - {name} (v{info.get('version', 'N/A')}): {info.get('description', 'No description')}")

def ppm_update(tab, plugin_name):
    """Updates one or all plugins."""
    if not plugin_name:
        tab.add("Usage: ppm update <plugin_name|--all>")
        return

    if plugin_name == "--all":
        tab.add("Updating all installed plugins...")
        plugins_dir = get_plugins_dir()
        if not os.path.exists(plugins_dir):
            tab.add("No plugins installed.")
            return
        
        installed_plugins = [os.path.splitext(fname)[0] for fname in os.listdir(plugins_dir) if fname.endswith(".py")]
        if not installed_plugins:
            tab.add("No plugins to update.")
            return
            
        for p_name in installed_plugins:
            tab.add(f"\n--- Updating {p_name} ---")
            ppm_install(tab, p_name) # Re-use the install logic
    else:
        tab.add(f"Updating plugin '{plugin_name}'...")
        ppm_install(tab, plugin_name) # Re-use the install logic for a single plugin

def ppm_command(tab, args):
    """
    Main handler for the 'ppm' command.
    """
    parts = args.split()
    if not parts:
        ppm_help(tab)
        return

    subcommand = parts[0].lower()
    
    if subcommand == "help":
        ppm_help(tab)
        return

    if subcommand == "install":
        plugin_name = parts[1] if len(parts) > 1 else None
        ppm_install(tab, plugin_name)
    elif subcommand == "uninstall":
        plugin_name = parts[1] if len(parts) > 1 else None
        ppm_uninstall(tab, plugin_name)
    elif subcommand == "list":
        installed_only = len(parts) > 1 and parts[1] == "-i"
        ppm_list(tab, installed_only)
    elif subcommand == "search":
        keyword = parts[1] if len(parts) > 1 else None
        ppm_search(tab, keyword)
    elif subcommand == "update":
        plugin_name = parts[1] if len(parts) > 1 else None
        ppm_update(tab, plugin_name)
    else:
        tab.add(f"Unknown command: {subcommand}")
        ppm_help(tab)




def register_plugin(app_context):
    """
    Registers the 'ppm' command.
    """
    define_command = app_context["define_command"]
    define_command("ppm", ppm_command, "Manages Poly plugins.")
