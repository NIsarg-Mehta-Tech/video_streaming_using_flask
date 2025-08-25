from database import *
from flask import Flask, render_template, request, redirect, url_for, session, Response
from dotenv import dotenv_values
from face_detection import FaceDetector
import cv2 as cv

config_env = {
    **dotenv_values(".env.secret")
}

# Initialize DB when Flask starts
init_db()

app = Flask(__name__, template_folder="templates", static_folder="static")

app.secret_key = config_env.get("Dev", "fallback-secret")

# Load credentials
VALID_EMAIL = config_env.get("EMAIL")
VALID_PASSWORD = config_env.get("PASSWORD")

detector = FaceDetector()
cap = cv.VideoCapture(0)

face_counter = get_next_face_counter()


@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email == VALID_EMAIL and password == VALID_PASSWORD:
            session["user"] = email
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid email or password"

    return render_template("login.html", error=error)

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=session["user"])


@app.route("/video_feed")
def video_feed():
    def generate():
        global face_counter
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame, cropped_faces = detector.detect_faces(frame)

            if cropped_faces:
                conn = get_connection()
                cursor = conn.cursor()
                for cropped in cropped_faces:
                    face_counter += 1
                    face_name = f"face_{face_counter}"
                    _, buffer = cv.imencode(".jpg", cropped)
                    face_bytes = buffer.tobytes()

                    query = f"INSERT INTO `{TABLE_NAME}` (face_name, face) VALUES (%s, %s)"
                    cursor.execute(query, (face_name, face_bytes))

                conn.commit()
                cursor.close()
                conn.close()



            # Encode frame as JPEG
            _, jpeg = cv.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)

