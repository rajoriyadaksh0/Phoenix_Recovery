import os
import struct

def modify_fat_table(drive_path, cluster_to_modify, new_value):
    try:
        # Ensure the drive exists and is accessible
        if not os.path.exists(drive_path):
            raise FileNotFoundError(f"Drive {drive_path} not found. Please check the path.")

        # Open the drive in binary read/write mode
        with open(drive_path, "r+b") as disk:
            # Step 1: Read Boot Sector
            disk.seek(0)  # Move to the beginning of the drive
            boot_sector = disk.read(512)  # Read the first 512 bytes (Boot Sector)

            # Validate boot sector size
            if len(boot_sector) < 512:
                raise ValueError("Boot sector could not be read. Ensure the device is a valid FAT32 drive.")

            # Extract necessary information from the Boot Sector
            bytes_per_sector = int.from_bytes(boot_sector[11:13], "little")
            sectors_per_cluster = boot_sector[13]
            reserved_sectors = int.from_bytes(boot_sector[14:16], "little")
            fat_size = int.from_bytes(boot_sector[36:40], "little")

            # Calculate FAT region location
            fat_start = reserved_sectors * bytes_per_sector
            fat_size_bytes = fat_size * bytes_per_sector

            # Validate Cluster Number
            total_clusters = fat_size_bytes // 4
            if cluster_to_modify < 2 or cluster_to_modify >= total_clusters:
                raise ValueError(f"Invalid cluster number: {cluster_to_modify}. Valid range is 2 to {total_clusters - 1}.")

            # Step 2: Modify the FAT Entry for the Given Cluster
            entry_offset = fat_start + cluster_to_modify * 4  # Each FAT32 entry is 4 bytes
            disk.seek(entry_offset)

            # Write the new value to the cluster
            disk.write(struct.pack('<I', new_value))

            print(f"Successfully modified cluster {cluster_to_modify} to value {new_value}.")
    except FileNotFoundError:
        print(f"Drive {drive_path} not found. Please check the path.")
    except PermissionError:
        print("Permission denied. Please run the script as root.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print("WARNING: Modifying the FAT table can corrupt the file system. Proceed with caution.")
    print("Ensure the drive is not mounted before modifying the FAT table.")
    drive_path = input("Enter the USB drive path (e.g., /dev/sdb): ").strip()
    try:
        cluster_to_modify = int(input("Enter the cluster number to modify (integer): ").strip())
        new_value = int(input("Enter the new value for the cluster (integer or hex, e.g., 4 or 0xFFFFFF8): ").strip(), 0)
        modify_fat_table(drive_path, cluster_to_modify, new_value)
    except ValueError:
        print("Invalid input: Cluster number and value must be integers or hex (e.g., 0x4).")
