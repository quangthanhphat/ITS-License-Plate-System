import os
import subprocess
from Database.violation_repository import (
    get_all_violations
)
from Database.vehicle_repository import (
    get_vehicle_by_id
)
from fastapi import (
    FastAPI,
    Request,
    UploadFile,
    File
)
from Database.violation_repository import (
    get_violations_by_plate
)

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# ==========================
# Static Files
# ==========================

app.mount(
    "/static",
    StaticFiles(directory="Static"),
    name="static"
)
app.mount(
    "/output",
    StaticFiles(directory="Output"),
    name="output"
)
# ==========================
# Templates
# ==========================

templates = Jinja2Templates(
    directory="Templates"
)

# ==========================
# Login Page
# ==========================

@app.get("/")
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )

# ==========================
# Citizen Dashboard
# ==========================

@app.get("/citizen")
async def citizen(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="citizen_home.html"
    )

# ==========================
# Admin Dashboard
# ==========================

@app.get("/admin")
async def admin(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="admin_home.html"
    )

# ==========================
# Upload Video Page
# ==========================

@app.get("/upload-video")
async def upload_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="upload_video.html"
    )

# ==========================
# Upload Video
# ==========================

@app.post("/upload-video")
async def upload_video(
    video: UploadFile = File(...)
):

    os.makedirs(
        "Input",
        exist_ok=True
    )

    file_path = "Input/demo.mp4"

    with open(
        file_path,
        "wb"
    ) as buffer:

        buffer.write(
            await video.read()
        )
    subprocess.run(
        ["python", "video_detector.py"]
        )
    return{
        "message":
        "Phan tich video hoan tat"
        }
@app.get("/violations")
async def violations_page(
    request: Request
):

    violations = get_all_violations()

    for violation in violations:

        vehicle = get_vehicle_by_id(
            violation["vehicle_id"]
        )

        if vehicle:

            violation[
                "license_plate"
            ] = vehicle[
                "license_plate"
            ]

        else:

            violation[
                "license_plate"
            ] = "Unknown"

    return templates.TemplateResponse(
        request=request,
        name="violation_list.html",
        context={
            "violations": violations
        }
    )
@app.get("/search")
async def search_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="search_violation.html"
    )


@app.post("/search")
async def search_result(
    request: Request
):

    form = await request.form()

    license_plate = form.get(
        "license_plate"
    )

    violations = (
        get_violations_by_plate(
            license_plate
        )
    )

    return templates.TemplateResponse(
        request=request,
        name="search_violation.html",
        context={
            "violations": violations,
            "license_plate": license_plate
        }
    )