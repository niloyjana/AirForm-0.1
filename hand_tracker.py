import cv2
import mediapipe as mp
import math

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

        self.prev_dist = None
        self.fingertips = [4, 8, 12, 16, 20]

    # ---------- MAIN ----------
    def get_data(self, frame):
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        rx = ry = 0.0
        scale = 1.0
        fist = False
        pinch = False

        # glow buffers
        glow = frame * 0
        core = frame * 0

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb)

        if result.multi_hand_landmarks:
            hands = result.multi_hand_landmarks
            handedness = result.multi_handedness

            # ---------- ZOOM ----------
            if len(hands) == 2:
                p1 = hands[0].landmark[8]
                p2 = hands[1].landmark[8]
                dist = math.hypot(p1.x - p2.x, p1.y - p2.y)
                if self.prev_dist:
                    scale = 1.0 + (dist - self.prev_dist) * 2.0
                self.prev_dist = dist
            else:
                self.prev_dist = None

            # ---------- ROTATION ----------
            lm0 = hands[0].landmark
            rx = -(lm0[9].y - 0.5) * 0.08
            ry = (lm0[9].x - 0.5) * 0.08

            folded = sum(1 for t in [8,12,16,20] if lm0[t].y > lm0[t-2].y)
            fist = folded >= 4

            # ---------- DRAW ----------
            for hand_lm, info in zip(hands, handedness):
                label = info.classification[0].label

                # ----- Fingertip hollow glow rings -----
                for idx in self.fingertips:
                    p = hand_lm.landmark[idx]
                    px, py = int(p.x * w), int(p.y * h)

                    # glow ring (thick)
                    cv2.circle(glow, (px, py), 12, (255,255,255), 3, cv2.LINE_AA)
                    # core ring (thin)
                    cv2.circle(core, (px, py), 8, (255,255,255), 1, cv2.LINE_AA)

                # ---------- LEFT HAND PINCH LINE ----------
                if label == "Left":
                    t = hand_lm.landmark[4]
                    i = hand_lm.landmark[8]

                    tx, ty = int(t.x * w), int(t.y * h)
                    ix, iy = int(i.x * w), int(i.y * h)

                    d = math.hypot(t.x - i.x, t.y - i.y)
                    pinch = d < 0.035

                    # glow line
                    cv2.line(glow, (tx, ty), (ix, iy),
                             (255,255,255), 6, cv2.LINE_AA)

                    # core line
                    cv2.line(core, (tx, ty), (ix, iy),
                             (255,255,255), 2, cv2.LINE_AA)

        # ---------- COMPOSE ----------
        glow = cv2.GaussianBlur(glow, (0,0), 8)
        frame = cv2.addWeighted(frame, 1.0, glow, 0.22, 0)
        frame = cv2.addWeighted(frame, 1.0, core, 1.0, 0)

        return frame, rx, ry, scale, fist, pinch
