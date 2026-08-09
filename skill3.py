import cv2
from ultralytics import YOLO

# Load YOLO model
model = YOLO('yolov8n.pt')

# Open video file
cap = cv2.VideoCapture('los_angeles.mp4')

if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

# Initialize counts
counts = {"car": 0, "bus": 0, "truck": 0, "motorbike": 0}

frame_count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    if frame_count % 10 == 0:  # process every 10th frame to speed up
        results = model(frame, conf=0.5)

        for result in results:
            for box in result.boxes:
                cls = int(box.cls.item())
                label = model.names[cls]
                if label in counts:
                    counts[label] += 1

cap.release()

# Print the counts
print("Vehicle counts in los_angeles.mp4:")
for vehicle, count in counts.items():
    print(f"{vehicle.capitalize()}: {count}")
