# Setup guide for Android

## Backup

- Aegis Authenticator (andOTP is unmaintained)
- AnySoftKeyboard
- Clock (alarms)
- NewPipe
- Open Camera
- RedReader
- Syncthing
- WhatsApp

## Flash ROM

### crDroid

1. Get firmware and recovery from https://lineage.linux4.de/devices/beyond1lte.html
2. Download ROM from https://crdroid.net/beyond1lte/8 (= Android 12.1)
3. Flash firmware to instructions from download location
4. Flash recovery with `sudo heimdall flash --RECOVERY recovery.img`
5. Reboot into recovery
6. Perform Factory reset
7. Apply update => From ADB => Run `sudo adb sideload crDroidAndroid*.zip`
8. Flash in same way `Magisk*.apk` from https://github.com/topjohnwu/Magisk/releases
9. Flash in same way `org.fdroid*.zip` from https://f-droid.org/en/packages/org.fdroid.fdroid.privileged.ota/

### iodé

See https://iode.tech/en/iodeos-installation/

## Calyx

See https://calyxos.org/install/devices/FP5/linux/

## General setup

### Reduce animation times

In `Developers options`, change following values to `Anitmation scale .5x`:

- Window animation scale
- Transition animation scale
- Animator duration scale

### Quick menu

1. Internet
1. Bluetooth
1. Do Not Disturb
1. Flashlight
1. Auto-rotate
1. Battery Saver
1. Extra dim
1. Airplane mode
1. NFC
1. Hotspot
1. Nearby Share
1. Dark theme
1. Night light

## Apps

### Obtainium

https://github.com/ImranR98/Obtainium

#### General

- [Aegis Authenticator](https://github.com/beemdevelopment/Aegis)
- [AnySoftKeyboard](https://github.com/AnySoftKeyboard/AnySoftKeyboard)
- [AnySoftKeyboard - Dutch lang pack](https://f-droid.org/packages/com.anysoftkeyboard.languagepack.dutch_oss/)
- [Aurora Store](https://gitlab.com/AuroraOSS/AuroraStore)
- [Collabora Office (com.collabora.libreoffice)](https://www.collaboraoffice.com/downloads/fdroid/repo/)
- [DAVx5](https://github.com/bitfireAT/davx5-ose)
- [Element](https://github.com/vector-im/element-android)
- [Fenix (Firefox, same APK as Google Play)](https://ftp.mozilla.org/pub/fenix/releases/)
- [Home Assistant](https://github.com/home-assistant/android) (version = [Minimal](https://companion.home-assistant.io/docs/core/android-flavors/))
- [Jellyfin](https://github.com/jellyfin/jellyfin-android) (version = [Libre](https://github.com/jellyfin-archive/jellyfin-android-original/issues/331#issuecomment-623391632))
- [Librera Reader](https://github.com/foobnix/LibreraReader)
- [LocalSend](https://github.com/localsend/localsend)
- [Mullvad VPN](https://github.com/mullvad/mullvadvpn-app)
- [NewPipe](https://github.com/TeamNewPipe/NewPipe)
- [Nextcloud](https://github.com/nextcloud/android)
- [Nextcloud Deck](https://f-droid.org/en/packages/it.niedermann.nextcloud.deck/)
- [Nextcloud Notes](https://f-droid.org/en/packages/it.niedermann.owncloud.notes/)
- [Open Camera](https://sourceforge.net/projects/opencamera/files/)
- [OsmAnd](https://f-droid.org/en/packages/net.osmand.plus)
- [PhoneTrack](https://f-droid.org/packages/net.eneiluj.nextcloud.phonetrack)
- [RedReader](https://github.com/QuantumBadger/RedReader)
- [Simple Calendar](https://github.com/SimpleMobileTools/Simple-Calendar)
- [Simple File Manager](https://github.com/SimpleMobileTools/Simple-File-Manager)
- [Simple Gallery](https://github.com/SimpleMobileTools/Simple-Gallery)
- [Simple SMS Messenger](https://github.com/SimpleMobileTools/Simple-SMS-Messenger)
- [Syncthing](https://github.com/syncthing/syncthing-android)
- [VLC](https://videolan.org)

#### microG

- [Déjà Vu (UnifiedNlp backend)](https://github.com/n76/DejaVu)
- [microG Services Core (com.google.android.gms)](https://github.com/microg/GmsCore/releases)
- [microG Service Framework Proxy (GSF)](https://github.com/microg/GsfProxy)
- [MozillaNlpBackend (UnifiedNlp backend)](https://github.com/microg/IchnaeaNlpBackend)
- [NominatimNlpBackend (UnifiedNlp backend)](https://github.com/microg/NominatimGeocoderBackend)

### Aurora Store

- [Argenta](https://play.google.com/store/apps/details?id=be.argenta.bankieren)
- [Belfius Mobile](https://play.google.com/store/apps/details?id=be.belfius.directmobile.android)
- [Bitwarden](https://play.google.com/store/apps/details?id=com.x8bit.bitwarden). Block autofill of:
  - androidapp://com.beemdevelopment.aegis
- [itsme](https://play.google.com/store/apps/details?id=be.bmid.itsme)
- [KopieID](https://play.google.com/store/apps/details?id=com.milvum.kopieid)
- [Magic Earth](https://play.google.com/store/apps/details?id=com.generalmagic.magicearth)
- [NMBS](https://play.google.com/store/apps/details?id=be.sncbnmbs.b2cmobapp)
- [Proton Mail](https://play.google.com/store/apps/details?id=ch.protonmail.android)
- [WhatsApp](https://play.google.com/store/apps/details?id=com.whatsapp)
- [Zoho Email](https://play.google.com/store/apps/details?id=com.zoho.mail)

### Legacy mentions

- [FairEmail](https://f-droid.org/en/packages/eu.faircode.email/) (See invoice to activate Pro + import settings from Nextcloud) => Currently replaced by ProtonMail
