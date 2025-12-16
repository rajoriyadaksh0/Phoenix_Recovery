import struct

SECTOR_SIZE = 512  # Sector size in bytes


def read_sector(disk, sector_num):
    """
    Reads a sector from the disk.
    """
    disk.seek(sector_num * SECTOR_SIZE)
    return bytearray(disk.read(SECTOR_SIZE))  # Convert to bytearray for mutability


def write_sector(disk, sector_num, data):
    """
    Writes a sector to the disk.
    """
    disk.seek(sector_num * SECTOR_SIZE)
    disk.write(data)


def add_directory_entry(disk_path, file_name, file_size, starting_cluster):
    """
    Adds a directory entry for a new file to the root directory in a FAT32 file system.

    :param disk_path: Path to the disk image or device (e.g., '/dev/sda1').
    :param file_name: Name of the file in 8.3 format (11 characters).
    :param file_size: Size of the file in bytes.
    :param starting_cluster: Starting cluster of the file.
    """
    try:
        # Open the disk for both reading and writing
        with open(disk_path, 'r+b') as disk:
            # Read the boot sector
            boot_sector = read_sector(disk, 0)

            # Parse boot sector to get file system parameters
            bytes_per_sector = struct.unpack_from("<H", boot_sector, 11)[0]
            sectors_per_cluster = struct.unpack_from("<B", boot_sector, 13)[0]
            reserved_sectors = struct.unpack_from("<H", boot_sector, 14)[0]
            num_fats = struct.unpack_from("<B", boot_sector, 16)[0]
            fat_size = struct.unpack_from("<I", boot_sector, 36)[0]
            root_cluster = struct.unpack_from("<I", boot_sector, 44)[0]

            # Calculate the data region start sector
            data_start = reserved_sectors + (num_fats * fat_size)

            # Calculate the first sector of the root directory
            first_sector = data_start + (root_cluster - 2) * sectors_per_cluster

            # Iterate through the directory sectors to find an empty entry
            for cluster_offset in range(sectors_per_cluster):
                sector_data = read_sector(disk, first_sector + cluster_offset)

                for offset in range(0, SECTOR_SIZE, 32):  # FAT32 directory entries are 32 bytes each
                    entry = sector_data[offset:offset + 32]

                    # Check if the entry is empty (0x00 or 0xE5)
                    if entry[0] in (0x00, 0xE5):
                        # Create a new directory entry
                        new_entry = bytearray(32)
                        new_entry[:11] = file_name.ljust(11, ' ').encode('ascii')  # File name in 8.3 format
                        new_entry[11] = 0x20  # Attribute: Archive
                        struct.pack_into("<H", new_entry, 20, (starting_cluster >> 16) & 0xFFFF)  # High cluster
                        struct.pack_into("<H", new_entry, 26, starting_cluster & 0xFFFF)  # Low cluster
                        struct.pack_into("<I", new_entry, 28, file_size)  # File size

                        # Replace the empty entry with the new one
                        sector_data[offset:offset + 32] = new_entry
                        write_sector(disk, first_sector + cluster_offset, sector_data)

                        print(f"Added entry for file '{file_name}' at cluster {starting_cluster} with size {file_size} bytes.")
                        return

            print("No empty directory entry found.")
    except FileNotFoundError:
        print("Error: Disk not found.")
    except Exception as e:
        print(f"Error: {e}")


# Example Usage
if __name__ == "__main__":
    try:
        disk_path = input("Enter the path to the disk image or device (e.g., '/dev/sda1'): ")
        file_name = input("Enter the file name (8.3 format, e.g., FILE    TXT): ").strip()
        if len(file_name) > 11:
            raise ValueError("File name exceeds 11 characters (8.3 format).")

        file_size = int(input("Enter the file size in bytes: "))
        starting_cluster = int(input("Enter the starting cluster: "))

        add_directory_entry(disk_path, file_name, file_size, starting_cluster)
    except Exception as e:
        print(f"Error: {e}")
