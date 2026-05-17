# Ultimate WordPress Manager (CLI)

A lightweight, ultra-fast CLI tool to manage local WordPress development environments using Docker. Replaces heavy GUI tools with native performance and automated setup.

## Features

- **One-Click Create:** Automatically sets up WordPress, MariaDB, and WP-CLI.
- **Pre-Configured:** Bypasses the WordPress setup wizard (Admin: `admin` / `admin`).
- **Native Speed:** No Electron overhead—pure Docker performance.
- **Isolated Sites:** Each site has its own container network and local file storage.
- **Full CLI Control:** Start, stop, restart, shell, logs, wp-cli, and database operations.
- **Image Caching:** Uses cached Docker images—pulls only when missing.
- **Easy Cleanup:** Remove sites and their associated Docker volumes with a single command.

## Installation

```bash
curl -sSL https://raw.githubusercontent.com/ehtishamnaveed/wordpress-manager/master/install.sh | bash
```

*Note: Ensure `~/.local/bin` is in your `$PATH`.*

## Usage

### Site Management

| Command | Description |
|---|---|
| `wordpress create <name> <port>` | Create a new WordPress site |
| `wordpress start <name>` | Start a stopped site |
| `wordpress stop <name>` | Stop a running site |
| `wordpress restart <name>` | Restart a site |
| `wordpress delete <name>` | Delete a site (with confirmation) |
| `wordpress list` | List all sites |
| `wordpress info <name>` | Show detailed site info |

### Development

| Command | Description |
|---|---|
| `wordpress shell <name>` | Open bash shell in the WordPress container |
| `wordpress logs <name> [-f]` | View container logs |
| `wordpress wp <name> <args...>` | Run wp-cli commands directly |
| `wordpress ps <name>` | Show containers for a site |
| `wordpress port <name> <port>` | Change the site port |

### Database & Backups

| Command | Description |
|---|---|
| `wordpress db export <name>` | Export database to a SQL file |
| `wordpress db import <name> <file>` | Import a SQL file into the database |
| `wordpress backup <name>` | Full backup (database + site files) |

### Examples

```bash
# Create a site
wordpress create mysite 8080

# List all sites
wordpress list

# Run wp-cli (install a plugin)
wordpress wp mysite plugin install woocommerce --activate

# Open a shell in the WordPress container
wordpress shell mysite

# Export the database
wordpress db export mysite

# Full backup
wordpress backup mysite

# View logs
wordpress logs mysite -f

# Change port
wordpress port mysite 9090
wordpress restart mysite
```

## Requirements

- **Linux** (Tested on Arch, Ubuntu, and Debian)
- **Docker** and **Docker Compose (V2)**
- **Python 3**
- **curl**

## Storage

Site files are stored in `~/.local/share/wordpress-lab/sites/`.
Database backups and site archives are stored per-site in `backups/`.

## License

MIT
