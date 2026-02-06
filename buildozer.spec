[app]
title = Synapse
package.name = synapse
package.domain = com.jack.neuroapp

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 0.1


android.archs = arm64-v8a


android.minapi = 21
android.api = 33

# 🧱 NDK compatível com python-for-android
android.ndk = 25b

android.accept_sdk_license = True

# 🌐 Permissões
android.permissions = INTERNET

# ⚠️ Ordem e conteúdo importam
requirements = python3,kivy

[presplash]
presplash.color = 000000

[buildozer]
log_level = 2
warn_on_root = 1
