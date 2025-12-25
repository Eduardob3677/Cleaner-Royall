#!/system/bin/sh
# Script Created by @AraafRoyall

if [ -d "/data/media/0" ]; then
INT="/data/media/0"
elif [ -d "/storage/emulated/0" ]; then
INT="/storage/emulated/0"
else
INT="/sdcard"
fi

# -------------------------------------------#


MSK="/data/adb/modules"

echo "Checking Magisk Installed..."

if [ ! -d "$MSK" ]; then
if ! { mkdir -p "$MSK" || install -d "$MSK"; }; then
echo "Failed to Create Module Path"
royallaraaf
exit 1
fi
fi


echo "Magisk is Correctly Installed."
echo "Making Module Path..."

if [ ! -d "$MSK/CleanerRoyall" ]; then
if ! { mkdir -p "$MSK/CleanerRoyall" || install -d "$MSK/CleanerRoyall"; }; then
echo "Failed to Create Module Path"
royallaraaf
exit 1
fi
fi


MDK="$MSK/CleanerRoyall"

echo "Module Path Created."
echo "Making module.prop file..."

echo "id=CleanerRoyall
name=Cleaner Royall
version=1.1
versionCode=1
author=Araaf Royall
description=Ultimate Systemless Module for Automated background cleaner at set intervals
" > $MDK/module.prop

echo "Checking Module File..."

if [ ! -f "$MDK/module.prop" ]; then
echo "Failed to Create Module.prop, Exiting..."
royallaraaf
exit 1
fi

echo "Module.prop File Sucessfully Created."

echo "Making Folder which will store data"


if [ ! -d "$MDK/xdata " ]; then
if ! { mkdir -p "$MDK/xdata" || install -d "$MDK/xdata"; }; then
echo "Failed to Create Folder for Data"
rm -rf "$MDK/xdata"
royallaraaf
exit 1
fi
fi

echo "Sucessfully Created Folder for data."


echo "Making log file"
echo "[$(date '+%Y-%m-%d %I:%M:%S %p')] - Module Installed" > $MDK/xdata/log.txt
echo "Log file created sucess"


echo "Making duration File"
echo "3600" > $MDK/xdata/duration.txt
echo "Duration file created sucessfully"




# ---------------------------------------
#                 PART 2
# ---------------------------------------



echo "Making service file"

cat << 'EOF' > $MDK/service.sh
#!/system/bin/sh
#Script created by AraafRoyall

# ---------------------------------------

while [ $(getprop sys.boot_completed) != 1 ]; do sleep 3; done

MODDIR="${0%/*}"
LOGFILE="$MODDIR/xdata/log.txt"

if [ ! -f "$LOGFILE" ]; then
echo "Making Log File" > $LOGFILE
fi

logg() {
        [ -f "$MODDIR/xdata/log" ] && echo "[$(date '+%Y-%m-%d %I:%M:%S %p')] - $1" >> "$LOGFILE" || echo "$1" > /dev/null 2>&1
}

if [ ! -f "$MODDIR/xdata/bootstart" ]; then
logg "Start from boot is disabled"
rm -rf $MODDIR/xdata/run
exit 1
fi

logg "Starting From Boot" 


if [ -f "$MODDIR/automatic.sh" ]; then
nohup $MODDIR/automatic.sh &
logg "Auto Cleaning Stared from Boot"
else
logg "Module is not properly Installed"
fi
EOF


echo "Checking Service & Granting Permission"

if [ ! -f "$MDK/service.sh" ]; then
echo "Failed to Create Service.sh file, Exiting..."
royallaraaf
exit 1
fi

chmod 777 $MDK/service.sh

echo "Check & Permission Done."



# ---------------------------------------
#                 PART 3
# ---------------------------------------



cat << 'EOG' > $MDK/automatic.sh
#!/system/bin/sh
# Created by Araaf Royall.

# ----------------------------------

MODDIR="/data/adb/modules/CleanerRoyall"
LOGFILE="$MODDIR/xdata/log.txt"
DURATION="$MODDIR/xdata/duration.txt"

if [ ! -f "$LOGFILE" ]; then
  echo "Initialing Records & Actions" > $LOGFILE
fi

if [ ! -f "$DURATION" ]; then
echo "1800" > $DURATION
fi


echo "x" > $MODDIR/xdata/run

INT="/data/media/0"
[ ! -d "$INT" ] && INT="/storage/emulated/0"
[ ! -d "$INT" ] && INT="/sdcard"

# ----------------------------------


logg() {
        [ -f "$MODDIR/xdata/log" ] && echo "[$(date '+%Y-%m-%d %I:%M:%S %p')] - $1" >> "$LOGFILE" || echo "$1" > /dev/null 2>&1
}


# ----------------------------------

dalvikClean() {
        sleep 120
        rm -rf /data/dalvik-cache/*
        logg "Cleaned Dalvik Cache"
        }
        
        
        if [ -f "$MODDIR/xdata/cleandalvik" ]; then
        dalvikClean &
        fi
        
        # ----------------------------------
        
        

cleanerCache() {
        find /data/data/*/cache/* -delete > /dev/null 2>&1
        find /data/data/*/code_cache/* -delete > /dev/null 2>&1
        find /data/user_de/*/*/cache/* -delete > /dev/null 2>&1
        find /data/user_de/*/*/code_cache/* -delete > /dev/null 2>&1
        rm -rf $INT/Android/data/*/cache/*
        rm -rf /data/data/*/cache/*
        rm -rf /data/data/*/code_cache/*
        rm -rf /data/user_de/*/*/cache/*
        rm -rf /data/user_de/*/*/code_cache/*
        }
        
        
        
cleanerLog() {
        
        rm -rf /data/adb/lspd/log
        rm -rf /data/system/*/logging/server_logging/log
        rm -rf /storage/emulated/0/Fox/logs
        rm -rf /data/misc/update_engine_log
        rm -rf /data/system/*/tmp/runtime.log
        rm -rf /data/log
        rm -rf /data/logger
        rm -rf /data/data/*/files/debug_log
        rm -rf /data/data/*/files/dump/log
        rm -rf /data/data/*/files/Logs
        rm -rf /data/media/*/Android/data/*/files/*/log*
        find /data -type f -name "*.log" -delete > /dev/null 2>&1
        }
        
        
cleanTrash() {
        find /data -type f -name "*.tmp" -delete > /dev/null 2>&1
        find /data -type f -name "*.temp" -delete > /dev/null 2>&1
        find /data -type f -name "*.tempfile" -delete > /dev/null 2>&1
        }
        
        
cleanOat() {
        rm -rf /data/app/*/*/oat
        rm -rf /data/app/*/oat
        }
    
    
maxRecord() {

if command -v sed >/dev/null && command -v wc >/dev/null; then
    if [ "$(wc -l < "$LOGFILE")" -ge 30 ]; then
        sed -i '1,30d' "$LOGFILE" && logg "Deleted old Actions"
    fi  
fi
}

        
        # ---------------------------------
        
        
while [ ! -f $MODDIR/disable ]; do
        
        
        if [ -f "$MODDIR/xdata/cleanlg" ]; then
        cleanerLog
        logg "Sucessfully Cleared All Logs"
        fi
        
        sleep 1
        
        if [ -f "$MODDIR/xdata/cleancache" ]; then
        cleanerCache
        logg "Sucessfully Cleaned All Caches"
        fi
        
        sleep 1
        
        if [ -f "$MODDIR/xdata/cleanoat" ]; then
        cleanOat
        logg "Sucessfully Cleaned Oat Files"
        fi
        
        sleep 1
        
        if [ -f "$MODDIR/xdata/cleantrash" ]; then
        cleanTrash
        logg "Sucessfully Cleaned Trash Files"
        fi
        
    
sleep 1

    [ -f "$MODDIR/xdata/log" ] && maxRecord


    logg "Next Cycle - Waiting"


        
        [ -f $MODDIR/disable ] && break
        
        sleep $(cat "$DURATION")
done
        
        
        
        rm -rf $MODDIR/xdata/run
        logg "Disabled Background Cleaner"
        
EOG



echo "granting permission"


if [ ! -f "$MDK/automatic.sh" ]; then
        echo "Failed to Create Service.sh file, Exiting..."
        royallaraaf
        exit 1
fi

chmod 777 $MDK/automatic.sh

echo "Check & Permission Done."






echo "Module Installation Sucess."

echo "Now you can complete other setup"


