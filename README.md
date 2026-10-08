# Project Infinity-X 4.0 (Android 17) for POCO X3 Pro (vayu) Builder

Automated builder to compile Project Infinity-X 4.0 (Android 17) for POCO X3 Pro (`vayu`).

## 🚀 One-Click Build in Google Colab (Recommended)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/PouyaFakhari/infinityx_vayu_builder/blob/main/InfinityX_Vayu_Android17_Builder.ipynb)

Click the badge above to open the pre-configured notebook directly in Google Colab.
- Connect to High-RAM runtime.
- Mounts your Google Drive automatically.
- Caches compiler files in `MyDrive/ccache`.
- Automatically outputs the finished ROM zip directly into your **Google Drive** in `MyDrive/InfinityX_Vayu_Builds/`!

## Components
- **Base ROM Framework**: [Project Infinity-X Branch 17](https://github.com/ProjectInfinity-X/manifest/tree/17) (Android 17.0.0_r1 / Lineage-24.0 base)
- **Device Tree**: `xetob/android_device_xiaomi_vayu` (branch `lineage-24.0`)
- **Common Tree**: `xetob/android_device_xiaomi_sm8150-common` (branch `lineage-24.0`)
- **Vendor Blobs**: `xetob/proprietary_vendor_xiaomi_vayu` + `sm8150-common` (branch `lineage-24.0`)
- **Kernel Tree**: `xetob/android_kernel_xiaomi_sm8150` (branch `lineage-24.0`)
