from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")

vehicle_classes = [
    "car",
    "bus",
    "truck",
    "motorcycle"
]

cap = cv2.VideoCapture(0)

# Counting Line
line_y = 250

# Vehicle Counter
counted_ids = set()
total_passed = 0

# Shared Stats
live_stats = {
    "vehicle_count": 0,
    "traffic_status": "LOW",
    "cars": 0,
    "bikes": 0,
    "buses": 0,
    "trucks": 0,
    "total_passed": 0
}


def generate_frames():

    global total_passed

    while True:

        success, frame = cap.read()

        if not success:
            break

        frame = cv2.resize(
            frame,
            (640, 360)
        )

        results = model.track(
            frame,
            persist=True,
            conf=0.5,
            imgsz=320,
            verbose=False
        )

        vehicle_count = 0

        car_count = 0
        bike_count = 0
        bus_count = 0
        truck_count = 0

        if results[0].boxes is not None:

            for box in results[0].boxes:

                cls_id = int(box.cls[0])

                class_name = model.names[cls_id]

                if class_name not in vehicle_classes:
                    continue

                if box.id is None:
                    continue

                track_id = int(box.id[0])

                center_y = int(
                    (
                        box.xyxy[0][1]
                        + box.xyxy[0][3]
                    ) / 2
                )

                if (
                    center_y > line_y
                    and track_id not in counted_ids
                ):
                    counted_ids.add(track_id)
                    total_passed += 1

                vehicle_count += 1

                if class_name == "car":
                    car_count += 1

                elif class_name == "motorcycle":
                    bike_count += 1

                elif class_name == "bus":
                    bus_count += 1

                elif class_name == "truck":
                    truck_count += 1

        # Traffic Status

        traffic_status = "LOW"

        if vehicle_count > 5:
            traffic_status = "MEDIUM"

        if vehicle_count > 15:
            traffic_status = "HIGH"

        # Update Shared Stats

        live_stats["vehicle_count"] = vehicle_count
        live_stats["traffic_status"] = traffic_status

        live_stats["cars"] = car_count
        live_stats["bikes"] = bike_count
        live_stats["buses"] = bus_count
        live_stats["trucks"] = truck_count

        live_stats["total_passed"] = total_passed

        # Draw YOLO Results

        annotated = results[0].plot()

        # Counting Line

        cv2.line(
            annotated,
            (0, line_y),
            (annotated.shape[1], line_y),
            (0, 255, 255),
            3
        )

        # Draw Vehicle IDs

        if results[0].boxes is not None:

            for box in results[0].boxes:

                cls_id = int(box.cls[0])

                class_name = model.names[cls_id]

                if class_name not in vehicle_classes:
                    continue

                if box.id is None:
                    continue

                track_id = int(box.id[0])

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )

                cv2.putText(
                    annotated,
                    f"ID:{track_id}",
                    (x1, y1 - 25),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 255),
                    2
                )

        # Dashboard Text

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

        cv2.putText(
            annotated,
            f"Passed: {total_passed}",
            (20, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 0),
            2
        )

        ret, buffer = cv2.imencode(
            ".jpg",
            annotated
        )

        frame_bytes = buffer.tobytes()

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + frame_bytes +
            b"\r\n"
        )