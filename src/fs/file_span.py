import struct

SECTOR_SIZE = 512  # Standard sector size in bytes


def calculate_file_clusters(disk_path, file_size):
    """
    Calculates the number of clusters required for a file given its size on a FAT32 file system.

    :param disk_path: Path to the disk image or device (e.g., '/dev/sda1').
    :param file_size: Total size of the file in bytes.
    :return: A tuple containing the cluster size and the number of clusters required.
    """
    try:
        with open(disk_path, 'rb') as disk:
            # Read the boot sector (first 512 bytes)
            boot_sector = disk.read(SECTOR_SIZE)
            
            # Extract relevant fields
            bytes_per_sector = struct.unpack_from("<H", boot_sector, 11)[0]
            sectors_per_cluster = struct.unpack_from("<B", boot_sector, 13)[0]
            
            # Calculate cluster size
            cluster_size = bytes_per_sector * sectors_per_cluster
            
            # Calculate the number of clusters required
            clusters_needed = (file_size + cluster_size - 1) // cluster_size
            
            return clusters_needed
    except FileNotFoundError:
        raise FileNotFoundError("Error: Disk or file not found.")
    except Exception as e:
        raise RuntimeError(f"Error reading boot sector: {e}")


# Example Usage
if __name__ == "__main__":
    try:
        disk_path = input("Enter the path to the disk image or device (e.g., '/dev/sda1'): ")
        file_size = int(input("Enter the total size of the file (in bytes): "))
        
        cluster_size, clusters_needed = calculate_file_clusters(disk_path, file_size)
        
        print(f"Cluster size detected: {cluster_size} bytes")
        print(f"The file spans {clusters_needed} cluster(s).")
    except Exception as e:
        print(f"Error: {e}")
