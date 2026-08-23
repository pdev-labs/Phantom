import os
import subprocess
import sys

separator = ';' if sys.platform == 'win32' else ':'

subprocess.check_call([
    'pyinstaller',
    '--noconfirm',
    '--onefile',
    '--windowed',
    f'--add-data=prank_android_combined/assets/audio/*{separator}assets/audio',
    '--name=phantom_desktop',
    'prank_android_combined/service_desktop.py'
])
