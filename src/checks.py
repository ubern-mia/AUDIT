import subprocess
import os

# def run_itk_snap(img_path, seg_path):
#     # Verificar si la ruta del archivo de imagen existe
#     if not os.path.exists(img_path):
#         print("El archivo de imagen no se encuentra en la ruta especificada.")
#     else:
#         # Comando para abrir ITK-SNAP con el archivo de imagen
#         subprocess.run(["open", "-n", "-a", "ITK-SNAP", "--args", "-g", img_path, "-s", seg_path])
#
#
# # Ruta al archivo de imagen que deseas abrir
# img_path = "/Users/caumente/Projects/robustness/real_datasets/fda/fda_images/1-006-01/1-006-01_t1ce.nii.gz"
# seg_path = "/Users/caumente/Projects/robustness/real_datasets/fda/fda_images/1-006-01/1-006-01_seg.nii.gz"
#
# run_itk_snap(img_path, seg_path)


def rename_files(root_dir):
    for subdir, _, files in os.walk(root_dir):
        folder_name = subdir.split("/")[-1]
        for file in files:
            old_file_path = os.path.join(subdir, file)
            new_file_name = f'{folder_name}_{file.split("_")[1:][0]}'
            new_file_path = os.path.join(subdir, new_file_name)
            os.rename(old_file_path, new_file_path)
            # print(f"Renamed: {old_file_path} -> {new_file_path}")
            # if file.endswith("t1c.nii.gz"):
            #     old_file_path = os.path.join(subdir, file)
            #     new_file_name = file.replace("t1c.nii.gz", "t1ce.nii.gz")
            #     new_file_path = os.path.join(subdir, new_file_name)
            #     os.rename(old_file_path, new_file_path)
            #     print(f"Renamed: {old_file_path} -> {new_file_path}")


rename_files("/Users/caumente/Projects/robustness/real_datasets/ucsf_postoperative/")
