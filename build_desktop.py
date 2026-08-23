import os
import subprocess
import sys

separator = ';' if sys.platform == 'win32' else ':'

projects = [
    ('prank_android_1_basic', 'phantom_desktop_basic'),
    ('prank_android_2_sensors', 'phantom_desktop_sensors'),
    ('prank_android_combined', 'phantom_desktop_combined')
]

for proj_dir, name in projects:
    subprocess.check_call([
        'pyinstaller',
        '--noconfirm',
        '--onefile',
        '--windowed',
        f'--add-data={proj_dir}/assets/audio/*{separator}assets/audio',
        f'--name={name}',
        f'{proj_dir}/service_desktop.py'
    ])
