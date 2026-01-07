from fastapi import FastAPI
from app.db import engine
from app.models import Base  # importa tudo pelo __init__.py

from app.routers.catalog_products import router as catalog_products
from app.routers.catalog_vehicles import router as catalog_vehicles
from app.routers.catalog_applications import router as catalog_applications
from app.routers.companies import router as companies
from app.routers.company_products import router as company_products
from app.routers.inventory import router as inventory
from app.routers.tax import router as tax
from app.routers.seed import router as seed_router

app = FastAPI(title="Superarch PDV API", version="1.0.0")

Base.metadata.create_all(bind=engine)

app.include_router(catalog_products)
app.include_router(catalog_vehicles)
app.include_router(catalog_applications)
app.include_router(companies)
app.include_router(company_products)
app.include_router(inventory)
app.include_router(tax)
app.include_router(seed_router)
