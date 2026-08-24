# Phantom Release Signing

This document outlines the secure, automated pipeline for building and signing Phantom release APKs using GitHub Actions.

## 1. Why Secure Release Signing?
A release keystore is your digital identity as a developer. 
- **Back it up securely:** If you lose this keystore or the passwords, you will be **permanently unable to update the application** for existing users, as Android requires updates to be signed with the exact same key.
- **Play Protect:** Note that simply signing an APK does not guarantee that Google Play Protect will not flag the application. However, properly signing the app is a mandatory requirement for distribution outside of a debug environment.

## 2. Generating the Release Keystore
If you do not already have a release keystore, generate one using the Java `keytool` utility (do this securely on your local machine, **never** in a public environment):

```bash
keytool -genkey -v -keystore phantom-release.keystore -alias phantom_alias -keyalg RSA -keysize 2048 -validity 10000
```
*You will be prompted to enter a Keystore Password and a Key Password.*

## 3. Converting the Keystore to Base64
To securely upload this binary keystore to GitHub Secrets, convert it to a Base64 string:

**Linux / macOS:**
```bash
base64 -i phantom-release.keystore > keystore_base64.txt
```

**Windows (PowerShell):**
```powershell
[convert]::ToBase64String((Get-Content -path "phantom-release.keystore" -Encoding byte)) > keystore_base64.txt
```

## 4. Configuring GitHub Secrets
Navigate to your repository on GitHub -> **Settings** -> **Secrets and variables** -> **Actions** -> **New repository secret**.

You must configure the following exactly:

1. **`ANDROID_KEYSTORE_BASE64`**: The entire contents of `keystore_base64.txt`.
2. **`ANDROID_KEY_ALIAS`**: The alias used during generation (e.g., `phantom_alias`).
3. **`ANDROID_KEYSTORE_PASSWORD`**: The password for the keystore.
4. **`ANDROID_KEY_PASSWORD`**: The password for the specific key.

## 5. How the GitHub Actions Workflow Works
The `.github/workflows/android-release.yml` pipeline automates the release securely:
1. It is triggered manually via **workflow_dispatch**.
2. It decodes `ANDROID_KEYSTORE_BASE64` back into a temporary file on the GitHub runner.
3. It passes the credentials securely into Buildozer via environment variables (`P4A_RELEASE_KEYSTORE`, etc.).
4. The Buildozer compilation runs `assembleRelease` equivalent, generating a signed APK.
5. The pipeline uses `apksigner` to strictly verify the signature.
6. The public SHA-256 certificate fingerprint is extracted and printed in the logs (passwords and private keys are never exposed).
7. The temporary keystore and any sensitive properties are immediately deleted.
8. The securely signed APK is uploaded as an artifact and attached to a new GitHub Release.

## 6. How to Trigger a Release Manually
1. Go to the **Actions** tab in your GitHub repository.
2. Select **Android Release Build** on the left sidebar.
3. Click the **Run workflow** dropdown on the right.
4. Enter the `Version Name` (e.g., 4.1), `Version Code`, and `Release Notes`.
5. Click **Run workflow**.

## 7. Verifying the Resulting APK
You can download the `phantom-release-apk` artifact from the workflow run summary. You can verify it yourself locally by running:
```bash
apksigner verify --verbose --print-certs phantom-release.apk
```

## 8. Extracting the SHA-256 Fingerprint
The pipeline automatically extracts the public SHA-256 fingerprint and prints it at the end of the workflow run. If you need to do this manually:
```bash
keytool -printcert -jarfile phantom-release.apk
```
