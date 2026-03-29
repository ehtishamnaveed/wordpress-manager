#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil
import argparse
import time

BASE_DIR = os.path.expanduser("~/.local/share/wordpress-lab/sites")

COMPOSE_TEMPLATE = """
services:
  db:
    image: mariadb:10.6
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wordpress
      MYSQL_PASSWORD: wordpress
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-u", "root", "-proot"]
      timeout: 5s
      retries: 10

  wordpress:
    image: wordpress:latest
    depends_on:
      db:
        condition: service_healthy
    ports:
      - "{port}:80"
    restart: always
    environment:
      WORDPRESS_DB_HOST: db:3306
      WORDPRESS_DB_USER: wordpress
      WORDPRESS_DB_PASSWORD: wordpress
      WORDPRESS_DB_NAME: wordpress
    volumes:
      - ./app:/var/www/html
"""

def check_dependencies():
    """Verify required system tools are installed."""
    for tool in ["docker", "curl"]:
        if shutil.which(tool) is None:
            print(f"❌ Error: '{tool}' is not installed. Please install it and try again.")
            sys.exit(1)
    
    # Check for docker compose (v2)
    try:
        subprocess.run(["docker", "compose", "version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Error: 'docker compose' (V2) is not available. Please install the Docker Compose plugin.")
        sys.exit(1)

def create_site(name, port):
    path = os.path.join(BASE_DIR, name)
    if os.path.exists(path):
        print(f"❌ Error: Site '{name}' already exists in {path}")
        return
    
    print(f"🚀 Initializing '{name}' on port {port}...")
    try:
        os.makedirs(os.path.join(path, "app"), exist_ok=True)
        with open(os.path.join(path, "docker-compose.yml"), "w") as f:
            f.write(COMPOSE_TEMPLATE.format(port=port))
        
        print("📦 Starting Docker containers...")
        subprocess.run(["docker", "compose", "-p", name, "up", "-d"], cwd=path, check=True)
        
        print("⏳ Waiting for database to be healthy (this can take up to 30s)...")
        time.sleep(15) # Buffer for initial setup

        container_name = f"{name}-wordpress-1"
        print("🛠️ Installing WP-CLI and setting up WordPress...")
        
        setup_script = f"""
            docker exec -u 0 {container_name} curl -s -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar && \
            docker exec -u 0 {container_name} chmod +x wp-cli.phar && \
            docker exec -u 0 {container_name} mv wp-cli.phar /usr/local/bin/wp && \
            docker exec {container_name} wp core install --url=http://localhost:{port} --title='{name.capitalize()}' --admin_user=admin --admin_password=admin --admin_email=admin@example.com --allow-root
        """
        subprocess.run(setup_script, shell=True, check=True)

        print(f"\n✨ SUCCESS!")
        print(f"🔗 URL: http://localhost:{port}")
        print(f"👤 Admin: http://localhost:{port}/wp-admin (admin/admin)")

    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

def delete_site(name):
    path = os.path.join(BASE_DIR, name)
    if not os.path.exists(path):
        print(f"❌ Error: Site '{name}' not found.")
        return
    
    confirm = input(f"⚠️  Confirm deletion of '{name}' and all data? (y/N): ")
    if confirm.lower() != 'y': return

    try:
        print("🛑 Stopping containers...")
        subprocess.run(["docker", "compose", "-p", name, "down", "-v"], cwd=path, check=True)
        print("🗑️  Cleaning up files (requires sudo)...")
        subprocess.run(["sudo", "rm", "-rf", path], check=True)
        print(f"✅ Site '{name}' deleted.")
    except Exception as e:
        print(f"❌ Deletion failed: {e}")

def list_sites():
    if not os.path.exists(BASE_DIR):
        print("📭 No sites created yet.")
        return
    sites = os.listdir(BASE_DIR)
    if not sites:
        print("📭 No sites found.")
        return

    print(f"{'SITE NAME':<20} {'PORT':<10} {'STATUS'}")
    print("-" * 40)
    for name in sites:
        status = "Stopped"
        try:
            res = subprocess.run(["docker", "compose", "-p", name, "ps", "--format", "json"], 
                                cwd=os.path.join(BASE_DIR, name), capture_output=True, text=True)
            if "running" in res.stdout.lower(): status = "🟢 Running"
        except: pass
        print(f"{name:<20} {'---':<10} {status}")

def main():
    check_dependencies()
    parser = argparse.ArgumentParser(description="Wordpress Ultimate Manager")
    subparsers = parser.add_subparsers(dest="command")
    
    c = subparsers.add_parser("create", help="Create a new site")
    c.add_argument("name", help="Name of the site")
    c.add_argument("port", type=int, help="Port number")
    
    d = subparsers.add_parser("delete", help="Delete a site")
    d.add_argument("name", help="Name of the site")
    
    subparsers.add_parser("list", help="List all sites")
    
    args = parser.parse_args()
    if args.command == "create": create_site(args.name, args.port)
    elif args.command == "delete": delete_site(args.name)
    elif args.command == "list": list_sites()
    else: parser.print_help()

if __name__ == "__main__":
    main()
