# Setup guide for Android

## Backup

- Aegis Authenticator (andOTP is unmaintained)
- AnySoftKeyboard
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

## General setup

### Quick menu

1. Wifi
1. Bluetooth
1. Auto-rotate
1. Do Not Disturb
1. Caffeine
1. Reading mode
1. Battery Saver
1. Extra dim
1. Airplane mode
1. Dark theme

## Apps

### F-Droid

#### Repo's

- Collabora Office: https://www.collaboraoffice.com/downloads/fdroid/repo/
- microG: https://github.com/microg/GmsCore/wiki/Downloads#microg-f-droid-repository
- NewPipe https://newpipe.net/FAQ/tutorials/install-add-fdroid-repo/

#### Apps

- [F-Droid](https://f-droid.org/)
- [Aegis Authenticator](https://f-droid.org/en/packages/com.beemdevelopment.aegis/)
- [AnySoftKeyboard](https://f-droid.org/packages/com.menny.android.anysoftkeyboard/) + [Dutch lang pack](https://f-droid.org/packages/com.anysoftkeyboard.languagepack.dutch_oss/)
- [Aurora Store](https://f-droid.org/en/packages/com.aurora.store/)
- Collabora Office
- [DAVx5](https://f-droid.org/en/packages/at.bitfire.davdroid)
- [Déjà Vu](https://f-droid.org/en/packages/org.fitchfamily.android.dejavu) (UnifiedNlp backend)
- [Document Viewer](https://f-droid.org/en/packages/org.sufficientlysecure.viewer/) (PDF reader)
- [Element](https://f-droid.org/en/packages/im.vector.app/)
- [Etar](https://f-droid.org/packages/ws.xsoh.etar) (Calendar)
- [Fennec (Firefox)](https://f-droid.org/en/packages/org.mozilla.fennec_fdroid/)
- [Home Assistant](https://f-droid.org/en/packages/io.homeassistant.companion.android.minimal/)
- [Jellyfin](https://f-droid.org/en/packages/org.jellyfin.mobile/)
- microG Services Core (Enable GCM in settings!)
- microG Service Framework Proxy
- [MozillaNlpBackend](https://f-droid.org/en/packages/org.microg.nlp.backend.ichnaea) (UnifiedNlp backend)
- [Mullvad VPN](https://f-droid.org/en/packages/net.mullvad.mullvadvpn/)
- NewPipe
- [Nextcloud](https://f-droid.org/en/packages/com.nextcloud.client/)
- [Nextcloud Deck](https://f-droid.org/en/packages/it.niedermann.nextcloud.deck/)
- [Nextcloud Notes](https://f-droid.org/en/packages/it.niedermann.owncloud.notes/)
- [NominatimNlpBackend](https://f-droid.org/en/packages/org.microg.nlp.backend.nominatim) (UnifiedNlp backend)
- [Open Camera](https://f-droid.org/en/packages/net.sourceforge.opencamera/)
- [OpenTasks](https://f-droid.org/en/packages/org.dmfs.tasks)
- [OsmAnd](https://f-droid.org/en/packages/net.osmand.plus)
- [RedReader](https://f-droid.org/en/packages/org.quantumbadger.redreader)
- [Syncthing](https://f-droid.org/en/packages/com.nutomic.syncthingandroid/)

### Aurora Store

- [Argenta](https://play.google.com/store/apps/details?id=be.argenta.bankieren)
- [Belfius Mobile](https://play.google.com/store/apps/details?id=be.belfius.directmobile.android)
- [Bitwarden](https://play.google.com/store/apps/details?id=com.x8bit.bitwarden). Block autofill of:
  - androidapp://com.beemdevelopment.aegis
- [itsme](https://play.google.com/store/apps/details?id=be.bmid.itsme)
- [KopieID](https://play.google.com/store/apps/details?id=com.milvum.kopieid)
- [Magic Earth](https://play.google.com/store/apps/details?id=com.generalmagic.magicearth)
- [NMBS](https://play.google.com/store/apps/details?id=be.sncbnmbs.b2cmobapp)
- [Plex](https://play.google.com/store/apps/details?id=com.plexapp.android)
- [WhatsApp](https://play.google.com/store/apps/details?id=com.whatsapp)
- [Zoho Email](https://play.google.com/store/apps/details?id=com.zoho.mail)

### Legacy mentions

- [FairEmail](https://f-droid.org/en/packages/eu.faircode.email/) (See invoice to activate Pro + import settings from Nextcloud) => Currently replaced by ProtonMail
