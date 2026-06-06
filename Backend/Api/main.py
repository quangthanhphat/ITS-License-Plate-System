"""
API Module - ITS License Plate System
Nhiệm vụ:
- Nhận request từ website
- Nhận video/hình ảnh tải lên
- Trả dữ liệu (giả) cho website trước khi kết nối các module khác
"""

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

API_PREFIX = "/api/v1"

app = FastAPI(title="ITS License Plate System API", version="1.0.0")

# Cấu hình CORS để Website (Frontend) có thể gọi tới API mà không bị chặn
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Thay bằng domain của Website
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Endpoint kiểm tra trạng thái hệ thống
@app.get("/")
def read_root():
    return {"message": "Welcome to ITS License Plate System API", "status": "Running"}

@app.get("/health") 
async def health_check():
    return { "status": "healthy" }

# 2. Endpoint nhận Video/Hình ảnh tải lên để xử lý biển số
@app.post(f"{API_PREFIX}/process-video")
async def process_video(file: UploadFile = File(...)):
    
    # Mock Data mô phỏng kết quả AI phát hiện vi phạm
    return {
        "status": "success",
        "filename": file.filename,
        "message": "Video uploaded successfully. Violation detected.",
        "result": {
            "license_plate": "51G-999.99",
            "vehicle_type": "Ô tô",
            "confidence": 0.97,
            "timestamp": "2026-06-06 11:45:00",

            # Thông tin vi phạm
            "violation": {
                "type": "Vượt đèn đỏ",
                "location": "Đường Nguyễn Gia Trí",
                "fine_amount": 500000,
                "status": "đang chờ xử lí"
            }
        }
    }

# 3. Endpoint lấy danh sách lịch sử nhận diện (Data giả để Web gọi thử)
@app.get(f"{API_PREFIX}/history")
async def get_history():

    # Mock Data mô phỏng dữ liệu lịch sử nhận diện
    mock_data = [
        {
            "id": 1,
            "license_plate": "30A-123.45",
            "vehicle_type": "Ô tô",
            "timestamp": "2026-06-06 11:00",
            "confidence": 0.95,
            "violation": {
                "type": "Chạy quá tốc độ",
                "location": "Xa lộ Hà Nội",
                "fine_amount": 700000,
                "status": "Đã xử lý"
            }
        },
        {
            "id": 2,
            "license_plate": "51G-999.99",
            "vehicle_type": "Xe máy",
            "timestamp": "2026-06-06 11:15",
            "confidence": 0.97,
            "violation": {
                "type": "Vượt đèn đỏ",
                "location": "Đường Nguyễn Gia Trí",
                "fine_amount": 500000,
                "status": "Đang chờ xử lý"
            }
        }
    ]

    return {
        "status": "success",
        "data": mock_data
    }



# Chạy Server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)