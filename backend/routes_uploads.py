from fastapi import APIRouter, UploadFile, HTTPException, BackgroundTasks
from backend.infrastructure.structured_logging import logger
import os, shutil, uuid
from typing import Optional
from backend.infrastructure.file_validation import validate_upload_file

router = APIRouter(prefix="/api/v1/uploads", tags=["uploads"])

UPLOAD_ROOT = os.path.join("backend", "images", "uploads")
os.makedirs(UPLOAD_ROOT, exist_ok=True)

def safe_filename(filename: Optional[str]) -> str:
    ext = os.path.splitext(filename or "")[1]
    return f"img_{uuid.uuid4().hex}{ext}"

@router.post("/images")
async def upload_image(file: UploadFile, background_tasks: BackgroundTasks):
    validate_upload_file(file)
    filename = safe_filename(file.filename)
    temp_path = os.path.join(UPLOAD_ROOT, f"temp_{filename}")
    final_path = os.path.join(UPLOAD_ROOT, filename)
    try:
        with open(temp_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        os.rename(temp_path, final_path)
    except Exception as e:
        try:
            logger.exception("upload.save_failed", temp_path=temp_path, final_path=final_path, error=str(e))
        except Exception:
            pass
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail="Failed to save file")
    url = f"/static/uploads/{filename}"
    return {"image_url": url, "image_id": filename}

@router.post("/products/{product_id}/image")
async def upload_product_image(product_id: int, file: UploadFile, background_tasks: BackgroundTasks):
    validate_upload_file(file)
    product_dir = os.path.join(UPLOAD_ROOT, f"product_{product_id}")
    os.makedirs(product_dir, exist_ok=True)
    filename = safe_filename(file.filename)
    temp_path = os.path.join(product_dir, f"temp_{filename}")
    final_path = os.path.join(product_dir, filename)
    try:
        with open(temp_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        os.rename(temp_path, final_path)
    except Exception as e:
        try:
            logger.exception("upload.product_save_failed", temp_path=temp_path, final_path=final_path, product_id=product_id, error=str(e))
        except Exception:
            pass
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail="Failed to save file")
    url = f"/static/uploads/product_{product_id}/{filename}"
    return {"image_url": url, "image_id": filename}

def delete_uploaded_image(image_id: Optional[str] = None, product_id: Optional[int] = None):
    if not image_id and not product_id:
        return
    if product_id and not image_id:
        # Delete entire product folder
        dir_path = os.path.join(UPLOAD_ROOT, f"product_{product_id}")
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            shutil.rmtree(dir_path)
        return
    if product_id:
        path = os.path.join(UPLOAD_ROOT, f"product_{product_id}", image_id)
    else:
        path = os.path.join(UPLOAD_ROOT, image_id)
    if os.path.exists(path):
        os.remove(path)
        if product_id:
            dir_path = os.path.dirname(path)
            if os.path.isdir(dir_path) and not os.listdir(dir_path):
                os.rmdir(dir_path)

