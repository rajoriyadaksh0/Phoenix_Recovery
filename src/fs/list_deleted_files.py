import struct

SECTOR_SIZE = 512


def read_sector(file, sector_num):
    """Reads a specific sector from the file."""
    file.seek(sector_num * SECTOR_SIZE)
    return file.read(SECTOR_SIZE)


def list_deleted_files(disk_path):
    """Parses the root directory of a FAT32 disk image to list deleted files."""
    try:
        with open(disk_path, "rb") as disk:
            # Read the boot sector
            boot_sector = read_sector(disk, 0)

            # Parse boot sector to get filesystem parameters
            bytes_per_sector = struct.unpack_from("<H", boot_sector, 11)[0]
            sectors_per_cluster = struct.unpack_from("<B", boot_sector, 13)[0]
            reserved_sectors = struct.unpack_from("<H", boot_sector, 14)[0]
            num_fats = struct.unpack_from("<B", boot_sector, 16)[0]
            fat_size = struct.unpack_from("<I", boot_sector, 36)[0]
            root_cluster = struct.unpack_from("<I", boot_sector, 44)[0]

            # Calculate the start of the data region
            data_start = reserved_sectors + (num_fats * fat_size)

            # Calculate the first sector of the root cluster
            first_sector = data_start + (root_cluster - 2) * sectors_per_cluster

            deleted_files = []

            # Iterate through the sectors of the root directory
            # Read all sectors that may be part of the root directory
            for sector_offset in range(0, 65536, sectors_per_cluster):  # Read multiple sectors
                sector_data = read_sector(disk, first_sector + sector_offset)

                # Iterate through entries in the sector
                for offset in range(0, SECTOR_SIZE, 32):  # FAT32 directory entries are 32 bytes
                    entry = sector_data[offset:offset + 32]

                    # Check if the entry is deleted
                    if entry[0] == 0xE5:
                        # Extract file name (8.3 format)
                        name = entry[1:11].decode("ascii", errors="ignore").rstrip()

                        # Extract other attributes
                        file_size = struct.unpack_from("<I", entry, 28)[0]
                        first_cluster_high = struct.unpack_from("<H", entry, 20)[0]
                        first_cluster_low = struct.unpack_from("<H", entry, 26)[0]
                        first_cluster = (first_cluster_high << 16) | first_cluster_low

                        # Store the entry
                        deleted_files.append([
                            name,
                            file_size,
                            first_cluster]
                        )

                # If there are no entries left, we break the loop
                if len(sector_data.strip(b'\0')) == 0:
                    break

            return deleted_files

    except FileNotFoundError:
        print(f"Error: Disk file '{disk_path}' not found.")
    except PermissionError:
        print(f"Error: Insufficient permissions to access '{disk_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Example Usage
disk_path = "/dev/sda1"  # Replace with your disk image path
deleted_files = list_deleted_files(disk_path)

if deleted_files:
    print("Deleted Files:")
    for file in deleted_files:
        # print(f"[Name]: {file['name']} | [Size]: {file['size']} | [Cluster]: {file['cluster']}")
        print(file)
else:
    print("No deleted files found.")
