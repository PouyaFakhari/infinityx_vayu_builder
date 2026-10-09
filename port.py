#!/usr/bin/env python3
"""
Project Infinity-X 4.0 (Android 17) Binary Porting Tool for POCO X3 Pro (vayu)
Maintainer: Pouya Fakhari (PouyaPF) - Telegram: @Pouya_Fakhari
"""

import os
import sys
import shutil
import zipfile
import re

def log(msg):
    print(f"[+] {msg}", flush=True)

def parse_op_list(filepath):
    sizes = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 3 and parts[0] == 'resize':
                sizes[parts[1]] = parts[2]
    return sizes

def build_merged_op_list(base_op_path, port_op_path, out_op_path):
    log("Merging dynamic_partitions_op_list...")
    base_sizes = parse_op_list(base_op_path)
    port_sizes = parse_op_list(port_op_path)
    
    # Read base op list as template
    with open(base_op_path, 'r', encoding='utf-8') as f:
        base_lines = f.readlines()
        
    out_lines = []
    for line in base_lines:
        parts = line.strip().split()
        if len(parts) >= 3 and parts[0] == 'resize':
            partition = parts[1]
            if partition in ['system', 'system_ext', 'product'] and partition in port_sizes:
                new_size = port_sizes[partition]
                out_lines.append(f"resize {partition} {new_size}\n")
                log(f"  Partition {partition}: updated size to {new_size} (from Infinity-X)")
            else:
                out_lines.append(line)
        else:
            out_lines.append(line)
            
    with open(out_op_path, 'w', encoding='utf-8') as f:
        f.writelines(out_lines)
    log("dynamic_partitions_op_list generated successfully.")

def patch_updater_script(script_path):
    log("Patching updater-script with custom Pouya Fakhari maintainer banner...")
    with open(script_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    custom_banner = """
ui_print("==================================================");
ui_print("       PROJECT INFINITY-X 4.0 - ANDROID 17        ");
ui_print("            POCO X3 Pro (vayu / bhima)            ");
ui_print("--------------------------------------------------");
ui_print("   Maintainer : Pouya Fakhari (PouyaPF)           ");
ui_print("   Telegram   : @Pouya_Fakhari                    ");
ui_print("   Build Type : UNOFFICIAL / RELEASE              ");
ui_print("==================================================");
"""
    # Replace existing banner prints or insert at beginning
    if 'ui_print("Target:' in content:
        content = re.sub(r'ui_print\("Target:.*?\);(\s*ui_print\(".*?\);)*', custom_banner, content, count=1)
    else:
        content = custom_banner + "\n" + content

    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    base_zip = sys.argv[1] if len(sys.argv) > 1 else "base.zip"
    port_zip = sys.argv[2] if len(sys.argv) > 2 else "port.zip"
    out_zip = sys.argv[3] if len(sys.argv) > 3 else "Project_Infinity-X-4.0-vayu-VANILLA-UNOFFICIAL.zip"

    work_dir = "work_port"
    if os.path.exists(work_dir):
        shutil.rmtree(work_dir)
        
    base_dir = os.path.join(work_dir, "base")
    port_dir = os.path.join(work_dir, "port")
    out_dir = os.path.join(work_dir, "out")
    
    os.makedirs(base_dir, exist_ok=True)
    os.makedirs(port_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    log(f"Extracting Vayu Hardware Base: {base_zip}")
    with zipfile.ZipFile(base_zip, 'r') as z:
        z.extractall(base_dir)

    log(f"Extracting Infinity-X 4.0 System Port: {port_zip}")
    with zipfile.ZipFile(port_zip, 'r') as z:
        z.extractall(port_dir)

    log("Assembling target ROM filesystem...")
    # 1. Copy Vayu Hardware Partitions & Kernels
    vayu_hw_files = [
        "boot.img", "dtbo.img", "vbmeta.img", "vbmeta_system.img",
        "vendor.new.dat.br", "vendor.transfer.list", "vendor.patch.dat",
        "odm.new.dat.br", "odm.transfer.list", "odm.patch.dat"
    ]
    for fn in vayu_hw_files:
        src = os.path.join(base_dir, fn)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(out_dir, fn))
            log(f"  [VAYU HW] Copied {fn}")

    # Copy install & META-INF binaries
    for subdir in ["install", "META-INF"]:
        src = os.path.join(base_dir, subdir)
        if os.path.exists(src):
            shutil.copytree(src, os.path.join(out_dir, subdir), dirs_exist_ok=True)

    # 2. Copy Infinity-X 4.0 System, System_Ext, Product
    infinity_sys_files = [
        "system.new.dat.br", "system.transfer.list", "system.patch.dat",
        "system_ext.new.dat.br", "system_ext.transfer.list", "system_ext.patch.dat",
        "product.new.dat.br", "product.transfer.list", "product.patch.dat"
    ]
    for fn in infinity_sys_files:
        src = os.path.join(port_dir, fn)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(out_dir, fn))
            log(f"  [INFINITY-X 4.0] Copied {fn}")

    # 3. Dynamic Partitions OP List
    base_op = os.path.join(base_dir, "dynamic_partitions_op_list")
    port_op = os.path.join(port_dir, "dynamic_partitions_op_list")
    out_op = os.path.join(out_dir, "dynamic_partitions_op_list")
    build_merged_op_list(base_op, port_op, out_op)

    # 4. Patch Updater Script
    updater_script = os.path.join(out_dir, "META-INF", "com", "google", "android", "updater-script")
    if os.path.exists(updater_script):
        patch_updater_script(updater_script)

    # 5. Repack into final zip
    log(f"Repacking final signed flashable zip: {out_zip}")
    with zipfile.ZipFile(out_zip, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z_out:
        for root, dirs, files in os.walk(out_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, out_dir)
                z_out.write(full_path, rel_path)

    log(f"ROM package successfully generated: {out_zip} ({os.path.getsize(out_zip):,} bytes)")

if __name__ == "__main__":
    main()
