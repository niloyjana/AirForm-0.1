# 🦾 AirForm-0.1: Gesture-Controlled 3D Shapes

A premium, interactive 3D shape simulator that uses **Computer Vision** and **MediaPipe** to allow touchless control of geometric point-clouds directly from your webcam.

![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.10-green)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-orange)

---

## ✨ Features

- 🧊 **Dynamic 3D Shapes**: Cycle through Cube, Cuboid, Sphere, Tetrahedron (Fixed!), Cone, and Cylinder.
- 🖐️ **Intuitive Gestures**:
  - **Rotate**: Move your hand to rotate the 3D projection on the X and Y axes.
  - **Scale**: Use two hands to "pull" or "push" the shape to zoom in and out.
  - **Spin**: Close your hand into a **Fist** to apply a continuous Z-axis momentum.
  - **Switch Shape**: Use a **Pinch** gesture (Left Hand: Index + Thumb) to instantly cycle shapes.
- 🎨 **Visual Excellence**:
  - Point-cloud rendering with glassmorphism-inspired glow effects.
  - Real-time HUD with animated property labels.
  - Smooth LERP-based transitions and rotations.

---
## DEMO


https://github.com/user-attachments/assets/3eadc67d-d311-4772-9185-8386b0169b92



## 🚀 Getting Started

### Prerequisites
> [!IMPORTANT]
> **Python 3.10** is required. MediaPipe currently has stability issues with Python 3.14+ on some systems.

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/niloyjana/AirForm-0.1.git
   cd AirForm-0.1
   ```

2. **Create a Virtual Environment (Recommended)**:
   ```powershell
   # Windows
   py -3.10 -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

---

## 🎮 How to Run

Execute the main controller script:
```powershell
python main.py
```

### Controls Guide
| Gesture | Action |
| :--- | :--- |
| **Hand Movement** | Rotate X / Y |
| **Fist** | High-speed Spin |
| **Left Hand Pinch** | Next Shape |
| **Two Hands (Distance)** | Scale / Zoom |
| **Esc Key** | Exit Application |

---

## 🛠️ Tech Stack

- **MediaPipe**: Hand landmark detection and gesture tracking.
- **OpenCV**: Camera I/O and custom 2D-to-3D projection rendering.
- **NumPy**: High-performance mathematical operations for coordinate transformations.
- **PyOpenGL**: (Optional/Future) Extended hardware-accelerated rendering.

---

## 🐞 Troubleshooting

- **AttributeError: module 'mediapipe' has no attribute 'solutions'**: This usually means you are running a Python version (like 3.14) that MediaPipe 0.10.x doesn't support yet. **Please use Python 3.10.**
- **Laggy Performance**: Ensure your lighting is consistent. High-contrast backgrounds can sometimes confuse the hand tracker.


---
*Created with ❤️ by Niloy Jana*
