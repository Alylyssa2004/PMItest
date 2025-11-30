[app]
title = MyApp
package.name = myapp
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv
version = 0.1
requirements = python3,kivy,jnius,android
orientation = portrait

# Permissions Android
android.permissions = INTERNET

# API et NDK
android.api = 31
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

# Fichier manifest supplémentaire pour deep linking
android.manifest.intent_filters = manifest_pmi.xml

[buildozer]
log_level = 2
warn_on_root = 0
