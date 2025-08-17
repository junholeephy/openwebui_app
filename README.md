# OpenWebUI - FastAPI Application

A modern, responsive web chat interface built with FastAPI and OpenAI API integration.

## ✨ Features

- 🤖 **AI Chat Interface**: Powered by OpenAI's GPT models
- 💬 **Real-time Chat**: WebSocket support for streaming responses
- 🎨 **Modern UI**: Beautiful, responsive design with animations
- 🔧 **FastAPI Backend**: High-performance Python web framework
- 📱 **Mobile Friendly**: Responsive design for all devices
- 💾 **Chat History**: Local storage and server-side history
- ⚙️ **Customizable**: Adjustable temperature and token limits

## 🚀 Quick Start

### **Option 1: Docker Setup (Recommended) 🐳**

The easiest way to get started is using Docker with the official Open WebUI:

```bash
# 1. Run the Docker setup script
python setup-docker.py

# 2. Edit .env file with your OpenAI API key
# 3. Launch Open WebUI
python launch-docker.py start

# 4. Open your browser to http://localhost:8080
```

**Docker Commands:**
```bash
# Start Open WebUI
python launch-docker.py start

# Check status
python launch-docker.py status

# View logs
python launch-docker.py logs

# Stop Open WebUI
python launch-docker.py stop

# Restart Open WebUI
python launch-docker.py restart
```

### **Option 2: Custom FastAPI App**

If you prefer to run the custom FastAPI application:

```bash
# Run the setup script
python setup.py

# Edit .env file with your OpenAI API key
# Then run the app
python run.py
```

### **Option 3: Manual Setup**

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your OpenAI API key

# Run the application
python run.py
# OR
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📋 Requirements

- **Python**: 3.8 or higher
- **Docker**: For Docker setup (recommended)
- **OpenAI API Key**: Get one at [platform.openai.com](https://platform.openai.com)
- **Internet Connection**: Required for OpenAI API calls

## 🔧 Configuration

### **Docker Configuration**

The `docker-compose.yml` file is pre-configured with:
- **Port**: 8080 (Open WebUI)
- **Default Model**: GPT-4o-mini
- **Available Models**: GPT-4o-mini, GPT-4o, GPT-4-turbo, GPT-3.5-turbo
- **Data Persistence**: Your chat history and settings are saved

### **Monitoring Configuration**

The monitoring stack includes:
- **MLflow**: Port 5000 (experiment tracking)
- **MinIO**: Port 9000 (API), 9001 (Console)
- **Prometheus**: Port 9090 (metrics collection)
- **Grafana**: Port 3000 (dashboards)
- **Node Exporter**: Port 9100 (system metrics)
- **Metrics Retention**: 200 hours of historical data
- **Auto-scraping**: Every 15 seconds for system metrics, 10 seconds for Open WebUI

### **Environment Variables**

Create a `.env` file in the project root:

```env
# Required
OPENAI_API_KEY=your_actual_api_key_here

# Open WebUI Configuration
WEBUI_SECRET_KEY=your_secret_key_for_webui_access

# Optional
DEFAULT_USER_ROLE=admin
DEFAULT_MODELS=gpt-4o-mini,gpt-4o,gpt-4-turbo,gpt-3.5-turbo
DEFAULT_MODEL=gpt-4o-mini

# Monitoring (optional)
GRAFANA_PASSWORD=admin
```

## 📁 Project Structure

```
openwebui_app/
├── docker-compose.yml      # Docker configuration
├── setup-docker.py         # Docker setup automation
├── launch-docker.py        # Docker container management
├── main.py                 # Custom FastAPI application
├── run.py                  # Custom app launcher
├── setup.py                # Custom app setup
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── monitoring/             # Monitoring stack configuration
│   ├── prometheus.yml      # Prometheus configuration
│   └── grafana/            # Grafana setup
│       ├── provisioning/   # Auto-configuration
│       │   ├── datasources/prometheus.yml
│       │   └── dashboards/dashboards.yml
│       └── dashboards/     # Custom dashboards
│           └── open-webui-dashboard.json
├── templates/
│   └── index.html         # Custom app interface
├── static/
│   ├── css/
│   │   └── style.css      # Custom app styling
│   └── js/
│       └── app.js         # Custom app logic
└── README.md              # This file
```

## 🎯 What You Get with Docker

By using Docker with the official Open WebUI, you get:

- **Full-featured AI interface** with 107k+ stars on GitHub
- **Multiple AI providers** (OpenAI, Ollama, local models)
- **Advanced features** like RAG, image generation, file uploads
- **Professional UI/UX** with Svelte frontend
- **Active development** and community support
- **Enterprise features** like user management, API keys, etc.

## 📊 **Monitoring & Observability Stack**

Your Open WebUI setup includes a comprehensive monitoring solution:

### **🔍 Monitoring Services**

- **MLflow** - Experiment tracking and model registry
- **MinIO** - Object storage for ML artifacts
- **Prometheus** - Metrics collection and storage
- **Grafana** - Beautiful dashboards and visualizations  
- **Node Exporter** - System resource monitoring
- **Open WebUI Metrics** - Built-in performance tracking

### **📈 What You Can Monitor**

1. **Open WebUI Performance**:
   - API request rates and response times
   - Error rates and service health
   - User activity and chat statistics
   - Model usage patterns

2. **System Resources**:
   - CPU, memory, and disk usage
   - Network traffic and I/O performance
   - Docker container health
   - Resource utilization trends

3. **Custom Metrics**:
   - Chat session duration
   - API cost tracking
   - User engagement patterns
   - Performance bottlenecks

## 🛠️ Development

### **Running with Docker & Monitoring**

```bash
# Start Open WebUI + Monitoring Stack
python launch-docker.py start

# View logs in real-time
python launch-docker.py logs

# Check monitoring status
python launch-docker.py monitor

# Stop all services
python launch-docker.py stop
```

### **Monitoring Access Points**

Once started, access your monitoring tools at:

- **Open WebUI**: http://localhost:8080
- **MLflow**: http://localhost:5000
- **MinIO Console**: http://localhost:9001 (minioadmin/minioadmin)
- **Grafana**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090
- **Node Exporter**: http://localhost:9100

### **Running Custom FastAPI App**

```bash
python run.py
```

The app will automatically reload when you make changes.

## 🐛 Troubleshooting

### **Docker Issues**

1. **Docker not running**: Start Docker Desktop first
2. **Port conflicts**: Change port in `docker-compose.yml`
3. **Container won't start**: Check logs with `python launch-docker.py logs`

### **Monitoring Issues**

1. **Grafana not accessible**: Check if container is running with `docker ps`
2. **No metrics in Prometheus**: Verify Open WebUI metrics endpoint at `/metrics`
3. **Dashboard not loading**: Check Grafana logs with `docker-compose logs grafana`
4. **High resource usage**: Monitor system resources in Grafana dashboards

### **Common Issues**

1. **Import Errors**: Make sure you've installed requirements with `pip install -r requirements.txt`

2. **OpenAI API Errors**: 
   - Check your API key in `.env`
   - Ensure you have sufficient API credits
   - Verify your OpenAI account is active

3. **Port Already in Use**: Change the port in `docker-compose.yml` or `run.py`

4. **Environment Variables**: Make sure `.env` file exists and contains `OPENAI_API_KEY`

### **Getting Help**

- Check the logs in your terminal for error messages
- Verify your OpenAI API key is correct
- Ensure Docker is running (for Docker setup)
- Check our [Open WebUI Documentation](https://github.com/open-webui/open-webui)

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🌟 Why Open WebUI?

Open WebUI is the most popular open-source AI chat interface with:
- **107k+ GitHub stars**
- **Active development** and community
- **Professional features** like RAG, file uploads, user management
- **Multiple AI providers** support
- **Beautiful, responsive UI** built with Svelte
- **Enterprise-ready** with proper authentication and security

## 📊 **Monitoring & Analytics Guide**

### **Getting Started with Monitoring**

1. **Access Grafana**: Navigate to http://localhost:3000
2. **Login**: Use `admin` / `admin` credentials
3. **View Dashboard**: Open WebUI dashboard is pre-loaded
4. **Explore Metrics**: Use Prometheus queries for custom insights

### **Key Monitoring Commands**

```bash
# Check monitoring status
python launch-docker.py monitor

# View specific service logs
docker-compose logs prometheus
docker-compose logs grafana
docker-compose logs node-exporter

# Check container health
docker ps
docker stats

# Access Prometheus directly
curl http://localhost:9090/api/v1/targets
```

### **Creating Custom Dashboards**

1. **In Grafana**: Click "+" → "Dashboard"
2. **Add Panels**: Choose visualization types (graphs, stats, tables)
3. **Use PromQL**: Write queries like:
   - `rate(http_requests_total[5m])` - Request rate
   - `histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))` - 95th percentile response time
   - `100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)` - CPU usage

### **Setting Up Alerts**

1. **In Grafana**: Go to Alerting → Notification channels
2. **Configure Rules**: Set thresholds for critical metrics
3. **Examples**:
   - High CPU usage (>80%)
   - High response time (>5s)
   - Service down (up metric = 0)
   - High error rate (>5%)

### **Performance Optimization Tips**

- **Monitor during peak usage** to identify bottlenecks
- **Track API costs** by monitoring request patterns
- **Watch system resources** to prevent overload
- **Set up alerts** for proactive issue detection
- **Use historical data** to plan capacity
