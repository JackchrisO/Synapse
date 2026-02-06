[app]
title = Synapse
package.name = naodeixeosistemanervoso
package.domain = com.jack.neuroapp

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 0.1

android.archs = arm64-v8a
android.minapi = 29
android.api = 34
android.ndk = 25b
android.accept_sdk_license = True

requirements = python3,kivy,openssl,sqlite3

orientation = portrait

android.permissions = INTERNET

[presplash]
presplash.color = 000000

[buildozer]
log_level = 2
warn_on_root = 1
