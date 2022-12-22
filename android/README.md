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

## Apps

### F-Droid

#### Repo's

- Collabora Office: https://www.collaboraoffice.com/downloads/fdroid/repo/
- microG: https://github.com/microg/GmsCore/wiki/Downloads#microg-f-droid-repository
- Nebulo: https://github.com/Ch4t4r/Nebulo#f-droid
- NewPipe https://newpipe.net/FAQ/tutorials/install-add-fdroid-repo/

#### Apps

- [F-Droid](https://f-droid.org/)
- [andOTP](https://f-droid.org/en/packages/org.shadowice.flocke.andotp/)
- [AnySoftKeyboard](https://f-droid.org/packages/com.menny.android.anysoftkeyboard/) + [Dutch lang pack](https://f-droid.org/packages/com.anysoftkeyboard.languagepack.dutch_oss/)
- [Aurora Store](https://f-droid.org/en/packages/com.aurora.store/)
- Collabora Office
- [DAVx5](https://f-droid.org/en/packages/at.bitfire.davdroid)
- [Déjà Vu](https://f-droid.org/en/packages/org.fitchfamily.android.dejavu) (UnifiedNlp backend)
- [Document Viewer](https://f-droid.org/en/packages/org.sufficientlysecure.viewer/) (PDF reader)
- [Etar](https://f-droid.org/packages/ws.xsoh.etar) (Calendar)
- [Fennec (Firefox)](https://f-droid.org/en/packages/org.mozilla.fennec_fdroid/)
- [Jellyfin](https://f-droid.org/en/packages/org.jellyfin.mobile/)
- microG Services Core (Enable GCM in settings!)
- microG Service Framework Proxy
- [MozillaNlpBackend](https://f-droid.org/en/packages/org.microg.nlp.backend.ichnaea) (UnifiedNlp backend)
- Nebulo
- NewPipe
- [Nextcloud](https://f-droid.org/en/packages/com.nextcloud.client/)
- [NominatimNlpBackend](https://f-droid.org/en/packages/org.microg.nlp.backend.nominatim) (UnifiedNlp backend)
- [Open Camera](https://f-droid.org/en/packages/net.sourceforge.opencamera/)
- [OpenTasks](https://f-droid.org/en/packages/org.dmfs.tasks)
- [OsmAnd](https://f-droid.org/en/packages/net.osmand.plus)
- [QR & Barcode Scanner](https://f-droid.org/en/packages/com.example.barcodescanner/)
- [RedReader](https://f-droid.org/en/packages/org.quantumbadger.redreader)

### Aurora Store

- [Alan BE](https://play.google.com/store/apps/details?id=com.alan.bemobile)
- [Belfius Mobile](https://play.google.com/store/apps/details?id=be.belfius.directmobile.android)
- [Joplin](https://play.google.com/store/apps/details?id=net.cozic.joplin)
- [Keepass2Android](https://play.google.com/store/apps/details?id=keepass2android.keepass2android)
- [Messenger Lite](https://play.google.com/store/apps/details?id=com.facebook.mlite)
- [NMBS](https://play.google.com/store/apps/details?id=be.sncbnmbs.b2cmobapp)
- [Plex](https://play.google.com/store/apps/details?id=com.plexapp.android)
- [WhatsApp](https://play.google.com/store/apps/details?id=com.whatsapp)

### Legacy mentions

- [FairEmail](https://f-droid.org/en/packages/eu.faircode.email/) (See invoice to activate Pro + import settings from Nextcloud) => Currently replaced by ProtonMail
