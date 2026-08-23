# Phantom 👻

> [!WARNING]
> **DISCLAIMER: For Educational Purposes Only**
> This project was created strictly for educational purposes and harmless pranking. **Do NOT run these scripts on someone else's computer maliciously or without their explicit consent.**

**Phantom** is a collection of stealthy, unkillable audio prank scripts and a comprehensive Android application designed to randomly trigger audio files based on background interactions.

---

## The Phantom Android App

The Phantom Android app is a transparent, consent-based, offline background prank application. It uses hardware sensors and system broadcasts to trigger random audio clips while running seamlessly in the background.

### What Phantom Does
When armed, Phantom continuously monitors enabled background triggers (like shaking the device, flipping it, or plugging in a charger). Whenever an enabled trigger occurs, Phantom randomly selects a bundled audio clip and plays it out loud. 

### Trigger System
Any enabled trigger independently triggers a random audio file. You do not need to perform all of them; an *OR* relationship applies.
- **Shake**: Detects vigorous device shaking using the accelerometer.
- **Flip / Rotate**: Detects when the device is flipped completely over.
- **Tilt**: Detects when the device is tilted past a steep angle.
- **Quick Spin / Twist**: Detects rapid rotational movement using the gyroscope.
- **Charger Connected / Disconnected**: Triggers when a power cable is plugged in or removed.
- **Bluetooth Connected / Disconnected**: Triggers when a Bluetooth device connects or disconnects.
- **Motion Pattern**: (Configurable) Triggers only after a sequence of motions.

### Privacy Guarantee
Phantom is built with strict privacy constraints. It is entirely offline and harmless.
- **No Accessibility Service**: It does not intercept system-wide UI interactions.
- **No Keylogging**: It does not monitor keyboard input.
- **No Screen Recording**: It does not take screenshots or read screen contents.
- **No Analytics / Telemetry**: It does not upload any sensor or usage data to any server.
- **No Network Requests**: The app operates 100% offline.
- **No Sensitive Access**: It does not request access to your contacts, microphone, camera, SMS, or location.

### Usage
1. **Install Phantom** by downloading the APK from the GitHub Releases page.
2. **Open Phantom**.
3. **Configure Triggers**: Tap `TRIGGER SETTINGS` to turn on/off the hardware sensors or broadcast events you want to listen to.
4. **Arm the Prank**: Press `START PRANK`. The app is now armed and running as a sticky background service.
5. **Leave the App**: You can now swipe Phantom away or lock your screen.
6. **Trigger the Prank**: Perform any enabled trigger (e.g., shake your phone). A random audio file will play!
7. **Repeat**: Perform another trigger to stop the current audio and instantly play a new random file.
8. **Stop Audio**: Press `STOP AUDIO` to halt the current playback (but keep the prank armed).
9. **Stop Prank**: Press `STOP PRANK` to completely disarm Phantom, unregister all sensors, and halt the background service.

### Building
The Phantom Android APK is built entirely in the cloud using **GitHub Actions**. You do not need Android Studio, Gradle, or a local SDK installed to compile this project!
- Any push to the `main` branch automatically triggers the `.github/workflows/build-apk.yml` workflow.
- The workflow provisions an Ubuntu runner, sets up Python, installs Buildozer, and compiles the `.apk`.
- The final binary is uploaded as a GitHub Artifact and appended to the GitHub Release page for immediate download.

---

## Desktop Pranks

### 1. Prank 1: Infinite Loop (`prank_1_infinite_loop`)
A cross-platform, zero-dependency script that embeds an audio payload natively within the script itself using Base64 encoding.

### 2. Prank 2: Input Trigger (`prank_2_input_trigger`)
A Python-based daemon that silently monitors for global inputs (specifically the `Enter` key or any mouse click) and plays a random audio file from its directory every time the user interacts with their system.

## Stopping the Desktop Pranks

Because the desktop scripts are engineered to be resilient against standard user attempts to close them (`Ctrl+C` or closing the terminal), you **must** use forceful termination signals. See the [TROUBLESHOOTING.md](TROUBLESHOOTING.md) guide for exact commands to kill the phantom processes on your specific operating system.
