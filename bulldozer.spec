[app]

# (str) Title of your app
title = Não deixe o sistema nervoso

# (str) Package name
package.name = naodeixeosistemanervoso

# (str) Package domain (needed for android/ios packaging)
package.domain = com.jack.neuroapp

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
#source.exclude_dirs = tests, bin

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*.jpg

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported android version
android.arch = armeabi-v7a
android.minapi = 21
android.sdk = 30
android.ndk = 19b
android.release = debug

# (int) API to use
#android.api = 30

# (int) Android min API to use
#android.minapi = 21

# (int) Android SDK version to use
#android.sdk = 30

# (str) Android NDK version to use
#android.ndk = 19b

# (str) Android NDK API to use. Set to the highest available API
#android.ndk_api = 21

# (bool) Use --private data storage (True) or --dir public storage (False)
#android.private_storage = True

# (str) Android logcat filters to use
#android.logcat_filters = *:S python:D

# (bool) Disable installing android package so python can just update the .py/.pyc files
#android.no_install = False

# (str) Path to a custom loader
#loader = %(source.dir)s/loader.py

# (str) permissions
#android.permissions = INTERNET

# (int) Android API to use
#android.api = 30

# (str) The format used to package the app for release (one of 'apk', 'aab')
#android.release_format = apk

# (str) The release format to use (one of 'debug', 'release')
#android.release = debug

# (bool) Enable log output
#android.logcat = *:S

# (int) Android min API to use
#android.minapi = 21

# (int) Android SDK version to use
#android.sdk = 30

# (str) Android NDK version to use
#android.ndk = 19b

# (str) Android NDK API to use. Set to the highest available API
#android.ndk_api = 21

# (bool) Use --private data storage (True) or --dir public storage (False)
#android.private_storage = True

# (str) Android logcat filters to use
#android.logcat_filters = *:S python:D

# (bool) Disable installing android package so python can just update the .py/.pyc files
#android.no_install = False

# (str) Path to a custom loader
#loader = %(source.dir)s/loader.py

# (str) permissions
#android.permissions = INTERNET

[requirements]
python3,kivy

[presplash]
# (file) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (RGBA) Presplash color
#presplash.color = 0x000000

[icon]
# (file) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

[buildozer]
# (int) Log level (0 = error only, 1 = warning, 2 = info, 3 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
