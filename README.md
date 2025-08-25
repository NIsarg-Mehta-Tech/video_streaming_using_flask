Here’s a **professional README** you can use for your GitHub project:

---

# Flask Live Face Detection with MySQL Storage

This project is a **Flask web application** that performs **real-time face detection** using OpenCV's **YuNet model**, streams live video to the dashboard, and saves cropped faces into a **MySQL database**.

---

## Features

* **Authentication:** Login system using credentials stored in a `.env` file.
* **Live Face Detection:** Detects faces from a webcam or video file in real-time.
* **Video Streaming:** Stream live video with bounding boxes on detected faces directly in the Flask dashboard.
* **Database Integration:** Stores cropped face images in MySQL with unique names.
* **Modular Design:** Separate files for database handling, face detection, and Flask app.

---

## Project Structure

```
flask_app/
│── app.py               # Main Flask app
│── face_detection.py    # YuNet face detection logic
│── database.py          # Database initialization and helper functions
│── .env.secret          # Environment variables
│── templates/
│    ├── login.html
│    └── dashboard.html
│── static/
```

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd flask_app
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate    # Linux/macOS
venv\Scripts\activate       # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Dependencies include:

* Flask
* python-dotenv
* OpenCV (`opencv-python` & `opencv-contrib-python`)
* gdown
* mysql-connector-python

---

### 4. Configure environment variables

Create a `.env.secret` file:

```env
# Flask secret key
Dev=your-flask-secret-key

# Login credentials
EMAIL=your-email@example.com
PASSWORD=your-password

# MySQL database
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your-mysql-password
DB_NAME=face_db
TABLE_NAME=faces
```

---

### 5. Run the app

```bash
python app.py
```

* Open browser at [http://127.0.0.1:5000](http://127.0.0.1:5000)
* Login with the credentials from `.env.secret`
* Dashboard will show **live video feed with face detection**
* Cropped faces are automatically saved in MySQL.

---

## Notes

* **Model Download:** The YuNet model (`face_detection_yunet.onnx`) is automatically downloaded when the app runs.
* **Database Initialization:** `database.py` handles creating the database and table if they don’t exist.
* **Video Source:** You can change the video input in `app.py`:

cap = cv2.VideoCapture(0)       # For webcam
cap = cv2.VideoCapture("prof1.mp4")  # For video file




Do you want me to create that too?
