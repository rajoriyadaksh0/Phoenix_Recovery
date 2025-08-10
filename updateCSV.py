from model import recover,print_clusters
import pandas as pd


file_path='./data.csv'


import os

def read_cluster_content(drive_path, cluster_number):
    try:
        with open(drive_path, "rb") as disk:
            disk.seek(0)  # Move to the beginning of the drive
            boot_sector = disk.read(512)  # Read Boot Sector

            bytes_per_sector = int.from_bytes(boot_sector[11:13], "little")
            sectors_per_cluster = boot_sector[13]
            reserved_sectors = int.from_bytes(boot_sector[14:16], "little")
            fat_count = boot_sector[16]
            fat_size = int.from_bytes(boot_sector[36:40], "little")

            cluster_size = bytes_per_sector * sectors_per_cluster
            fat_region_size = fat_count * fat_size * bytes_per_sector
            data_start_offset = (reserved_sectors * bytes_per_sector) + fat_region_size

            cluster_offset = data_start_offset + (cluster_number - 2) * cluster_size

            disk.seek(0, os.SEEK_END)
            total_size = disk.tell()
            if cluster_offset + cluster_size > total_size:
                raise ValueError("Cluster number out of range for this drive.")

            disk.seek(cluster_offset)
            cluster_data = disk.read(cluster_size)

            # Remove NULL characters before decoding
            cleaned_data = cluster_data.replace(b'\x00', b'')  

            # Attempt to decode as text
            try:
                text_content = cleaned_data.decode('utf-8').strip()
                if text_content:
                    return text_content  
            except UnicodeDecodeError:
                pass  

            return cleaned_data.hex()  

    except FileNotFoundError:
        return f"Error: Drive {drive_path} not found. Please check the path."
    except PermissionError:
        return "Error: Permission denied. Please run the script as root."
    except Exception as e:
        return f"Error: {e}"




def update_csv(orphan_clusters, drive_path):
    """
    Updates the data.csv file with content retrieved from orphan clusters.
    
    :param orphan_clusters: List of orphan cluster numbers.
    :param drive_path: Path to the drive where cluster data is stored.
    """
    file_path = "./data.csv"
    data = pd.read_csv(file_path, on_bad_lines='skip')  # Load existing data
    
    new_data = []
    for cluster in orphan_clusters:
        content = read_cluster_content(drive_path, cluster)
        if content:
            cleaned_content = content.replace("\n", " ").replace("\r", " ")  # Remove new lines
            new_data.append({'cluster_number': cluster, 'content': cleaned_content})
    
    # Append new data to the existing dataframe and save it back
    updated_data = pd.concat([data, pd.DataFrame(new_data)], ignore_index=True)
    updated_data.to_csv(file_path, index=False)


# drive_path="123"
# orphan_clusters=[]
# n_cluster=4
# update_csv(orphan_clusters, drive_path)

# input_clusters = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 18]
# grouped_clusters = recover(file_path, input_clusters, n_clusters=4, start_cluster=4)


# print_clusters(grouped_clusters,start_cluster=4)

