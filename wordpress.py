#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil
import argparse
import time
import re

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
    for tool in ["docker", "curl"]:
        if shutil.which(tool) is None:
            print(f"❌ Error: '{tool}' is not installed.")
            sys.exit(1)
    try:
        subprocess.run(["docker", "compose", "version"], capture_output=True, check=True)
    except:
        print("❌ Error: 'docker compose' (V2) is not available.")
        sys.exit(1)

def create_site(name, port):
    path = os.path.join(BASE_DIR, name)
    if os.path.exists(path):
        print(f"❌ Error: Site '{name}' already exists.")
        return
    
    print(f"🚀 Initializing '{name}' on port {port}...")
    try:
        os.makedirs(os.path.join(path, "app"), exist_ok=True)
        with open(os.path.join(path, "docker-compose.yml"), "w") as f:
            f.write(COMPOSE_TEMPLATE.format(port=port))
        
        subprocess.run(["docker", "compose", "-p", name, "up", "-d"], cwd=path, check=True)
        
        print("⏳ Waiting for setup (30s)...")
        time.sleep(20)

        container_name = f"{name}-wordpress-1"
        setup_script = f"""
            docker exec -u 0 {container_name} curl -s -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar && \
            docker exec -u 0 {container_name} chmod +x wp-cli.phar && \
            docker exec -u 0 {container_name} mv wp-cli.phar /usr/local/bin/wp && \
            docker exec {container_name} wp core install --url=http://localhost:{port} --title='{name.capitalize()}' --admin_user=admin --admin_password=admin --admin_email=admin@example.com --allow-root
        """
        subprocess.run(setup_script, shell=True, check=True)
        print(f"\n✨ SUCCESS! http://localhost:{port} (admin/admin)")
    except Exception as e:
        print(f"❌ Failed: {e}")

def delete_site(name):
    path = os.path.join(BASE_DIR, name)
    if not os.path.exists(path):
        print(f"❌ Error: Site '{name}' not found.")
        return
    if input(f"⚠️ Confirm delete '{name}'? (y/N): ").lower() != 'y': return
    try:
        subprocess.run(["docker", "compose", "-p", name, "down", "-v"], cwd=path, check=True)
        subprocess.run(["sudo", "rm", "-rf", path], check=True)
        print(f"✅ Deleted '{name}'.")
    except Exception as e:
        print(f"❌ Error: {e}")

def get_site_port(path):
    compose_path = os.path.join(path, "docker-compose.yml")
    if not os.path.exists(compose_path): return "???"
    try:
        with open(compose_path, "r") as f:
            content = f.read()
            match = re.search(r'["\'](\d+):80["\']', content)
            return match.group(1) if match else "???"
    except: return "???"

def list_sites():
    if not os.path.exists(BASE_DIR): return
    sites = sorted(os.listdir(BASE_DIR))
    if not sites:
        print("📭 No sites found.")
        return

    print(f"{'SITE NAME':<20} {'PORT':<10} {'STATUS'}")
    print("-" * 45)
    for name in sites:
        path = os.path.join(BASE_DIR, name)
        port = get_site_port(path)
        status = "🔴 Stopped"
        try:
            res = subprocess.run(["docker", "compose", "-p", name, "ps", "--format", "json"], 
                                cwd=path, capture_output=True, text=True)
            if "running" in res.stdout.lower():
                status = "🟢 Running"
        except: pass
        print(f"{name:<20} {port:<10} {status}")

def main():
    check_dependencies()
    parser = argparse.ArgumentParser(description="Wordpress Ultimate Manager")
    subparsers = parser.add_subparsers(dest="command")
    c = subparsers.add_parser("create"); c.add_argument("name"); c.add_argument("port", type=int)
    d = subparsers.add_parser("delete"); d.add_argument("name")
    subparsers.add_parser("list")
    args = parser.parse_args()
    if args.command == "create": create_site(args.name, args.port)
    elif args.command == "delete": delete_site(args.name)
    elif args.command == "list": list_sites()
    else: parser.print_help()

if __name__ == "__main__": main()
