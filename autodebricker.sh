#!/bin/bash

# TB-J606F Autodebricker Script
# Developed for Antigravity Workspace

echo "==============================================="
echo "   Lenovo Tab P11 (TB-J606F) Autodebricker     "
echo "==============================================="

# Configuration
FILES=( "boot.img" "dtbo.img" "vbmeta.img" "recovery.img" "super_fixed.img" )
BASE_DIR="/home/op"

check_files() {
    echo "[*] Checking for required image files..."
    for file in "${FILES[@]}"; do
        if [ ! -f "$BASE_DIR/$file" ]; then
            echo "[!] ERROR: $file not found in $BASE_DIR"
            exit 1
        fi
    done
    echo "[+] All files found!"
}

flash_device() {
    echo "[*] Waiting for device in Fastboot mode..."
    fastboot wait-for-device
    
    echo "[*] Flashing Boot..."
    fastboot flash boot "$BASE_DIR/boot.img"
    
    echo "[*] Flashing DTBO..."
    fastboot flash dtbo "$BASE_DIR/dtbo.img"
    
    echo "[*] Flashing VBMeta (verity disabled)..."
    fastboot flash vbmeta "$BASE_DIR/vbmeta.img" --disable-verity --disable-verification
    
    echo "[*] Flashing Recovery..."
    fastboot flash recovery "$BASE_DIR/recovery.img"
    
    echo "[*] Flashing Super Partition (This may take a while)..."
    fastboot flash super "$BASE_DIR/super_fixed.img"
    
    echo "[*] Wiping user data..."
    fastboot -w
    
    echo "[+] Flashing complete. Rebooting..."
    fastboot reboot
}

echo "Instructions:"
echo "1. Power off your tablet."
echo "2. Hold Vol Down + Power until you see Fastboot mode."
echo "3. Connect the tablet to this PC via USB."
echo ""
read -p "Press [Enter] when the device is connected in Fastboot mode..."

check_files
flash_device

echo "==============================================="
echo "   Process Finished! Check your device.        "
echo "==============================================="
