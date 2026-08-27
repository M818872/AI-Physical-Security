import cv2
import os
import numpy as np
import time
import winsound
from datetime import datetime

# ==========================================================
# FOLDERS
# ==========================================================

AUTHORIZED_DIR = "authorized_faces"
ALERT_DIR = "alerts"
EVIDENCE_DIR = "evidence"
LOG_DIR = "logs"

os.makedirs(AUTHORIZED_DIR, exist_ok=True)
os.makedirs(ALERT_DIR, exist_ok=True)
os.makedirs(EVIDENCE_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "security.log")

# ==========================================================
# SETTINGS
# ==========================================================

CONFIDENCE_THRESHOLD = 70
ALERT_COOLDOWN = 5

last_alert_time = 0

# ==========================================================
# FACE DETECTOR
# ==========================================================

detector = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

if detector.empty():
    print("ERROR: Could not load face detector.")
    exit()

# ==========================================================
# FACE RECOGNIZER
# ==========================================================

recognizer = cv2.face.LBPHFaceRecognizer_create()

faces = []
labels = []
names = []

current_label = 0

# ==========================================================
# LOAD AUTHORIZED FACES
# ==========================================================

print("================================")
print(" Loading Authorized Faces")
print("================================")

for filename in os.listdir(AUTHORIZED_DIR):

    if not filename.lower().endswith(
        (".jpg", ".jpeg", ".png", ".bmp")
    ):
        continue

    path = os.path.join(AUTHORIZED_DIR, filename)

    image = cv2.imread(
        path,
        cv2.IMREAD_GRAYSCALE
    )

    if image is None:
        print("Could not read:", filename)
        continue

    detected = detector.detectMultiScale(
        image,
        scaleFactor=1.3,
        minNeighbors=5
    )

    if len(detected) == 0:
        print("No face found:", filename)
        continue

    x, y, w, h = detected[0]

    face = image[y:y+h, x:x+w]

    faces.append(face)
    labels.append(current_label)

    name = os.path.splitext(filename)[0]
    names.append(name)

    print("Loaded:", name)

    current_label += 1

# ==========================================================
# CHECK DATABASE
# ==========================================================

if len(faces) == 0:

    print()
    print("ERROR: No authorized faces found.")
    print("Add an image to:")
    print("authorized_faces/")
    exit()

# ==========================================================
# TRAIN
# ==========================================================

recognizer.train(
    faces,
    np.array(labels)
)

print()
print("Authorized people:")

for name in names:
    print("-", name)

print()
print("================================")
print(" SECURITY CAMERA")
print("================================")
print("Press Q to quit.")
print()

# ==========================================================
# CAMERA
# ==========================================================

camera = cv2.VideoCapture(0)

if not camera.isOpened():

    print("ERROR: Camera could not be opened.")
    exit()

# ==========================================================
# FUNCTION: CREATE UNAUTHORIZED ALERT
# ==========================================================

def create_alert(frame):

    timestamp = datetime.now()

    readable_time = timestamp.strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    file_time = timestamp.strftime(
        "%Y%m%d_%H%M%S"
    )

    # ------------------------------------------------------
    # Evidence
    # ------------------------------------------------------

    evidence_file = os.path.join(
        EVIDENCE_DIR,
        f"unauthorized_{file_time}.jpg"
    )

    cv2.imwrite(
        evidence_file,
        frame
    )

    # ------------------------------------------------------
    # Alert file
    # ------------------------------------------------------

    alert_file = os.path.join(
        ALERT_DIR,
        f"alert_{file_time}.txt"
    )

    with open(
        alert_file,
        "w",
        encoding="utf-8"
    ) as alert:

        alert.write(
            "PHYSICAL SECURITY ALERT\n"
        )

        alert.write(
            "=======================\n"
        )

        alert.write(
            f"Time: {readable_time}\n"
        )

        alert.write(
            "Status: UNAUTHORIZED\n"
        )

        alert.write(
            "Action: ACCESS DENIED\n"
        )

        alert.write(
            f"Evidence: {evidence_file}\n"
        )

    # ------------------------------------------------------
    # Security log
    # ------------------------------------------------------

    with open(
        LOG_FILE,
        "a",
        encoding="utf-8"
    ) as log:

        log.write(
            f"{readable_time} | "
            f"ACCESS DENIED | "
            f"UNKNOWN PERSON | "
            f"Evidence: {evidence_file} | "
            f"Alert: {alert_file}\n"
        )

    # ------------------------------------------------------
    # Console
    # ------------------------------------------------------

    print()
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("       SECURITY ALERT")
    print("       UNAUTHORIZED PERSON")
    print("       ACCESS DENIED")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("Evidence:", evidence_file)
    print("Alert:", alert_file)
    print("Log:", LOG_FILE)
    print()

    # ------------------------------------------------------
    # Windows sound
    # ------------------------------------------------------

    try:
        winsound.Beep(1200, 700)
        winsound.Beep(1200, 700)
    except:
        pass

# ==========================================================
# MAIN LOOP
# ==========================================================

while True:

    ret, frame = camera.read()

    if not ret:
        print("Camera error.")
        break

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    detected_faces = detector.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5
    )

    for x, y, w, h in detected_faces:

        face = gray[y:y+h, x:x+w]

        label, confidence = recognizer.predict(face)

        # ==================================================
        # AUTHORIZED
        # ==================================================

        if (
            confidence < CONFIDENCE_THRESHOLD
            and 0 <= label < len(names)
        ):

            name = names[label]

            text = f"ACCESS GRANTED: {name}"

            color = (0, 255, 0)

            # Log only once every 5 seconds
            current_time = time.time()

            if current_time - last_alert_time >= ALERT_COOLDOWN:

                timestamp = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                with open(
                    LOG_FILE,
                    "a",
                    encoding="utf-8"
                ) as log:

                    log.write(
                        f"{timestamp} | "
                        f"ACCESS GRANTED | "
                        f"Person: {name}\n"
                    )

                print(
                    f"[AUTHORIZED] {name}"
                )

                last_alert_time = current_time

        # ==================================================
        # UNAUTHORIZED
        # ==================================================

        else:

            text = "ACCESS DENIED"

            color = (0, 0, 255)

            current_time = time.time()

            # IMPORTANT:
            # Create alert immediately when cooldown expires

            if (
                current_time - last_alert_time
                >= ALERT_COOLDOWN
            ):

                create_alert(frame)

                last_alert_time = current_time

        # ==================================================
        # DRAW BOX
        # ==================================================

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            color,
            2
        )

        cv2.putText(
            frame,
            text,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            color,
            2
        )

    # ======================================================
    # CAMERA WINDOW
    # ======================================================

    cv2.imshow(
        "Company Security Verification",
        frame
    )

    # ======================================================
    # QUIT
    # ======================================================

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# ==========================================================
# CLEANUP
# ==========================================================

camera.release()
cv2.destroyAllWindows()

print()
print("Security monitor stopped.")
