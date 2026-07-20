# AtmoSync: Micro-Climate Arbitrage Analytics

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Kafka](https://img.shields.io/badge/Apache_Kafka-Streaming-black?logo=apachekafka)
![Snowflake](https://img.shields.io/badge/Snowflake-Data_Warehouse-29B5E8?logo=snowflake)
![dbt](https://img.shields.io/badge/dbt-Transformation-FF694B?logo=dbt)
![FastAPI](https://img.shields.io/badge/FastAPI-REST_APIs-009688?logo=fastapi)
![React](https://img.shields.io/badge/React-18.2-61DAFB?logo=react)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)

> **Enterprise Cold-Chain Streaming Analytics & Machine Learning Platform**  
> Continuous container-level micro-climate monitoring, Arrhenius spoilage prediction, financial loss estimation, and automated market arbitrage rerouting.

---

## 📌 Executive Summary & Business Problem

Traditional agricultural supply chains lose billions annually due to cargo degradation during sea and highway transit. Refrigerated containers (*reefers*) experience micro-climate thermal variations, humidity spikes, and compressor failures that standard external weather forecasts cannot detect.

**AtmoSync** solves this by delivering an end-to-end streaming intelligence platform that:
1. **Monitors Micro-Climates**: Captures 1-second IoT telemetry (temperature, humidity, door breaches, battery, GPS speed, market spot prices).
2. **Predicts Spoilage Risk**: Computes real-time Arrhenius chemical quality decay, Remaining Shelf Life (RSL), and XGBoost spoilage probability.
3. **Calculates Financial Loss**: Quantifies cargo value at risk ($) and carbon footprint tax liabilities.
4. **Detects Arbitrage Opportunities**: Evaluates regional spot market price differentials vs rerouting transport costs to recommend profitable port diversions.
5. **Pushes Live Alerts**: Dispatches multi-channel webhooks to Slack and Email when thresholds breach.
6. **Adaptive Dataset Pipeline**: Automatically inspects user-provided external datasets (CSV/Parquet), detecting data types, missing values, duplicates, and column semantics without hardcoding.

---

## 🏗️ End-to-End System Architecture

```
+------------------------+      +------------------------+      +------------------------+
|  IoT Sensor Simulator  | ---> |  Apache Kafka Stream   | ---> |  FastAPI REST Backend  |
|  (Micro-Climate 1Hz)   |      | (Producer / DLQ / Cons)|      |   & WebSockets Server  |
+------------------------+      +------------------------+      +------------------------+
                                            |                               |
                                            v                               v
                                +------------------------+      +------------------------+
                                |  Snowflake Data Lake   |      | React Executive UI     |
                                |  RAW -> STG -> MART    |      | (Glassmorphism Dashboard)|
                                +------------------------+      +------------------------+
                                            |                               
                                            v                               
                                +------------------------+                  
                                |   dbt Data Models &    |                  
                                |  Airflow Orchestration |                  
                                +------------------------+                  
```

---

## 📂 Repository Structure

```
d:\AtmoSync\
├── frontend/             # React 18 + Vite + Glassmorphic UI + Recharts + Leaflet Maps
├── backend/              # FastAPI REST APIs, JWT Auth, WebSockets, Export Engine (PDF, Excel, PPTX)
├── simulator/            # IoT Sensor Telemetry Generator (Arrhenius kinetics, GPS, weather)
├── kafka/                # Kafka Producer, Consumer, DLQ Handler, Topic Configs & Validation
├── analytics/            # Micro-Climate Core Engine (Spoilage, Shelf Life, Arbitrage, Loss calculation)
├── ml/                   # Machine Learning Models (XGBoost Classifier, Price Forecast, SHAP Explainability)
├── snowflake/            # Snowflake DDLs (RAW, STAGING, ANALYTICS, CDC Streams, Tasks, RBAC)
├── dbt/                  # dbt Data Transformation Models (Staging, Marts, Schema tests)
├── airflow/              # Apache Airflow Orchestration DAGs
├── dashboards/           # Apache Superset Dashboard Export JSON & Configuration Specs
├── sql/                  # PostgreSQL Schema & Analytical Queries (Window functions)
├── reports/              # PDF / Excel / PowerPoint / CSV Report Generation Engine
├── docs/                 # Technical Specifications (Architecture, API, Snowflake, Kafka, dbt, Analytics)
├── docker/               # Production Dockerfiles for microservices
├── tests/                # Comprehensive Pytest Suite (Unit, API, ML, Simulator)
├── docker-compose.yml    # Full Multi-container Orchestration
└── README.md             # Project Showcase Documentation
```

---

## ⚡ Quick Start & Installation

### Option 1: Run via Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/enterprise/atmosync.git
cd atmosync

# Spin up all containers (Kafka, Postgres, Redis, Backend, Frontend, Simulator)
docker-compose up --build -d
```

Access the interfaces:
- **React Executive Dashboard UI**: `http://localhost`
- **FastAPI OpenAPI Swagger**: `http://localhost:8000/docs`

---

### Option 2: Local Development Setup

#### 1. Setup Python Backend Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start FastAPI Backend Server
python -m uvicorn backend.main:app --reload --port 8000
```

#### 2. Setup React Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## 🧪 Verification & Testing Suite

Run the full automated pytest suite:

```bash
pytest tests/ -v
```

---

## 📜 License & Portfolio Author
Built for Enterprise Cold-Chain Streaming Analytics & Portfolio Showcase.
