import logging
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from app.services.document_parser import DocumentParser
from app.services.leaseboost_service import LeaseBoostService
from app.utils.file_cleanup import FileCleanupService
from app.config import Settings
from pathlib import Path
from datetime import datetime
from app.models.schemas import LeaseAnalysisResponse

def create_logger():
    Path("logs").mkdir(exist_ok=True)

    launch_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = f"logs/leaseboost_service_{launch_date}.log"

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

    logger = logging.getLogger(__name__)

    return logger



app = FastAPI(
    title="LeaseBoost API",
    version="1.0.0",
    descriptiion="API for intelligent lease analysis",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Services
app_logger = create_logger()

file_cleanup_service = FileCleanupService(logger=app_logger)

leaseboost_service = LeaseBoostService(openai_api_key=Settings.openai_api_key, legifrance_client_id=Settings.legifrance_client_id,
                                        legifrance_client_secret=Settings.legifrance_client_secret, logger=app_logger)
document_parser = DocumentParser(logger=app_logger)




@app.on_event("startup")
async def startup_event():
    #file_cleanup_service.start_cleanup_scheduler() # in memory for now
    app_logger.info("LeaseBoost Service started")

@app.on_event("shutdown")
async def shutdown_event():
    #file_cleanup_service.stop_cleanup_scheduler() # in memory for now
    app_logger.info("LeaseBoost Service stopped")

@app.get("/")
async def root():
    return {
        "message": "LeaseBoost MVP API",
        "version": "1.0.0",
        "features": [
            "🏢 Market Intelligence & Benchmark",
            "⚖️ Legal Compliance & Alerts",  
            "💰 Financial Optimization"
        ]
    }

@app.post("/api/analyze-lease", response_model=LeaseAnalysisResponse)
async def analyze_lease(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    # 1. file validation
    app_logger.info(f"New file upload: {file.filename}")
    if file.content_type not in [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ]:
        raise HTTPException(status_code=400, detail="Invalid file format")

    file_content = await file.read()

    if len(file_content) > Settings.max_file_size_mb * 1024 * 1024:
        raise HTTPException(status_code=400, 
                            detail="File size limit exceeded. Maximun is {Settings.max_file_size_mb}MB")

    # 2. file processing
    app_logger.info(f"Processing file: {file.filename}")
    extracted_text = await document_parser.extract_text_from_file(file_content, file.filename)

    if not extracted_text or len(extracted_text.strip()) < 200:
        raise HTTPException(status_code=400, detail="Invalid file content : text too short, check that your file contains readable text")

    # 3. analysis
    app_logger.info(f"Starting analysis for file: {file.filename}")
    try:
        analysis_results = await leaseboost_service.analyze_lease(extracted_text, background_tasks)

        return analysis_results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f" Error during analysis:{str(e)}")

@app.get("/api/health")
async def health_check():
    return {
        "status": "OK",
        "service": "LeaseBoost Service",
        "features_active": [
            "Market Intelligence",
            "Legal Compliance", 
            "Financial Optimization"
        ]
    }

