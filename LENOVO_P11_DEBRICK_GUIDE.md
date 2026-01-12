# 📱 Lenovo Tab P11 (TB-J606F) Debricking & Customization Guide

This guide provides a detailed walkthrough for recovering a bricked Lenovo Tab P11 and installing custom firmware.

## 🛠 Prerequisites

- **Tools**: `fastboot` and `adb` installed on your machine.
- **Drivers**: Qualcomm USB Drivers (for EDL mode).
- **Files**: 
  - [Stock Firmware Partitions](https://mirrors-obs-1.lolinet.com/lenovo/tab_p11/TB-J606F/) (`boot.img`, `recovery.img`, `vbmeta.img`, `dtbo.img`).
  - Reconstructed Super Image (`super_fixed.img`).
  - [TWRP Recovery 3.7.1](https://xdaforums.com/t/recovery-twrp-unofficial-twrp-3-7-1-recovery-for-lenovo-tb-j606f-l.4582697/) (`twrp-J606F_3.7.1_12.0-20240414.img`).
  - Custom ROM (e.g., [AOSP GSI](https://github.com/phhusson/treble_experimentations/releases) `system.img`).

---

## 🔗 Downloads & Resources

| Resource | Source Link |
| :--- | :--- |
| **Official Firmware Mirror** | [Lolinet Mirror](https://mirrors-obs-1.lolinet.com/lenovo/tab_p11/TB-J606F/) |
| **TWRP Recovery (XDA)** | [Unofficial TWRP Thread](https://xdaforums.com/t/recovery-twrp-unofficial-twrp-3-7-1-recovery-for-lenovo-tb-j606f-l.4582697/) |
| **GSI List (Treble)** | [Project Treble GSI List](https://github.com/phhusson/treble_experimentations/wiki/Generic-System-Image-%28GSI%29-list) |
| **ADB & Fastboot** | [Android SDK Platform-Tools](https://developer.android.com/studio/releases/platform-tools) |

## 🏗 Part 1: Debricking (Restoring Stock)

If your device is in a bootloop or stuck at the Lenovo logo:

### 1. Reconstruct the Super Image
The `super` partition on the P11 is dynamic and often needs reconstruction if flashing individual sub-partitions.
1. Ensure your extracted firmware is in `firmware_extracted/`.
2. Run the provided builder script:
   ```bash
   python3 build_super.py
   ```
   This generates `super_fixed.img`.

### 2. Enter Fastboot Mode
1. Power off the tablet.
2. Hold **Volume Down + Power** until the Fastboot screen appears.
3. Connect to your PC.

### 3. Flash Stock Partitions
Run the following commands in order:
```bash
fastboot flash boot boot.img
fastboot flash dtbo dtbo.img
fastboot flash vbmeta vbmeta.img --disable-verity --disable-verification
fastboot flash recovery recovery.img
fastboot flash super super_fixed.img
fastboot -w
fastboot reboot
```

---

## 🚀 Part 2: Customization (TWRP & GSI)

Once stock is booted and verified:

### 1. Flash TWRP
1. Return to Fastboot mode.
2. Flash the custom recovery:
   ```bash
   fastboot flash recovery twrp-J606F_3.7.1_12.0-20240414.img
   ```

### 2. Flash GSI (AOSP 16 / Android 12+)
1. Reboot to TWRP.
2. Format Data (Wipe > Format Data > type 'yes').
3. Flash the GSI `system.img` to the System partition:
   ```bash
   adb push system.img /sdcard/
   # In TWRP: Install -> Install Image -> select system.img -> Partition: System Image
   ```
4. Flash `vbmeta.img` with flags to ensure it boots:
   ```bash
   fastboot flash vbmeta vbmeta.img --disable-verity --disable-verification
   ```

---

## 🤖 Part 3: Using the Autodebricker Script

For a semi-automated experience, use the `autodebricker.sh` script:

```bash
chmod +x autodebricker.sh
./autodebricker.sh
```
Follow the on-screen prompts to recover your device.
