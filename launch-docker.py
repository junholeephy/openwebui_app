#!/usr/bin/env python3
"""
Launch script for Open WebUI Docker container
"""
import os
import subprocess
import sys
import time

def run_command(command, description, check_output=False):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        if check_output:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            return result.stdout.strip()
        else:
            subprocess.run(command, shell=True, check=True)
            print(f"✅ {description} completed successfully")
            return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return False

def check_container_status():
    """Check if Open WebUI container is running"""
    try:
        result = subprocess.run("docker ps --filter name=open-webui --format '{{.Status}}'", 
                              shell=True, capture_output=True, text=True)
        if result.stdout.strip():
            return "running"
        else:
            return "stopped"
    except:
        return "error"

def start_openwebui():
    """Start Open WebUI using Docker Compose"""
    print("🚀 Starting Open WebUI with Monitoring...")
    
    # Check if .env exists
    if not os.path.exists(".env"):
        print("❌ .env file not found!")
        print("Please run 'python setup-docker.py' first")
        return False
    
    # Start the container
    if not run_command("docker-compose up -d", "Starting Open WebUI and monitoring services"):
        return False
    
    # Wait for containers to be ready
    print("⏳ Waiting for services to start...")
    time.sleep(15)
    
    # Check status
    status = check_container_status()
    if status == "running":
        print("✅ Open WebUI is now running!")
        print("\n🌐 Access Points:")
        print("  • Open WebUI:     http://localhost:8080")
        print("  • MLflow:         http://localhost:5001")
        print("  • MinIO Console:  http://localhost:9001 (minioadmin/minioadmin)")
        print("  • Grafana:        http://localhost:3000 (admin/admin)")
        print("  • Prometheus:     http://localhost:9090")
        print("  • Node Exporter:  http://localhost:9100")
        print("\n📊 Monitoring Features:")
        print("  • Real-time metrics collection")
        print("  • Beautiful Grafana dashboards")
        print("  • System resource monitoring")
        print("  • Open WebUI performance tracking")
        return True
    else:
        print(f"⚠️  Container status: {status}")
        print("Check logs with: docker-compose logs open-webui")
        return False

def stop_openwebui():
    """Stop Open WebUI container"""
    print("🛑 Stopping Open WebUI...")
    return run_command("docker-compose down", "Stopping Open WebUI container")

def show_logs():
    """Show Open WebUI container logs"""
    print("📋 Showing Open WebUI logs...")
    return run_command("docker-compose logs -f open-webui", "Showing logs")

def show_status():
    """Show container status"""
    status = check_container_status()
    print(f"📊 Container Status: {status}")
    
    if status == "running":
        print("✅ Open WebUI is running at http://localhost:8080")
    elif status == "stopped":
        print("⏸️  Open WebUI is stopped")
    else:
        print("❌ Error checking container status")

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("🚀 Open WebUI Docker Launcher with Monitoring")
        print("=" * 50)
        print("Usage:")
        print("  python launch-docker.py start    - Start Open WebUI + Monitoring")
        print("  python launch-docker.py stop     - Stop all services")
        print("  python launch-docker.py status  - Check status")
        print("  python launch-docker.py logs     - Show logs")
        print("  python launch-docker.py restart  - Restart all services")
        print("  python launch-docker.py monitor  - Show monitoring info")
        return
    
    command = sys.argv[1].lower()
    
    if command == "start":
        start_openwebui()
    elif command == "stop":
        stop_openwebui()
    elif command == "status":
        show_status()
    elif command == "logs":
        show_logs()
    elif command == "restart":
        stop_openwebui()
        time.sleep(2)
        start_openwebui()
    elif command == "monitor":
        show_monitoring_info()
    else:
        print(f"❌ Unknown command: {command}")
        print("Use: start, stop, status, logs, restart, or monitor")

def show_monitoring_info():
    """Show monitoring information and access points"""
    print("📊 Open WebUI Monitoring Stack")
    print("=" * 40)
    print("\n🔍 Monitoring Services:")
    print("  • MLflow:         Experiment tracking and model registry")
    print("  • MinIO:          Object storage for ML artifacts")
    print("  • Prometheus:     Metrics collection and storage")
    print("  • Grafana:        Beautiful dashboards and visualizations")
    print("  • Node Exporter:  System resource metrics")
    print("  • Open WebUI:     Built-in metrics endpoint")
    
    print("\n🌐 Access URLs:")
    print("  • Open WebUI:     http://localhost:8080")
    print("  • MLflow:         http://localhost:5001")
    print("  • MinIO Console:  http://localhost:9001")
    print("  • Grafana:        http://localhost:3000")
    print("  • Prometheus:     http://localhost:9090")
    print("  • Node Exporter:  http://localhost:9100")
    
    print("\n🔑 Default Credentials:")
    print("  • MLflow:         No authentication required")
    print("  • MinIO:          minioadmin / minioadmin")
    print("  • Grafana:        admin / admin")
    
    print("\n📈 What You Can Monitor:")
    print("  • API request rates and response times")
    print("  • System CPU, memory, and disk usage")
    print("  • Docker container performance")
    print("  • Open WebUI service health")
    print("  • User activity and chat statistics")
    
    print("\n💡 Tips:")
    print("  • Check Grafana dashboards for insights")
    print("  • Use Prometheus queries for custom metrics")
    print("  • Monitor system resources during heavy usage")
    print("  • Set up alerts for critical metrics")

if __name__ == "__main__":
    main()
