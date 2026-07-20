# AtmoSync REST API Specification

## Base URL
`http://localhost:8000/api`

## Interactive OpenAPI Documentation
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Key Endpoints

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/dashboard/summary` | `GET` | Returns executive KPIs, cargo valuation, and high-risk container counts |
| `/api/containers` | `GET` | Returns all active reefer containers with micro-climate status |
| `/api/containers/{id}` | `GET` | Returns detailed telemetry history and diagnostics for specific container |
| `/api/spoilage` | `GET` | Returns Arrhenius kinetics spoilage risk breakdown |
| `/api/arbitrage` | `GET` | Returns profitable market rerouting opportunities |
| `/api/routes` | `GET` | Returns live GPS coordinates for Mapbox/Leaflet interactive map |
| `/api/forecast/prices` | `GET` | Returns 7-day spot market price trend forecasts |
| `/api/alerts` | `GET` | Returns active operational cold-chain alerts |
| `/api/alerts/trigger` | `POST` | Dispatches alert notifications to Slack/Email webhooks |
| `/api/ml/metrics` | `GET` | Returns XGBoost classifier accuracy, precision, recall, & ROC-AUC |
| `/api/ml/predict` | `POST` | Evaluates spoilage probability for custom container event |
| `/api/ml/shap` | `POST` | Computes local SHAP feature importance breakdown |
| `/api/reports/download` | `GET` | Downloads downloadable report in PDF, Excel, PPTX, CSV, or JSON |
| `/api/inspect-dataset` | `POST` | Uploads CSV/Parquet dataset for dynamic schema detection |
