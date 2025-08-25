import os
import gdown
import cv2

#  Put your model file ID here (NOT folder ID)
DRIVE_ID = "1qxVftZnJketO6D84R36KxzCBPw0GnyJV"
URL = f"https://drive.google.com/uc?id={DRIVE_ID}"
MODEL_PATH = "face_detection_yunet.onnx"

class FaceDetector:
    def __init__(self):
        # Download YuNet model if not already downloaded
        if not os.path.isfile(MODEL_PATH):
            print("Downloading YuNet ONNX model...")
            gdown.download(URL, MODEL_PATH, quiet=False)

        # Load YuNet model

        self.detector = cv2.FaceDetectorYN.create(
            model=MODEL_PATH,
            config="",
            input_size=(640, 480),
            score_threshold=0.6,
            nms_threshold=0.3,
            top_k=5000
        )

    def detect_faces(self, frame):
        h, w, _ = frame.shape

        frame_resized = cv2.resize(frame, (640, 480))
        self.detector.setInputSize((frame_resized.shape[1], frame_resized.shape[0]))
        _, faces = self.detector.detect(frame_resized)

        cropped_faces = []

        if faces is not None:
            for face in faces:
                x, y, w, h = face[:4].astype(int)
                cv2.rectangle(frame_resized, (x, y), (x + w, y + h), (0, 255, 0), 2)

                x, y = max(0, x), max(0, y)
                cropped_face = frame_resized[y:y + h, x:x + w]

                if cropped_face.size > 0:
                    cropped_faces.append(cropped_face)

        return frame_resized, cropped_faces