import cv2
import os

AUTHORIZED_DIR = "authorized_faces"

# Face detector
detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# Face recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

faces = []
labels = []
names = []

# Load every image from authorized_faces
for label, filename in enumerate(os.listdir(AUTHORIZED_DIR)):

    path = os.path.join(AUTHORIZED_DIR, filename)

    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        continue

    detected = detector.detectMultiScale(image, 1.3, 5)

    if len(detected) == 0:
        print("No face found:", filename)
        continue

    x, y, w, h = detected[0]

    face = image[y:y+h, x:x+w]

    faces.append(face)
    labels.append(label)

    name = os.path.splitext(filename)[0]
    names.append(name)

    print("Loaded:", name)


if not faces:
    print("No authorized faces found!")
    print("Put employee images inside:", AUTHORIZED_DIR)
    exit()


# Train recognizer using all authorized images
recognizer.train(faces, __import__("numpy").array(labels))

print("\nAuthorized people:")
for name in names:
    print("-", name)

print("\nStarting security camera...\n")


camera = cv2.VideoCapture(0)

while True:

    ret, frame = camera.read()

    if not ret:
        print("Camera error")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    detected = detector.detectMultiScale(gray, 1.3, 5)

    for x, y, w, h in detected:

        face = gray[y:y+h, x:x+w]

        label, confidence = recognizer.predict(face)

        # Lower confidence = better match
        if confidence < 70:

            name = names[label]

            text = f"AUTHORIZED: {name}"
            box_color = (0, 255, 0)

        else:

            text = "UNAUTHORIZED"
            box_color = (0, 0, 255)

        cv2.rectangle(
            frame,
            (x, y),
            (x+w, y+h),
            box_color,
            2
        )

        cv2.putText(
            frame,
            text,
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            box_color,
            2
        )

    cv2.imshow("Company Security Verification", frame)

    # Q = exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


camera.release()
cv2.destroyAllWindows()