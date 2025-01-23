from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os
from pathlib import Path

class VideoServer:
    def __init__(self):
        self.app = FastAPI()
        self.setup_routes()

    def setup_routes(self):
        @self.app.get("/{full_path:path}")
        async def serve_video(full_path: str):
            if not os.path.isfile(f"/{full_path}"):
                raise HTTPException(status_code=404, detail="File not found")
            
            return FileResponse(
                f"/{full_path}",
                media_type="video/mp4",
                filename=Path(full_path).name
            )
