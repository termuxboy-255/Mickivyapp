[app]
title = Micmac Betting
package.name = micmacapp
package.domain = org.micmac
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,json
version = 0.1
requirements = python3,kivy,android
presplash.filename = %(source.dir)s/background.png
icon.filename = %(source.dir)s/icon.png
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 1

# Android specific
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.archs = arm64-v8a

# Point to our pre-installed SDK
android.sdk_path = ./android-sdk
