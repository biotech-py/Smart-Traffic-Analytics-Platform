from ultralytics import YOLO
import cv2
import math

# Load YOLO model
model = YOLO("yolov8n.pt")

# Video Source
cap = cv2.VideoCapture("uploads/traffic.mp4")

# Vehicle Classes
vehicle_classes = [
    "car",
    "bus",
    "truck",
    "motorcycle"
]

# Tracking
vehicle_tracks = {}
next_vehicle_id = 0
entered_count = 0

# Counting Line
line_y = 350

while True:

    success, frame = cap.read()

    if not success:
        break

    results = model(frame)

    annotated_frame = frame.copy()

    vehicle_count = 0

    car_count = 0
    bike_count = 0
    bus_count = 0
    truck_count = 0

    current_tracks = {}

    for box in results[0].boxes:

        cls_id = int(box.cls[0])
        class_name = model.names[cls_id]

        if class_name not in vehicle_classes:
            continue

        vehicle_count += 1

        if class_name == "car":
            car_count += 1

        elif class_name == "motorcycle":
            bike_count += 1

        elif class_name == "bus":
            bus_count += 1

        elif class_name == "truck":
            truck_count += 1

        x1, y1, x2, y2 = map(
            int,
            box.xyxy[0]
        )

        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2

        matched_id = None

        for track_id, (prev_x, prev_y) in vehicle_tracks.items():

            distance = math.sqrt(
                (center_x - prev_x) ** 2 +
                (center_y - prev_y) ** 2
            )

            if distance < 50:
                matched_id = track_id
                break

        if matched_id is None:

            matched_id = next_vehicle_id

            next_vehicle_id += 1

        current_tracks[matched_id] = (
            center_x,
            center_y
        )

        # Count crossing line
        if matched_id in vehicle_tracks:

            prev_y = vehicle_tracks[matched_id][1]

            if prev_y < line_y and center_y >= line_y:

                entered_count += 1

        # Bounding Box
        cv2.rectangle(
            annotated_frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        # Vehicle ID
        cv2.putText(
            annotated_frame,
            f"{class_name} ID:{matched_id}",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

        # Center Dot
        cv2.circle(
            annotated_frame,
            (center_x, center_y),
            5,
            (0, 0, 255),
            -1
        )

    vehicle_tracks = current_tracks

    # Traffic Density
    if vehicle_count < 5:
        traffic_status = "Low"

    elif vehicle_count < 15:
        traffic_status = "Medium"

    else:
        traffic_status = "High"

    # Counting Line
    cv2.line(
        annotated_frame,
        (0, line_y),
        (frame.shape[1], line_y),
        (0, 255, 255),
        3
    )

    # Dashboard Text
    cv2.putText(
        annotated_frame,
        f"Vehicles: {vehicle_count}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2
    )

    cv2.putText(
        annotated_frame,
        f"Traffic: {traffic_status}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 0, 0),
        2
    )

    cv2.putText(
        annotated_frame,
        f"Entered: {entered_count}",
        (20, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 0),
        2
    )

    cv2.putText(
        annotated_frame,
        f"Cars: {car_count}",
        (20, 160),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    cv2.putText(
        annotated_frame,
        f"Bikes: {bike_count}",
        (20, 190),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 0),
        2
    )

    cv2.putText(
        annotated_frame,
        f"Buses: {bus_count}",
        (20, 220),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 0, 255),
        2
    )

    cv2.putText(
        annotated_frame,
        f"Trucks: {truck_count}",
        (20, 250),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 165, 255),
        2
    )

    cv2.imshow(
        "Live Vehicle Tracking",
        annotated_frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

