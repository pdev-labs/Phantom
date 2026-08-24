[app]

title = Phantom Combined
package.name = phantomcombined
package.domain = org.phantom.combined

# (str) Application versioning
version = 1.0

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,mp3

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy==2.3.0,plyer

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
# We only need standard permissions, maybe INTERNET if buildozer defaults to it, but none explicit required for local audio
android.permissions = FOREGROUND_SERVICE, WAKE_LOCK, POST_NOTIFICATIONS, FOREGROUND_SERVICE_MEDIA_PLAYBACK, BLUETOOTH, BLUETOOTH_CONNECT, BATTERY_STATS, MODIFY_AUDIO_SETTINGS
services = pranksrv:service.py:foreground:sticky:foregroundServiceType=mediaPlayback
android.add_src = java
android.add_res = res
p4a.hook = p4a/hook.py
# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK / AAB will support.
android.minapi = 21

# (str) Android NDK version to use
# android.ndk = 25b

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid excess downloads or save time
# android.skip_update = False

# (bool) If True, then automatically accept SDK license
# agreements. This is intended for automation only. If set to False,
# the default, you will be shown the license when first run and
# you will need to accept it.
android.accept_sdk_license = True

# (str) Android entry point, default is ok for Kivy-based app
android.entrypoint = org.kivy.android.PythonActivity

# (str) python-for-android branch to use
p4a.branch = release-2024.01.21

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
