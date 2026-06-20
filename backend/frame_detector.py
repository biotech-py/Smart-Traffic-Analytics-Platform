from ultralytics import YOLO
import cv2
import numpy as np
import base64

model = YOLO("yolov8n.pt")

vehicle_classes = [
    "car",
    "bus",
    "truck",
    "motorcycle"
]

def detect_frame(image_bytes):

    np_arr = np.frombuffer(
        image_bytes,
        np.uint8
    )

    frame = cv2.imdecode(
        np_arr,
        cv2.IMREAD_COLOR
    )

    results = model(
        frame,
        conf=0.5,
        imgsz=320,
        verbose=False
    )

    vehicle_count = 0

    cars = 0
    bikes = 0
    buses = 0
    trucks = 0

    for box in results[0].boxes:

        cls_id = int(box.cls[0])

        class_name = model.names[cls_id]

        if class_name not in vehicle_classes:
            continue

        vehicle_count += 1

        if class_name == "car":
            cars += 1

        elif class_name == "motorcycle":
            bikes += 1

        elif class_name == "bus":
            buses += 1

        elif class_name == "truck":
            trucks += 1

    traffic_status = "LOW"

    if vehicle_count > 5:
        traffic_status = "MEDIUM"

    if vehicle_count > 15:
        traffic_status = "HIGH"

    # ---------------------------------
    # DRAW YOLO BOXES
    # ---------------------------------

    annotated = results[0].plot()

    cv2.putText(
        annotated,
        f"Vehicles: {vehicle_count}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.putText(
        annotated,
        f"Traffic: {traffic_status}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 255),
        2
    )

    # ---------------------------------
    # CONVERT TO BASE64
    # ---------------------------------

    _, buffer = cv2.imencode(
        ".jpg",
        annotated
    )

    image_base64 = base64.b64encode(
        buffer
    ).decode("utf-8")

    return {
        "vehicle_count": vehicle_count,
        "traffic_status": traffic_status,
        "cars": cars,
        "bikes": bikes,
        "buses": buses,
        "trucks": trucks,
        "image": image_base64
    }
