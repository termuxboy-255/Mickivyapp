[app]
title = Micmac Betting
package.name = micmacapp
package.domain = org.micmac
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,json,xml
source.include_patterns = assets/**,images/**,data/**
version = 0.1
requirements = python3,kivy==2.1.0,kivymd,requests,urllib3,ssl,certifi,android,pyjnius
presplash.filename = %(source.dir)s/background.png
icon.filename = %(source.dir)s/icon.png
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

# Android specific
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.sdk = 23
android.ndk = 25b
android.archs = arm64-v8a
android.allow_backup = True
p4a.bootstrap = sdl2
android.entrypoint = org.kivy.android.PythonActivity
