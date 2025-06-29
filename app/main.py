# app/main.py
from fastapi import FastAPI
from app.routers import ai, metrics, notify, assets
from app.data.mqtt_client import start_mqtt
from app.data.mqtt_feeder import start_publisher
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers import dashboard
from app.auth.auth_router import router as auth_router
from app.routers import sensors
from app.routers import charts
from app.routers import equipment_map


app = FastAPI(title="AssetOpsAI")

# Mount static and template directories
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.on_event("startup")
async def startup_event():
    start_mqtt()
    start_publisher()

app.include_router(ai.router, prefix="/ai")
app.include_router(metrics.router, prefix="/metrics")
app.include_router(notify.router, prefix="/notify")
app.include_router(assets.router, prefix="/assets")
app.include_router(sensors.router)
app.include_router(charts.router)
app.include_router(equipment_map.router)
# Include routes
app.include_router(dashboard.router)
app.include_router(auth_router)
