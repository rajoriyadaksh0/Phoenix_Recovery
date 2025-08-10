import struct

SECTOR_SIZE = 512

def read_sector(file, sector_num):
    """Reads a specific sector from the file."""
    file.seek(sector_num * SECTOR_SIZE)
    return file.read(SECTOR_SIZE)

def calculate_total_clusters(disk_path):
    """Calculates the total number of clusters in a FAT32 disk image."""
    try:
        with open(disk_path, "rb") as disk:
            # Read the boot sector
            boot_sector = read_sector(disk, 0)

            # Parse boot sector to get filesystem parameters
            total_sectors = struct.unpack_from("<I", boot_sector, 19)[0]  # Total sectors (can be in FAT12/FAT16)
            sectors_per_cluster = struct.unpack_from("<B", boot_sector, 13)[0]
            reserved_sectors = struct.unpack_from("<H", boot_sector, 14)[0]
            num_fats = struct.unpack_from("<B", boot_sector, 16)[0]
            fat_size = struct.unpack_from("<I", boot_sector, 36)[0]
            root_cluster = struct.unpack_from("<I", boot_sector, 44)[0]

            # If total sectors is 0, calculate total sectors using 32-bit total sectors (e.g., larger disks)
            if total_sectors == 0:
                total_sectors = struct.unpack_from("<I", boot_sector, 32)[0]

            # Calculate the total number of clusters
            data_start = reserved_sectors + (num_fats * fat_size)
            total_clusters = (total_sectors - data_start) // sectors_per_cluster

            return total_clusters

    except FileNotFoundError:
        print(f"Error: Disk file '{disk_path}' not found.")
    except PermissionError:
        print(f"Error: Insufficient permissions to access '{disk_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example Usage
disk_path = "/dev/sda1"  # Replace with your disk image path
total_clusters = calculate_total_clusters(disk_path)

if total_clusters:
    print(f"Total Clusters: {total_clusters}")
else:
    print("Could not calculate total clusters.")
