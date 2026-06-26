# 🚦 Smart Traffic Analytics Platform

A Full-Stack AI-powered Traffic Analytics Platform that performs real-time vehicle detection, counting, and traffic monitoring using **YOLOv8**, **FastAPI**, and **React**.

The platform allows users to upload traffic videos, automatically detect multiple vehicle classes, generate processed videos, and visualize traffic statistics through an interactive dashboard.

---

## 🌐 Live Demo

**Frontend:** https://smart-traffic-analytics-platform.vercel.app/

---

## 📸 Project Preview

> *(Add screenshots here after uploading them to the repository.)*

```
images/
│── dashboard.png
│── upload-page.png
│── processed-video.png
```

Example:

```markdown
![Dashboard](images/dashboard.png)

![Upload Page](images/upload-page.png)
```

---

# Features

- 🚗 Real-time Vehicle Detection
- 🚙 Multi-class Vehicle Classification
- 📈 Live Traffic Statistics
- 🎥 Video Upload & Processing
- 📊 Interactive Dashboard
- ⚡ FastAPI REST API
- 🌐 React Frontend
- 🤖 YOLOv8 Deep Learning Model
- 📁 Processed Video Download
- 📱 Responsive UI

---

# Tech Stack

## Frontend

- React
- Vite
- JavaScript
- CSS

## Backend

- FastAPI
- Python
- Uvicorn

## AI / Computer Vision

- YOLOv8 (Ultralytics)
- OpenCV
- NumPy

## Deployment

- Vercel (Frontend)
- Render (Backend)

---

# Project Structure

```
Smart-Traffic-Analytics-Platform/
│
├── backend/
│   ├── app.py
│   ├── traffic.py
│   ├── requirements.txt
│   └── outputs/
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── Procfile
├── render.yaml
├── requirements.txt
└── README.md
```

---

# Workflow

```
Traffic Video
       │
       ▼
Upload via React UI
       │
       ▼
FastAPI Backend
       │
       ▼
YOLOv8 Vehicle Detection
       │
       ▼
Vehicle Counting
       │
       ▼
Traffic Analysis
       │
       ▼
Processed Video + Dashboard
```

---

# Vehicle Classes

The model detects:

- Car
- Bus
- Truck
- Motorcycle
- Bicycle

---

# Dashboard Metrics

The application provides:

- Total Vehicles
- Cars
- Buses
- Trucks
- Motorcycles
- Bicycles
- Vehicles per Minute
- Traffic Density
- Traffic Status

---

# Installation

## Clone Repository

```bash
git clone https://github.com/biotech-py/Smart-Traffic-Analytics-Platform.git

cd Smart-Traffic-Analytics-Platform
```

---

## Backend

```bash
cd backend

pip install -r requirements.txt

uvicorn app:app --reload
```

Runs at

```
http://localhost:8000
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

Runs at

```
http://localhost:5173
```

---

# API Endpoints

## Upload Video

```
POST /upload
```

Uploads a traffic video for analysis.

---

## Analyze Video

```
POST /analyze
```

Runs YOLOv8 inference on the uploaded video.

---

## Download Output

```
GET /outputs/{filename}
```

Returns the processed video.

---

# Sample Output

The processed video contains:

- Vehicle Bounding Boxes
- Vehicle Labels
- Live Vehicle Count
- Traffic Status
- Vehicles per Minute

---

# Performance

| Metric | Value |
|---------|--------|
| Detection Model | YOLOv8n |
| Backend | FastAPI |
| Frontend | React |
| Average FPS | Real-time (hardware dependent) |
| Supported Formats | MP4, AVI, MOV |

---

# Future Improvements

- Live CCTV Streaming
- Multi-camera Support
- Traffic Congestion Prediction
- Vehicle Speed Estimation
- License Plate Recognition
- Accident Detection
- Heatmap Visualization
- Cloud Storage Integration
- Admin Dashboard
- Analytics Reports

---

# Learning Outcomes

This project demonstrates experience with:

- Full-Stack Development
- REST API Development
- Computer Vision
- Deep Learning
- Object Detection
- React Development
- FastAPI
- Deployment
- Video Processing
- AI Integration

---

# Author

**Nirupam Joarder**

B.Tech Biotechnology  
National Institute of Technology Rourkela

**LinkedIn**

https://www.linkedin.com/in/nirupam-joarder/

**GitHub**

https://github.com/biotech-py

---

# License

This project is licensed under the MIT License.

---

⭐ If you found this project useful, consider giving it a star!
