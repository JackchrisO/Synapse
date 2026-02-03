[app]
title = Não deixe o sistema nervoso
package.name = naodeixeosistemanervoso
package.domain = com.jack.neuroapp
source.dir = .
version = 0.1
source.include_exts = py,png,jpg,kv,atlas

# Suporte a 32 e 64 bits
android.archs = armeabi-v7a, arm64-v8a

# API mínima e alvo
android.minapi = 21
android.api = 30
android.ndk = 25b

# Permissões necessárias
android.permissions = INTERNET

[requirements]
# Não incluir "python3" aqui
requirements = kivy, cython

[presplash]
presplash.color = 0x000000
android.accept_sdk_license = True
[icon]

[buildozer]
log_level = 2
warn_on_root = 1
