import cv2
import time
from modules.detector import ObjectDetector
from modules.ai_helper import AIHelper
from modules.speaker import Speaker

def main():
    detector = ObjectDetector()
    ai = AIHelper()
    speaker = Speaker()

    cap = cv2.VideoCapture(0)

    last_spoken = {}
    cooldown = 20  # seconds before repeating object

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        detections, annotated = detector.detect(frame)

        for obj in detections:
            now = time.time()
            if obj not in last_spoken or (now - last_spoken[obj]) > cooldown:
                fact = ai.explain(obj)
                print(f"[INFO] {obj}: {fact}")
                speaker.say(fact)
                last_spoken[obj] = now

        cv2.imshow("Context-Aware Virtual Guide", annotated)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
