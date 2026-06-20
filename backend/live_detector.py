from ultralytics import YOLO
import cv2

# Load YOLO model
model = YOLO("yolov8n.pt")

# Webcam
cap = cv2.VideoCapture(0)

# Vehicle classes from COCO dataset
vehicle_classes = [
    "car",
    "bus",
    "truck",
    "motorcycle"
]

while True:

    success, frame = cap.read()

    if not success:
        break

    # Run YOLO
    results = model(frame)

    # Copy frame for drawing
    annotated_frame = frame.copy()

    # Vehicle counter
    vehicle_count = 0

    # Loop through detections
    for box in results[0].boxes:

        cls_id = int(box.cls[0])
        class_name = model.names[cls_id]

        if class_name in vehicle_classes:

            vehicle_count += 1

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0]
            )

            # Bounding box
            cv2.rectangle(
                annotated_frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            # Vehicle label
            cv2.putText(
                annotated_frame,
                class_name,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

    # Traffic Density Classification
    if vehicle_count < 5:
        traffic_status = "LOW"

    elif vehicle_count < 15:
        traffic_status = "MEDIUM"

    else:
        traffic_status = "HEAVY"

    # Vehicle count
    cv2.putText(
        annotated_frame,
        f"Vehicles: {vehicle_count}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2
    )

    # Traffic status
    cv2.putText(
        annotated_frame,
        f"Traffic: {traffic_status}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 0, 0),
        2
    )

    # Display frame
    cv2.imshow(
        "Live Traffic Detection",
        annotated_frame
    )

    # Press q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
