import os
import struct

def read_specific_cluster_details_in_fat(drive_path, cluster_number):
    try:
        # Ensure the drive exists and is accessible
        if not os.path.exists(drive_path):
            raise FileNotFoundError(f"Drive {drive_path} not found. Please check the path.")

        # Open the drive in binary read mode
        with open(drive_path, "rb") as disk:
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

            # Step 2: Read the FAT
            disk.seek(fat_start)
            fat_table = disk.read(fat_size_bytes)

            # Step 3: Validate Cluster Number
            total_clusters = len(fat_table) // 4
            if cluster_number < 2 or cluster_number >= total_clusters:
                raise ValueError(f"Invalid cluster number: {cluster_number}. Valid range is 2 to {total_clusters - 1}.")

            # Step 4: Parse the FAT Entry for the Given Cluster
            entry_offset = cluster_number * 4  # Each FAT32 entry is 4 bytes
            cluster_entry = int.from_bytes(fat_table[entry_offset:entry_offset + 4], "little")

            # Step 5: Determine Occupied/Free and Pointer
            # if cluster_entry == 0x00000000:
            #     status = "Free"
            #     pointer = None
            # elif 0x00000002 <= cluster_entry <= 0x0FFFFFEF:
            #     status = "Occupied"
            #     pointer = cluster_entry
            # elif cluster_entry >= 0x0FFFFFF8:
            #     status = "End of Chain"
            #     pointer = None
            # else:
            #     status = "Reserved/Bad Cluster"
            #     pointer = None

            # print(f"Cluster {cluster_number} details:")
            # print(f"  Status: {status}")
            # print(f"  Pointer (next cluster): {pointer}")
            # return {"status": status, "pointer": pointer}




            if cluster_entry == 0x00000000:
                status = "Free"
                pointer = None
                return True
            elif 0x00000002 <= cluster_entry <= 0x0FFFFFEF:
                status = "Occupied"
                pointer = cluster_entry
            elif cluster_entry >= 0x0FFFFFF8:
                status = "End of Chain"
                pointer = None
            else:
                status = "Reserved/Bad Cluster"
                pointer = None
            return False

    except FileNotFoundError:
        print(f"Drive {drive_path} not found. Please check the path.")
    except PermissionError:
        print("Permission denied. Please run the script as root.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None




def read_cluster_content(drive_path, cluster_number):
    try:
        # Open the drive in binary mode
        with open(drive_path, "rb") as disk:
            # Step 1: Read Boot Sector
            disk.seek(0)  # Move to the beginning of the drive
            boot_sector = disk.read(512)  # Read the first 512 bytes (Boot Sector)

            # Extract necessary information from the Boot Sector
            bytes_per_sector = int.from_bytes(boot_sector[11:13], "little")
            sectors_per_cluster = boot_sector[13]
            reserved_sectors = int.from_bytes(boot_sector[14:16], "little")
            fat_count = boot_sector[16]
            fat_size = int.from_bytes(boot_sector[36:40], "little")

            # Calculate offsets and sizes
            cluster_size = bytes_per_sector * sectors_per_cluster
            fat_region_size = fat_count * fat_size * bytes_per_sector
            data_start_offset = (reserved_sectors * bytes_per_sector) + fat_region_size

            # Calculate the offset of the target cluster
            cluster_offset = data_start_offset + (cluster_number - 2) * cluster_size

            # Validate cluster number
            disk.seek(0, os.SEEK_END)  # Move to the end to get total size
            total_size = disk.tell()
            if cluster_offset + cluster_size > total_size:
                raise ValueError("Cluster number out of range for this drive.")

            # Read the content of the specified cluster
            disk.seek(cluster_offset)
            cluster_data = disk.read(cluster_size)

            # Attempt to decode as text
            try:
                text_content = cluster_data.decode('utf-8').strip()
                # print(len(text_content.strip()))
                if text_content and text_content.strip() and any(c.isprintable() for c in text_content):
                    return True
    
                return False

            except UnicodeDecodeError:
                # print(f"Cluster {cluster_number} contains non-text binary data.")
                # print(f"Hexadecimal representation:")
                # print(cluster_data.hex())
                return False
            return False

    except FileNotFoundError:
        print(f"Drive {drive_path} not found. Please check the path.")
    except PermissionError:
        print("Permission denied. Please run the script as root.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return False




def cluster_status(path,number):
    if(read_specific_cluster_details_in_fat(path,number)):
        return read_cluster_content(path,number)
    else:
        return False



def orphanClusters(drive_path, totalClusters):
    arr = []
    for i in range(2, 1000):
        # print(i)
        if cluster_status(drive_path, i):
            arr.append(i)

    return arr


print(cluster_status("/dev/sda1",24))

