[app]
title = Kalkulator Beban Trafo
package.name = kalkulatorbeban
package.domain = org.kalkulator
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0
requirements = python3,kivy
orientation = portrait

[buildozer]
log_level = 2

[app:android]
android.api = 33
android.minapi = 21
android.permissions = INTERNET
