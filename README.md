# AI Physical Security Monitor

> AI-assisted physical security monitoring system for real-time face detection and authorized-person verification.

---

## 📌 Overview

**AI Physical Security Monitor** is a lightweight computer-vision-based security system designed to demonstrate how AI can be used for physical security monitoring.

The system uses a camera to detect a person's face and compares it against a collection of authorized reference images.

Based on the verification result, the system identifies the person as:

- ✅ **AUTHORIZED**
- 🚨 **UNAUTHORIZED**

For an unauthorized detection, the system can generate a security alert and store evidence and security logs.

The project is designed as a simple prototype of the type of camera-based verification device that could be used at a company entrance, server room, laboratory, restricted office, or other controlled area.

---

# 🎯 Project Objective

The main objective of this project is to demonstrate the integration of:

- Artificial Intelligence
- Computer Vision
- Face Detection
- Face Verification
- Physical Security Monitoring
- Security Alerts
- Evidence Collection
- Security Logging

The system provides a simple foundation that can later be extended into a larger physical security platform.

---

# ✨ Features

- Real-time camera monitoring
- Face detection
- Face verification
- Authorized face collection
- Authorized / unauthorized status
- Security alerts
- Evidence capture
- Security event logging
- Local processing
- Simple Python implementation
- Webcam support
- Easy-to-understand project structure

---

# 🔄 How the System Works

The system follows this workflow:

```text
                    START
                      │
                      ▼
             ┌─────────────────┐
             │ Load Authorized │
             │     Faces       │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ Open Camera     │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ Face Detection  │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ Face Verification│
             └────────┬────────┘
                      │
                ┌─────┴─────┐
                │           │
              MATCH       NO MATCH
                │           │
                ▼           ▼
          ┌──────────┐  ┌─────────────┐
          │AUTHORIZED│  │UNAUTHORIZED │
          └────┬─────┘  └──────┬──────┘
               │                │
               ▼                ▼
            SECURE          SECURITY ALERT
                                 │
                                 ▼
                         ┌───────────────┐
                         │   EVIDENCE    │
                         │   + LOGGING   │
                         └───────────────┘
```

## 1. Clone the Repository

Open **Command Prompt**, PowerShell, or a terminal.

Run:

```bash
git clone https://github.com/M818872/AI-Physical-Security.git
```

Then enter the project directory:

```bash
cd AI-Physical-Security
```

---

## 2. Install Python Requirements

Install the required Python packages:

```bash
py -m pip install -r requirement.txt
```

If your computer uses `python` instead of `py`, use:

```bash
python -m pip install -r requirement.txt
```

---

## 3. Add Authorized People

The project uses the:

```text
authorized_faces/
```

folder to store reference images of people who are allowed to access the protected area.

Place the authorized person's image inside this folder.

### Example

```text
authorized_faces/
│
├── employee_01.jpg
├── employee_02.jpg
└── employee_03.jpg
```

These images are used as the local authorized reference collection.

### Example Scenario

Suppose a company has three employees who are authorized to enter a restricted server room.

The administrator can place their reference images inside:

```text
authorized_faces/
├── employee_01.jpg
├── employee_02.jpg
└── employee_03.jpg
```

The camera can then verify people against this collection.

> **Privacy:** Do not upload real employee photographs or biometric data to a public GitHub repository. Users should add their own authorized images locally after downloading the project.

---

## 4. Connect a Camera

Connect a webcam to your computer.

You can use:

- Laptop built-in camera
- USB webcam
- Other supported camera input

The camera acts as the security device.

---

## 5. Start the Program

Run:

```bash
py security_monitor.py
```

Or:

```bash
python security_monitor.py
```

The camera window will open and the security monitor will begin processing the camera feed.

---

## 6. Person Appears in Front of the Camera

When someone appears in front of the camera, the system detects the face.

The process is:

```text
Camera
   ↓
Face Detected
   ↓
Face Verification
   ↓
Compare With Authorized Faces
   ↓
Security Decision
```

```

# 📁 Project Structure

```text
AI-Physical-Security/
│
├── alerts/
│   └── .gitkeep
│
├── authorized_faces/
│   └── .gitkeep
│
├── employees/
│   └── .gitkeep
│
├── evidence/
│   └── .gitkeep
│
├── logs/
│   └── .gitkeep
│
├── dataset/
│
├── security_monitor.py
│
├── requirement.txt
│
└── README.md
