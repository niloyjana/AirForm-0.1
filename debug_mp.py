import sys
import mediapipe as mp
print(f"Python: {sys.version}")
print(f"Path: {sys.path}")
print(f"MediaPipe File: {mp.__file__}")
print(f"MediaPipe Version: {getattr(mp, '__version__', 'Unknown')}")
print(f"MediaPipe Attributes: {dir(mp)}")
try:
    print(f"MediaPipe Solutions: {mp.solutions}")
except Exception as e:
    print(f"Error accessing mp.solutions: {e}")
