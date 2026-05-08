import json
import re
import uuid
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile


router = APIRouter(prefix="/api/media", tags=["Destination Media"])

UPLOAD_ROOT = Path(__file__).resolve().parents[2] / "uploads" / "destination-media"
MAX_IMAGE_BYTES = 8 * 1024 * 1024
MAX_VIDEO_BYTES = 120 * 1024 * 1024


def clean_slug(slug: str) -> str:
    cleaned = re.sub(r"[^a-z0-9-]", "", slug.lower().strip())
    if not cleaned:
        raise HTTPException(status_code=400, detail="Invalid destination slug")
    return cleaned


def destination_dir(slug: str) -> Path:
    path = UPLOAD_ROOT / clean_slug(slug)
    path.mkdir(parents=True, exist_ok=True)
    return path


def media_index_path(slug: str) -> Path:
    return destination_dir(slug) / "media.json"


def load_media(slug: str) -> list[dict]:
    index_path = media_index_path(slug)
    if not index_path.exists():
        return []
    try:
        return json.loads(index_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def save_media(slug: str, items: list[dict]) -> None:
    media_index_path(slug).write_text(
        json.dumps(items, indent=2),
        encoding="utf-8",
    )


def public_file_url(slug: str, filename: str) -> str:
    return f"/uploads/destination-media/{clean_slug(slug)}/{filename}"


async def store_upload(slug: str, upload: UploadFile, media_type: str) -> dict:
    if media_type == "image":
        if not upload.content_type or not upload.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Only image files are allowed")
        max_bytes = MAX_IMAGE_BYTES
    else:
        if not upload.content_type or not upload.content_type.startswith("video/"):
            raise HTTPException(status_code=400, detail="Only video files are allowed")
        max_bytes = MAX_VIDEO_BYTES

    original_suffix = Path(upload.filename or "").suffix.lower()
    suffix = original_suffix if re.fullmatch(r"\.[a-z0-9]{1,8}", original_suffix) else ""
    filename = f"{uuid.uuid4().hex}{suffix}"
    file_path = destination_dir(slug) / filename

    size = 0
    with file_path.open("wb") as output:
        while chunk := await upload.read(1024 * 1024):
            size += len(chunk)
            if size > max_bytes:
                output.close()
                file_path.unlink(missing_ok=True)
                raise HTTPException(status_code=413, detail=f"{media_type.title()} file is too large")
            output.write(chunk)

    return {
        "id": uuid.uuid4().hex,
        "type": media_type,
        "source": "upload",
        "url": public_file_url(slug, filename),
        "filename": filename,
        "name": upload.filename or filename,
    }


@router.get("/destinations/{slug}")
def list_destination_media(slug: str):
    return load_media(slug)


@router.post("/destinations/{slug}/images")
async def upload_destination_images(slug: str, files: list[UploadFile] = File(...)):
    items = load_media(slug)
    new_items = [await store_upload(slug, file, "image") for file in files]
    items.extend(new_items)
    save_media(slug, items)
    return new_items


@router.post("/destinations/{slug}/video-file")
async def upload_destination_video(slug: str, file: UploadFile = File(...)):
    items = load_media(slug)
    new_item = await store_upload(slug, file, "video")
    items = [item for item in items if not (item.get("type") == "video" and item.get("source") == "upload")]
    items.append(new_item)
    save_media(slug, items)
    return new_item


@router.post("/destinations/{slug}/youtube")
def save_destination_youtube(slug: str, url: str = Form(...)):
    if not url.strip():
        raise HTTPException(status_code=400, detail="YouTube URL is required")

    items = load_media(slug)
    new_item = {
        "id": uuid.uuid4().hex,
        "type": "video",
        "source": "youtube",
        "url": url.strip(),
        "name": "YouTube video",
    }
    items = [item for item in items if not (item.get("type") == "video" and item.get("source") == "youtube")]
    items.append(new_item)
    save_media(slug, items)
    return new_item


@router.delete("/destinations/{slug}/{media_id}")
def delete_destination_media(slug: str, media_id: str):
    items = load_media(slug)
    target = next((item for item in items if item.get("id") == media_id), None)
    if not target:
        raise HTTPException(status_code=404, detail="Media item not found")

    if target.get("source") == "upload" and target.get("filename"):
        (destination_dir(slug) / target["filename"]).unlink(missing_ok=True)

    remaining = [item for item in items if item.get("id") != media_id]
    save_media(slug, remaining)
    return {"status": "deleted"}
