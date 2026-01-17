import os
import shutil
from typing import Optional

UPLOAD_ROOT = os.path.join("backend", "images", "uploads")
os.makedirs(UPLOAD_ROOT, exist_ok=True)

class Storage:
    def save(self, fileobj, destination: str):
        temp_path = destination + ".tmp"
        with open(temp_path, "wb") as f:
            shutil.copyfileobj(fileobj, f)
        os.replace(temp_path, destination)

    def delete(self, path: str):
        if os.path.exists(path):
            os.remove(path)

    def ensure_dir(self, path: str):
        os.makedirs(path, exist_ok=True)

    def url_for(self, filename: str, product_id: Optional[int] = None) -> str:
        if product_id:
            return f"/static/uploads/product_{product_id}/{filename}"
        return f"/static/uploads/{filename}"

storage = Storage()
