# 🚨 Posture Police

**Your AI-powered ergonomic assistant.** A lightweight, background daemon that uses computer vision to monitor your sitting posture in real-time. If you slouch or get too close to the screen, Posture Police will alert you to fix your ergonomics.

## ✨ Features
- **Local AI:** Uses Google's MediaPipe for blazing-fast, strictly local pose detection (No video is ever recorded or sent to the cloud).
- **Auto-Calibration:** Automatically adjusts to your height, desk setup, and webcam angle when you first launch it.
- **Aggressive Interventions:** Blurs your screen and sends OS-level critical alerts (and voice prompts) when you ruin your posture.
- **Cross-Platform:** Works seamlessly on Linux, Windows, and macOS.

## 🚀 Download & Installation

You don't need Python installed to run this! 
1. Go to the [Actions tab](../../actions) of this repository.
2. Click on the latest successful build.
3. Scroll down to **Artifacts** and download the `.zip` file for your operating system.
4. Extract the file and run the executable!

*(Note: On macOS and Linux, you may need to grant camera permissions and run `chmod +x` on the binary).*

## 💻 Run from Source (For Developers)

If you prefer to run the raw Python script:

1. Clone the repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/PosturePolice.git](https://github.com/YOUR_USERNAME/PosturePolice.git)
   cd PosturePolice

    Install dependencies (Requires Python 3.10+):
    Bash

pip install -r requirements.txt

Ensure you have your system's TTS engine installed (e.g., speech-dispatcher on Linux).

Run the daemon:
Bash

    python3 posture.py

🛠️ Built With

    OpenCV - Computer Vision

    MediaPipe - Pose tracking ML model

    Python 3.11

⚖️ License

Distributed under the MIT License.
