import psutil

def list_connected_disks():
    disks = psutil.disk_partitions()
    disk_devices = [disk.device for disk in disks if 'cdrom' not in disk.opts]
    return disk_devices

# Example usage
disks = list_connected_disks()
print("Connected Disks:", disks)
