# Phantom (Android)

## 1. What This Project Does
This is a harmless, consent-based Android application that acts as a simple soundboard. When the user explicitly presses "Start Prank", it repeatedly plays a bundled audio file. When the user presses "Stop Prank" or exits the app, the audio stops completely.

## 2. Why Python/Kivy is Used
Python and the Kivy framework allow for rapid cross-platform UI development. Using Kivy, we can build a functional Android interface with buttons and audio playback without needing to write complex Java/Kotlin code. 

## 3. Why Android Studio is Not Required Locally
Because this project utilizes **Buildozer** inside a **GitHub Actions** workflow, all the heavy lifting of downloading the Android SDK, NDK, and compiling the `.apk` happens on GitHub's cloud servers. This saves gigabytes of local disk space and avoids complicated local environment setups.

## 4. Project Structure
```text
prank_3_android/
├── main.py              # The core Kivy Python application
├── buildozer.spec       # Configuration for compiling the APK
├── README.md            # This documentation
└── assets/
    └── prank_audio.mp3  # The audio file to be looped
```

## 5. Where to Put the Audio File
The audio file must be placed at `assets/prank_audio.mp3` within this directory. The Buildozer configuration is explicitly set to package `.mp3` files from the `assets/` directory into the final APK.

## 6. How to Build (GitHub Actions)
This project is built automatically using GitHub Actions. Because of the `.github/workflows/build-apk.yml` file in the repository root, the workflow will start **automatically** as soon as you push your code.

## 7. How to Find the Generated APK Artifact
1. Go to your repository page on GitHub.
2. Click on the **Actions** tab at the top.
3. Click on the most recent workflow run (e.g., "Build Android APK").
4. Scroll to the bottom of the page to find the **Artifacts** section.

## 8. How to Download the APK
Under the **Artifacts** section, click on `Friends-App-APK` (or Phantom). It will download as a `.zip` file containing the compiled `.apk`. Extract the `.zip` file on your computer to get the APK.

## 9. How to Install it on an Android Phone
1. Transfer the `.apk` file to your Android phone (via USB, email, Google Drive, etc.).
2. On your phone, tap the `.apk` file to install it.
3. If prompted, you may need to allow "Install unknown apps" from the source you are opening it from (like your File Manager or Browser).
4. Tap **Install**.

## 10. How to Start the Prank
Open the "Phantom" app on your phone and tap the big green **Start Prank** button. The status text will change to "Playing" and the audio will loop continuously.

## 11. How to Stop the Prank
Tap the red **Stop Prank** button. The audio will cease immediately and the status text will change to "Stopped". Alternatively, you can tap **Exit** to cleanly close the app and stop the audio.

## 12. Android Permissions
This app requests **zero special permissions** (no microphone, no camera, no location, no storage access). It is completely self-contained. The only permission automatically added by the build system is basic `INTERNET` access (standard for most engines), but the app does not actually download or upload any data. The `.mp3` is bundled internally as an asset.
