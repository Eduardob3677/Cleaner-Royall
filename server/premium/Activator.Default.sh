DIRR="/data/importer/data"
mount -o rw,remount /data >/dev/null 2>&1
[ ! -d "$DIRR" ] && mkdir -p "$DIRR"
echo cache > "$DIRR/prm.txt"
rm -rf "$DIRR/system/expp.txt"