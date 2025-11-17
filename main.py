from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from models.model_manager import ModelManager
from services.cache_service import CacheService
from utils.analytics import usage_analytics
from utils.rate_limiter import rate_limiter
from fastapi.responses import JSONResponse
from utils.monitor import get_system_resource_usage

app = FastAPI()

AVAILABLE_MODELS = ["llama2", "codellama"]

manager = ModelManager(AVAILABLE_MODELS)
cache = CacheService()

class QueryRequest(BaseModel):
    prompt: str
    model: str

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    if not rate_limiter.is_allowed(client_ip):
        return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})
    response = await call_next(request)
    return response

@app.middleware("http")
async def add_analytics(request: Request, call_next):
    response = await call_next(request)
    if request.url.path == "/query" and request.method == "POST":
        try:
            body = await request.json()
            model = body.get("model", "unknown")
        except Exception:
            model = "unknown"
        usage_analytics.record_request(model, "/query")
    return response

@app.get("/")
def read_root():
    return {"message": "Local LLM API Gateway is running."}

@app.post("/query")
def query_model(req: QueryRequest):
    if req.model not in AVAILABLE_MODELS:
        raise HTTPException(status_code=400, detail="Unknown model")
    cached = cache.get(req.prompt, req.model)
    if cached:
        return {"response": cached, "cached": True}
    try:
        response = manager.generate(req.model, req.prompt)
        cache.set(req.prompt, req.model, response)
        return {"response": response, "cached": False}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/usage")
def get_usage():
    return usage_analytics.get_usage()

@app.get("/monitor")
def system_monitor():
    usage = get_system_resource_usage()
    return usage
