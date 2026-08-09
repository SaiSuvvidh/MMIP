import cv2
import numpy as np

# Load video
cap = cv2.VideoCapture('1.webm')

# Get properties
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print(f"Video FPS: {fps}, Total frames: {total_frames}")

# Compute motion scores
prev_frame = None
motion_scores = []
frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)  # blur to reduce noise
    if prev_frame is not None:
        diff = cv2.absdiff(gray, prev_frame)
        thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        motion = np.sum(thresh) / 255  # count white pixels
        motion_scores.append((frame_count, motion))
    prev_frame = gray
    frame_count += 1

cap.release()

if motion_scores:
    peak_frame, _ = max(motion_scores, key=lambda x: x[1])
    print(f"Peak motion at frame: {peak_frame}")

    # Slow motion for 4 seconds around peak (2 before, 2 after)
    slow_start = max(0, peak_frame - int(2 * fps))
    slow_end = min(total_frames, peak_frame + int(2 * fps))

    print(f"Slowing frames {slow_start} to {slow_end}")

    # Process the whole video
    cap = cv2.VideoCapture('1.webm')
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # start from beginning

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('slomo1.mp4', fourcc, fps, (width, height))

    slow_factor = 2  # slow down by factor 2

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if slow_start <= frame_count < slow_end:
            # Slow motion: write frame multiple times
            for _ in range(slow_factor):
                out.write(frame)
        else:
            # Normal speed
            out.write(frame)
        frame_count += 1

    out.release()
    cap.release()

    print("Highlight video created: slomo1.mp4")
else:
    print("No motion detected")
