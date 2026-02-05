[app]
title = Não deixe o sistema nervoso
package.name = naodeixeosistemanervoso
package.domain = com.jack.neuroapp

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 0.1

# 🚀 Build mais rápido e estável
android.archs = arm64-v8a

# 📱 Android moderno (compatível)
android.minapi = 21
android.api = 34

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
