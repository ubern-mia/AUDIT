import os
import shutil

import pandas as pd
import yaml


def ls_dirs(path: str) -> list:
    """
    Lists all directories within a given path and returns their names in sorted order.

    Args:
        path: The directory path where to look for subdirectories.

    Returns:
        list: A sorted list of directory names found within the specified path.
    """
    return sorted([f.path.split("/")[-1] for f in os.scandir(path) if f.is_dir()])


def load_config_file(path: str) -> dict:
    """
    Loads a configuration file in YAML format and returns its contents as a dictionary.

    Args:
        path: The file path to the YAML configuration file.

    Returns:
        dict: The contents of the YAML file as a dictionary.
    """
    with open(path) as cf:
        config = yaml.load(cf, Loader=yaml.FullLoader)
        return config


def rename_files(root_dir: str, old_ext: str = "_t1ce", new_ext: str = "_t1c"):
    """
    Renames files in a directory and its subdirectories by replacing a specific substring in the filenames.

    This function recursively walks through all files in a specified root directory and its subdirectories,
    identifies files containing a specified old extension substring, and renames them by replacing
    the old extension with a new one.

    Args:
        root_dir: The root directory containing the files to be renamed.
        old_ext: The substring in filenames that needs to be replaced.
                                 Defaults to "_t1ce".
        new_ext: The substring that will replace the old extension.
                                 Defaults to "_t1c".
    """
    if old_ext is None:
        old_ext = ""

    if new_ext is None:
        new_ext = ""

    for subdir, _, files in os.walk(root_dir):
        for file in files:
            # Check if the file contains the old extension
            if old_ext in file:
                # Construct the old and new file paths
                old_file_path = os.path.join(subdir, file)
                new_file_path = os.path.join(subdir, file.replace(old_ext, new_ext))

                # Rename the file
                os.rename(old_file_path, new_file_path)

                # Print a message indicating the rename operation
                print(f"Renamed: {old_file_path} -> {new_file_path}")


def copy_files_by_extension(src_dir: str, dst_dir: str, ext: str):
    """
    Copies all files with a specific extension from one directory to another.

    Args:
        src_dir: The source directory from which to copy files.
        dst_dir: The destination directory where files will be copied.
        ext: The file extension to search for and copy (e.g., ".txt", ".yaml").
    """
    os.makedirs(dst_dir, exist_ok=True)
    for subdir, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith(ext):
                src_file_path = os.path.join(subdir, file)
                dst_file_path = os.path.join(dst_dir, file)
                shutil.copy2(src_file_path, dst_file_path)
                print(f"Copied: {src_file_path} -> {dst_file_path}")


def delete_files_by_extension(root_dir: str, ext: str):
    """
    Deletes all files with a specific extension in a directory and its subdirectories.

    Args:
        root_dir: The root directory where the search will start.
        ext: The file extension of the files to be deleted.
    """
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(ext):
                file_path = os.path.join(subdir, file)
                os.remove(file_path)
                print(f"Deleted: {file_path}")


def concatenate_csv_files(directory: str, output_file: str):
    """
    Concatenates all CSV files in a specified directory into a single CSV file.

    Args:
        directory: The directory containing the CSV files to concatenate.
        output_file: The path where the concatenated CSV file will be saved.
    """
    csv_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".csv")]
    df_list = [pd.read_csv(csv_file) for csv_file in csv_files]
    concatenated_df = pd.concat(df_list, ignore_index=True)
    concatenated_df.to_csv(output_file, index=False)
    print(f"Concatenated CSV files saved to: {output_file}")


def read_datasets_from_dict(name_path_dict: dict, col_name: str = "set") -> pd.DataFrame:
    """
    Reads multiple datasets from a dictionary of name-path pairs and concatenates them into a single DataFrame.

    Args:
        name_path_dict: A dictionary where keys are dataset names and values are file paths to CSV files.
        col_name: The name of the column to add that will contain the dataset name. Defaults to "set".

    Returns:
        pd.DataFrame: A concatenated DataFrame containing all the datasets, with an additional column specifying
                      the dataset name.
    """

    out = []
    for name, path in name_path_dict.items():
        data = pd.read_csv(path)
        data[col_name] = name
        out.append(data)
    out = pd.concat(out)

    return out
