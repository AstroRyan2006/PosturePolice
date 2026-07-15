import cv2
import mediapipe as mp
import math
import time
import subprocess 

# ---------------------------------------------------------
# MEDIAPIPE INITIALIZATION (Posture Detection)
# ---------------------------------------------------------
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Camera Initialization (Index 0)
cap = cv2.VideoCapture(0)

# ---------------------------------------------------------
# CALIBRATION & SYSTEM VARIABLES
# ---------------------------------------------------------
calibrated = False
baseline_face_width = 0
baseline_neck_height = 0
calibration_start_time = time.time()

# Cooldown system to prevent spamming your computer
last_alert_time = 0
alert_cooldown = 10  # Seconds between each system/voice notification

print("🚨 Posture Daemon activated. Sit straight for calibration (5s)...")

# ---------------------------------------------------------
# MAIN LOOP
# ---------------------------------------------------------
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read camera.")
        break

    # Mirror effect for a natural feel
    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape
    
    # MediaPipe requires RGB colors
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)
    
    if results.pose_landmarks:
        lm = results.pose_landmarks.landmark
        
        # 1. Extract Keypoints (Nose, Ears, Shoulders)
        nose = lm[mp_pose.PoseLandmark.NOSE]
        ear_l = lm[mp_pose.PoseLandmark.LEFT_EAR]
        ear_r = lm[mp_pose.PoseLandmark.RIGHT_EAR]
        shoulder_l = lm[mp_pose.PoseLandmark.LEFT_SHOULDER]
        shoulder_r = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER]

        # 2. Convert to real pixels based on window size
        ny = int(nose.y * h)
        elx, ely = int(ear_l.x * w), int(ear_l.y * h)
        erx, ery = int(ear_r.x * w), int(ear_r.y * h)
        
        # Center point between shoulders
        sy = int((shoulder_l.y + shoulder_r.y) * h / 2)
        
        # 3. Calculate Current Metrics
        # - Face Width = Depth (Too close to screen)
        current_face_width = math.hypot(elx - erx, ely - ery)
        # - Neck Height (Shoulders -> Nose) = Slouching
        current_neck_height = sy - ny 
        
        # =========================================================
        # PHASE 1: CALIBRATION (First 5 seconds)
        # =========================================================
        if not calibrated:
            elapsed = time.time() - calibration_start_time
            countdown = 5 - int(elapsed)
            
            if countdown > 0:
                cv2.putText(frame, f"CALIBRATION: {countdown}s (Sit straight!)", 
                            (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
            else:
                # Lock in baseline data
                baseline_face_width = current_face_width
                baseline_neck_height = current_neck_height
                calibrated = True
                print("✅ Calibration complete! Script is now running in the background.")
                
        # =========================================================
        # PHASE 2: MONITORING & ALERTS
        # =========================================================
        else:
            # Posture tolerances
            is_too_close = current_face_width > (baseline_face_width * 1.30) # 30% wider = too close
            is_slouching = current_neck_height < (baseline_neck_height * 0.80) # 20% shorter = slouching
            
            if is_too_close or is_slouching:
                current_time = time.time()
                
                # Check Cooldown (10s)
                if current_time - last_alert_time > alert_cooldown:
                    # Switch text to English for correct TTS pronunciation
                    msg = "You are too close to the screen!" if is_too_close else "Sit up straight!"
                    
                    # Alert 1: Native Linux Pop-up
                    subprocess.run(["notify-send", "-u", "critical", "-t", "5000", "🚨 POSTURE ALERT 🚨", msg])
                    
                    # Alert 2: Robotic Voice
                    subprocess.run(["spd-say", msg])
                    
                    last_alert_time = current_time
                    print(f"⚠️ Alert triggered: {msg}")
                    
                # Alert 3: Violently blur the camera feed
                frame = cv2.GaussianBlur(frame, (99, 99), 0)
                warning_text = "TOO CLOSE!" if is_too_close else "SIT UP STRAIGHT!"
                cv2.putText(frame, warning_text, (50, h//2), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 5)
            
            else:
                # Correct posture = Green Display
                cv2.putText(frame, "Posture: OK", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # ---------------------------------------------------------
    # WINDOW DISPLAY (Comment out to make invisible)
    # ---------------------------------------------------------
    cv2.imshow("Posture Police (Jarvis V3)", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
# Cleanup on exit
cap.release()
cv2.destroyAllWindows()
