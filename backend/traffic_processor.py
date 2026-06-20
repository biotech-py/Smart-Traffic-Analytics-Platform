from ultralytics import YOLO
import cv2
from scipy.spatial.distance import euclidean
import os
import subprocess


def process_video(video_path):

    model = YOLO("yolov8n.pt")

    cap = cv2.VideoCapture(video_path)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps <= 0:
        fps = 30

    total_frames = int(
        cap.get(cv2.CAP_PROP_FRAME_COUNT)
    )

    os.makedirs(
        "outputs",
        exist_ok=True
    )

    # TEMP AVI FILE
    output_path = (
        "outputs/temp_output.avi"
    )

    # Much more stable on Windows
    fourcc = cv2.VideoWriter_fourcc(
        *"XVID"
    )

    out = cv2.VideoWriter(
        output_path,
        fourcc,
        fps,
        (width, height)
    )

    if not out.isOpened():

        raise Exception(
            "VideoWriter could not be opened"
        )

    vehicle_classes = [
        "car",
        "bus",
        "truck",
        "motorcycle"
    ]

    car_ids = set()
    bike_ids = set()
    bus_ids = set()
    truck_ids = set()

    traffic_status = "LOW"

    traffic_history = []

    while True:

        success, frame = cap.read()

        if not success:
            break

        results = model.track(
            frame,
            conf=0.5,
            persist=True,
            verbose=False
        )

        centers = []

        current_vehicle_count = 0

        boxes = results[0].boxes

        if boxes is not None:

            for box in boxes:

                cls_id = int(
                    box.cls[0]
                )

                class_name = (
                    model.names[cls_id]
                )

                if (
                    class_name
                    not in vehicle_classes
                ):
                    continue

                current_vehicle_count += 1

                if box.id is not None:

                    track_id = int(
                        box.id[0]
                    )

                    if class_name == "car":
                        car_ids.add(
                            track_id
                        )

                    elif (
                        class_name
                        == "motorcycle"
                    ):
                        bike_ids.add(
                            track_id
                        )

                    elif (
                        class_name
                        == "bus"
                    ):
                        bus_ids.add(
                            track_id
                        )

                    elif (
                        class_name
                        == "truck"
                    ):
                        truck_ids.add(
                            track_id
                        )

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )

                cx = (
                    x1 + x2
                ) // 2

                cy = (
                    y1 + y2
                ) // 2

                centers.append(
                    (cx, cy)
                )

        # Traffic Level

        if current_vehicle_count < 5:

            traffic_status = "LOW"

        elif current_vehicle_count < 10:

            traffic_status = "MEDIUM"

        elif current_vehicle_count < 20:

            traffic_status = "HIGH"

        else:

            traffic_status = (
                "CONGESTED"
            )

        traffic_history.append(
            current_vehicle_count
        )

        risk_count = 0

        annotated = (
            results[0].plot()
        )

        for i in range(
            len(centers)
        ):

            for j in range(
                i + 1,
                len(centers)
            ):

                distance = euclidean(
                    centers[i],
                    centers[j]
                )

                if distance < 100:

                    risk_count += 1

                    cv2.line(
                        annotated,
                        centers[i],
                        centers[j],
                        (0, 0, 255),
                        2
                    )

        if risk_count == 0:

            risk_status = "SAFE"

        elif risk_count < 3:

            risk_status = (
                "LOW RISK"
            )

        elif risk_count < 6:

            risk_status = (
                "MEDIUM RISK"
            )

        else:

            risk_status = (
                "HIGH RISK"
            )

        congestion_status = (
            "YES"
            if current_vehicle_count > 20
            else "NO"
        )

        cv2.putText(
            annotated,
            f"Vehicles: {current_vehicle_count}",
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
            (255, 255, 0),
            2
        )

        cv2.putText(
            annotated,
            f"Congestion: {congestion_status}",
            (20, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            2
        )

        cv2.putText(
            annotated,
            f"Risk: {risk_status}",
            (20, 160),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

        cv2.putText(
            annotated,
            f"Close Encounters: {risk_count}",
            (20, 200),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 0, 255),
            2
        )

        out.write(
            annotated
        )

    cap.release()
    out.release()

    unique_vehicle_count = (

        len(car_ids)
        + len(bike_ids)
        + len(bus_ids)
        + len(truck_ids)

    )

    duration_minutes = max(
        1,
        (total_frames / fps)
        / 60
    )

    vehicles_per_minute = int(
        unique_vehicle_count
        / duration_minutes
    )

    # FINAL BROWSER VIDEO

    h264_output = (
        "outputs/processed_traffic_h264.mp4"
    )

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            output_path,
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "23",
            h264_output
        ],
        check=True
    )

    print(
        "Generated:",
        h264_output
    )

    return {

        "output":
        h264_output,

        "cars":
        len(car_ids),

        "bikes":
        len(bike_ids),

        "buses":
        len(bus_ids),

        "trucks":
        len(truck_ids),

        "traffic_status":
        traffic_status,

        "vehicles_per_minute":
        vehicles_per_minute,

        "traffic_history":
        traffic_history

    }
