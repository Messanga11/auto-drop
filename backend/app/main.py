from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.exceptions import AppException, exception_handler
from app.api.routes import scraping, scoring, creatives, orders, campaigns, webhooks, health
from app.api.routes.admin import auth as admin_auth
from app.middleware.rate_limit import RateLimitMiddleware
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI app with OpenAPI documentation
app = FastAPI(
    title="Plateforme Dropshipping Automatisée API",
    version="1.0.0",
    description="API pour la gestion automatisée de produits dropshipping",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register exception handlers
app.add_exception_handler(AppException, exception_handler)

# Add error handler middleware
from app.middleware.error_handler import error_handler_middleware
app.middleware("http")(error_handler_middleware)

# Add rate limiting middleware
app.add_middleware(RateLimitMiddleware, requests_per_minute=60)

# Register routers
app.include_router(health.router)
app.include_router(scraping.router)
app.include_router(scoring.router)
app.include_router(creatives.router)
app.include_router(orders.router)
app.include_router(campaigns.router)
app.include_router(webhooks.router)

# Admin routes
app.include_router(admin_auth.router, prefix="/admin", tags=["admin"])

# Import admin routes
from app.api.routes.admin import dashboard as admin_dashboard
from app.api.routes.admin import websocket as admin_websocket
from app.api.routes.admin import products as admin_products
from app.api.routes.admin import campaigns as admin_campaigns
from app.api.routes.admin import creatives as admin_creatives

app.include_router(admin_dashboard.router, prefix="/admin", tags=["admin"])
app.include_router(admin_websocket.router, prefix="/admin", tags=["admin"])
app.include_router(admin_products.router, prefix="/admin", tags=["admin"])
app.include_router(admin_campaigns.router, prefix="/admin", tags=["admin"])
app.include_router(admin_creatives.router, prefix="/admin", tags=["admin"])

# Import admin actions and orders routes
from app.api.routes.admin import actions as admin_actions
from app.api.routes.admin import orders as admin_orders

app.include_router(admin_actions.router, prefix="/admin", tags=["admin"])
app.include_router(admin_orders.router, prefix="/admin", tags=["admin"])


@app.on_event("startup")
async def startup_event():
    """Startup event handler"""
    logger.info("Starting application...")
    
    # Validate required environment variables
    from app.config import settings
    required_vars = [
        "database_url",
        "redis_url",
    ]
    missing_vars = [var for var in required_vars if not getattr(settings, var, None)]
    if missing_vars:
        logger.warning(f"Missing environment variables: {missing_vars}")
    
    # Seed default admin user
    try:
        from app.scripts.seed_admin import seed_admin_user
        await seed_admin_user()
    except Exception as e:
        logger.warning(f"Failed to seed admin user: {e}")
    
    # Start scheduler for monthly scraping
    from app.scheduler import start_scheduler
    start_scheduler()


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler"""
    from app.cache import close_redis
    from app.scheduler import scheduler
    await close_redis()
    scheduler.shutdown()
    logger.info("Shutting down application...")


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Plateforme Dropshipping Automatisée API", "version": "1.0.0"}


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}

