[app]
title = Synapse
package.name = synapse
package.domain = com.jack.neuroapp

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 0.1

# libs necessárias
requirements = python3,kivy,requests,plyer

orientation = portrait

android.archs = arm64-v8a
android.minapi = 29
android.api = 34
android.ndk = 25b
android.accept_sdk_license = True

android.permissions = INTERNET, CAMERA

[presplash]
presplash.color = 000000

[buildozer]
log_level = 2
warn_on_root = 1
