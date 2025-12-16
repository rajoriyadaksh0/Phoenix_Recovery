from src.fs import total_clusters
from src.fs import edit_dir_table
from src.fs import edit_fat_table
from src.utils import orphanClusters
from src.fs import file_span
# from src.utils.model import recover

def recovery_func(file_name , starting_cluster , size,disk_path):
    noOfClusters = total_clusters.calculate_total_clusters(disk_path)
    noOfFileCluster = file_span.calculate_file_clusters(disk_path,int(size))
    print("The total clusters the file span is ",noOfFileCluster)
    if(noOfFileCluster > 1):
        arr = orphanClusters.orphanClusters(disk_path,noOfClusters)

        # print("orphan", arr)
        
        
        # for i in arr:
        #     print(i , end=" ")

        # update_csv(arr,disk_path)

        # new_arr = recover("./data.csv",arr,5,13)
        # print(new_arr)

        # for i in range(len(new_arr)-1):
        #     edit_fat_table.modify_fat_table(disk_path,new_arr[i],new_arr[i+1])
        # edit_dir_table(disk_path,new_arr[-1],0xFFFFFF8)
        # return True


        for i in range(int(starting_cluster),int(starting_cluster)+noOfFileCluster-1):
            edit_fat_table.modify_fat_table(disk_path,i,i+1)
        edit_fat_table.modify_fat_table(disk_path,int(starting_cluster)+noOfFileCluster,0xFFFFFF8)
        edit_dir_table.add_directory_entry(disk_path,file_name,int(size),int(starting_cluster))
        return True



    else:

        edit_dir_table.add_directory_entry(disk_path,file_name,int(size),int(starting_cluster))
        edit_fat_table.modify_fat_table(disk_path,int(starting_cluster),0xFFFFFF8)

        return True


