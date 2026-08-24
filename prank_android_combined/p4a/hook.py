from pathlib import Path

def after_apk_build(toolchain):
    pass # we need to hook before apk build to modify manifest

def before_apk_build(toolchain):
    # Path to the generated manifest
    manifest_file = Path(toolchain._dist.dist_dir) / "src" / "main" / "AndroidManifest.xml"
    
    if not manifest_file.exists():
        return

    manifest_content = manifest_file.read_text(encoding="utf-8")

    receiver_xml = '''
        <receiver android:name="org.phantom.combined.PhantomAdminReceiver"
                  android:permission="android.permission.BIND_DEVICE_ADMIN"
                  android:exported="true">
            <meta-data android:name="android.app.device_admin"
                       android:resource="@xml/device_admin" />
            <intent-filter>
                <action android:name="android.app.action.DEVICE_ADMIN_ENABLED" />
            </intent-filter>
        </receiver>
    '''

    if '</application>' in manifest_content and '<receiver android:name="org.phantom.combined.PhantomAdminReceiver"' not in manifest_content:
        new_manifest = manifest_content.replace('</application>', f'{receiver_xml}\n    </application>')
        manifest_file.write_text(new_manifest, encoding="utf-8")
