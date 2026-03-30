import cv2
import time
from hand_tracker import HandTracker
from cube_sim import CubeSim

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

tracker = HandTracker()
cube = CubeSim()

# ---------- SHAPE SWITCH LOCK ----------
shape_lock = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame, rx, ry, scale, fist, pinch = tracker.get_data(frame)

    # rotation
    cube.angle_x += rx
    cube.angle_y += ry

    # scale
    cube.scale *= scale
    cube.scale = max(0.6, min(1.6, cube.scale))

    # spin
    cube.update_spin(fist)

    # ---------- FIXED SHAPE SWITCH ----------
    if pinch and not shape_lock:
        cube.next_shape()
        shape_lock = True

    if not pinch:
        shape_lock = False

    cube.draw(frame)

    cv2.imshow("Gesture Controlled 3D Shapes", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
