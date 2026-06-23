import os
from datetime import datetime
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
from video_classifier import (
    detect_video_type
)
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
app.mount(
    "/input",
    StaticFiles(directory="Input"),
    name="input"
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

    file_path = f"Input/{video.filename}"

    with open(
        file_path,
        "wb"
    ) as buffer:

        buffer.write(
            await video.read()
        )


        video_type = detect_video_type(
    file_path
)
    if video_type == "REDLIGHT":
        subprocess.run(
            ["python", "video_redlight_detector.py"])
    else:
        subprocess.run(
            ["python", "video_detector.py"]
    )

    return{
        "message":
        "Phan tich video hoan tat"
        }

@app.get("/violations")
async def violations_page(
    request: Request,
    date: str = None
):
    violations = get_all_violations()
    if date:
        violations = [

        v for v in violations

        if str(
            v["violation_time"].date()
        ) == date

    ]

    today_count = 0
    lane_count = 0
    redlight_count = 0

    today = datetime.now().date()

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

        violation_date = violation[
            "violation_time"
        ].date()

        if violation_date == today:

            today_count += 1

            if (
                violation["violation_type"]
                == "Di Sai Lan"
            ):
                lane_count += 1

            elif (
                violation["violation_type"]
                == "Vuot Den Do"
            ):
                redlight_count += 1

    return templates.TemplateResponse(
        request=request,
        name="violation_list.html",
        context={
            "violations": violations,
            "today_count": today_count,
            "lane_count": lane_count,
            "redlight_count": redlight_count,
            "selected_date": date
        }
    )

@app.get("/live")
async def live_page(
    request: Request
):

    videos = []

    for file in os.listdir("Input"):

        if file.endswith(".mp4"):

            videos.append(file)

    return templates.TemplateResponse(
        request=request,
        name="live.html",
        context={
            "videos": videos
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
