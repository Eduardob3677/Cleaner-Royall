
INT=$(ls -d /data/media/0 /storage/emulated/0 /sdcard 2>/dev/null | head -n 1)

rm -rf /data/system/dropbox &
rm -rf /data/system/usagestats
rm -rf $INT/bugreports
rm -rf /data/log
rm -rf $INT/Android/data/*/cache &
rm -rf /data/data/*/cache &
rm -rf /data/local/tmp/*
rm -rf /data/logger
rm -rf $INT/LOST.DIR
rm -rf /data/anr
rm -rf /data/tombstones
rm -rf $INT/DCIM/.thumbnails/* &
rm -rf $INT/Pictures/.thumbnails/*
