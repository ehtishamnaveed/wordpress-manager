# Ultimate WordPress Manager (CLI)

A lightweight, ultra-fast CLI tool to manage local WordPress development environments using Docker. Replaces heavy GUI tools with native performance and automated setup.

## ✨ Features

- **One-Click Install:** Automatically sets up WordPress, MariaDB, and WP-CLI.
- **Pre-Configured:** Bypasses the WordPress setup wizard (Admin: `admin` / `admin`).
- **Native Speed:** No Electron overhead—pure Docker performance.
- **Isolated Sites:** Each site has its own container network and local file storage.
- **Easy Cleanup:** Remove sites and their associated Docker volumes with a single command.

## 🚀 Installation

Run the following command in your terminal:

```bash
curl -sSL https://raw.githubusercontent.com/ehtishamnaveed/wordpress-manager/master/install.sh | bash
```

*Note: Ensure `~/.local/bin` is in your `$PATH`.*

## 🛠️ Usage

### Create a new site
Spin up a fresh WordPress instance on a specific port:
```bash
wordpress create my-project 8080
```

### List all sites
See all your active and stopped sites:
```bash
wordpress list
```

### Delete a site
Completely remove a site and all its data:
```bash
wordpress delete my-project
```

## 📋 Requirements

- **Linux** (Tested on Arch, Ubuntu, and Debian)
- **Docker** and **Docker Compose (V2)**
- **Python 3**
- **curl**

## 📂 Storage
Site files are stored in `~/.local/share/wordpress-lab/sites/`.

## License
MIT
