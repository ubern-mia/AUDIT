import os
import shutil
import re
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


def ls_files(path: str) -> list:
    """
    Lists all files within a given path and returns their names in sorted order.

    Args:
        path: The directory path where to look for files.

    Returns:
        list: A sorted list of files names found within the specified path.
    """
    return sorted([f.path.split("/")[-1] for f in os.scandir(path) if f.is_file()])


def load_config_file(path: str) -> dict:
    """
    Loads a configuration file in YAML format and returns its contents as a dictionary.

    Args:
        path: The file path to the YAML configuration file.

    Returns:
        dict: The contents of the YAML file as a dictionary.
    """

    def replace_variables(config, variables):
        def replace(match):
            return variables.get(match.group(1), match.group(0))

        for key, value in config.items():
            if isinstance(value, str):
                config[key] = re.sub(r"\$\{(\w+)\}", replace, value)
            elif isinstance(value, dict):
                replace_variables(value, variables)

    with open(path, "r") as file:
        config = yaml.safe_load(file)

    variables = {key: value for key, value in config.items() if not isinstance(value, dict)}
    replace_variables(config, variables)

    return config


def rename_directories(path: str, old_name: str, new_name: str, verbose=False):
    """
    Renames all directories and subdirectories within a directory,
    replacing string_1 with string_2 in their names.

    Args:
        path (str): Path to the directory where renaming will be performed.
        old_name (str): The string to be replaced in the directory names.
        new_name (str): The new string that will replace string_1.
    """

    # Traverse the directory tree, renaming directories from the bottom up
    for root, dirs, files in os.walk(path, topdown=False):
        for dir_name in dirs:
            if old_name in dir_name:
                new_dir_name = dir_name.replace(old_name, new_name)
                old_dir_path = os.path.join(root, dir_name)
                new_dir_path = os.path.join(root, new_dir_name)
                os.rename(old_dir_path, new_dir_path)

                if verbose:
                    print(f"Directory renamed: {old_dir_path} -> {new_dir_path}")


def rename_files(path: str, old_name: str = "_t1ce", new_name: str = "_t1c", verbose=False):
    """
    Renames files in a directory and its subdirectories by replacing a specific substring in the filenames.

    This function recursively walks through all files in a specified root directory and its subdirectories,
    identifies files containing a specified old extension substring, and renames them by replacing
    the old extension with a new one.

    Args:
        path: The root directory containing the files to be renamed.
        old_name: The substring in filenames that needs to be replaced. Defaults to "_t1ce".
        new_name: The substring that will replace the old extension. Defaults to "_t1c".
        verbose: Whether print the log
    """
    if old_name is None:
        old_name = ""

    if new_name is None:
        new_name = ""

    for subdir, _, files in os.walk(path):
        for file in files:
            # Check if the file contains the old extension
            if old_name in file:
                # Construct the old and new file paths
                old_file_path = os.path.join(subdir, file)
                new_file_path = os.path.join(subdir, file.replace(old_name, new_name))

                # Rename the file
                os.rename(old_file_path, new_file_path)

                if verbose:
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


def delete_files_by_extension(root_dir: str, ext: str, verbose=False):
    """
    Deletes all files with a specific extension in a directory and its subdirectories.

    Args:
        root_dir: The root directory where the search will start.
        ext: The file extension of the files to be deleted.
        verbose: Whether print the log
    """
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(ext):
                file_path = os.path.join(subdir, file)
                os.remove(file_path)
                if verbose:
                    print(f"Deleted file: {file_path}")


def organize_files_into_folders(folder_path, extension='.nii.gz', verbose=False):
    # List all files in the given folder
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    for file in files:
        # Extract the file name without extension (excluding .nii.gz)
        file_name = file.split(extension)[0]

        # Create a new folder for the file
        folder_name = os.path.join(folder_path, file_name)
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Move the file into the new folder
        src_path = os.path.join(folder_path, file)
        dst_path = os.path.join(folder_name, file)
        shutil.move(src_path, dst_path)
        if verbose:
            print(f"Organizing file: {file}")

    print(f"Organized {len(files)} files into respective folders.")


def add_suffix_to_files(folder_path, suffix='pred', ext='.nii.gz', verbose=False):
    # Walk through all subfolders and files in the given folder
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # Check if the file is a .nii.gz file
            if file.endswith(ext):
                # Construct the old file path
                old_file_path = os.path.join(root, file)

                # Split the file name and add the "_pred" suffix before ".nii.gz"
                new_file_name = file.replace(ext, f'{suffix}{ext}')

                # Construct the new file path
                new_file_path = os.path.join(root, new_file_name)

                # Rename the file
                os.rename(old_file_path, new_file_path)

                if verbose:
                    print(f"Renaming file: {old_file_path} to {new_file_path}")

    print("Renaming completed.")


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
