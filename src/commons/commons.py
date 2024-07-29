import os
import numpy as np
import subprocess
import pandas as pd
import yaml
from colorama import Fore, Style
from tqdm import tqdm


def ls_dirs(path: str) -> list:
    patients_in_path = sorted([f.path.split("/")[-1] for f in os.scandir(path) if f.is_dir()])

    return patients_in_path


def load_csv(path: str) -> pd.DataFrame:
    data = pd.read_csv(path)

    return data


def load_config_file(path: str) -> dict:
    """
    This function load a config file and return the different sections.


    Parameters
    ----------
    path: Path where the config file is stored

    """
    with open(path) as cf:
        config = yaml.load(cf, Loader=yaml.FullLoader)
    # return config['model'], config['optimizer'], config['loss'], config['training'], config['data']
        return config


def add_prefix_dict(dictionary, prefix):
    return {f'{prefix}{k}': v for k, v in dictionary.items()}


def pretty_string(s):
    # Split the string by underscores
    words = s.split('_')

    # Capitalize the first letter of each word
    transformed_words = [word.capitalize() for word in words]

    # Join the words with a space
    result = ' '.join(transformed_words)

    return result


def all_capitals(text):
    return text.upper()


def snake_case(s):
    # Split the string by spaces
    words = s.split(' ')

    # Convert each word to lowercase
    transformed_words = [word.lower() for word in words]

    # Join the words with underscores
    result = '_'.join(transformed_words)

    return result


def read_datasets_from_dict(name_path_dict, col_name="set"):
    out = []
    for name, path in name_path_dict.items():
        data = load_csv(path)
        data[col_name] = name
        out.append(data)
    out = pd.concat(out)

    return out


def run_itk_snap(path, dataset, case, labels=None):
    verification_check = True
    t1 = f"{path}{dataset}/{dataset}_images/{case}/{case}_t1.nii.gz"
    t1c = f"{path}{dataset}/{dataset}_images/{case}/{case}_t1ce.nii.gz"
    t2 = f"{path}{dataset}/{dataset}_images/{case}/{case}_t2.nii.gz"
    flair = f"{path}{dataset}/{dataset}_images/{case}/{case}_flair.nii.gz"
    seg = f"{path}{dataset}/{dataset}_images/{case}/{case}_seg.nii.gz"

    if labels:
        labels_path = f"/Users/caumente/Projects/robustness/itk_labels.txt"
        generate_itk_labels(labels, labels_path)
        command = [
                      "open", "-n", "-a", "ITK-SNAP", "--args",
                      "-l", labels_path,
                      "-g", t1c,
                      "-s", seg,
                      "-o"
                  ] + [t1, t2, flair]
    else:
        command = [
                      "open", "-n", "-a", "ITK-SNAP", "--args",
                      # "-l", t1,
                      "-g", t1c,
                      "-s", seg,
                      "-o"
                  ] + [t1, t2, flair]

    # Checking if both path exist
    if os.path.exists(t1c) and os.path.exists(seg):
        subprocess.run(command)
    # elif os.path.exists(t1c) and not os.path.exists(seg_path):
    #     subprocess.run(["open", "-n", "-a", "ITK-SNAP", "--args", "-g", img_path])
    # elif not os.path.exists(t1c) and os.path.exists(seg_path):
    #     subprocess.run(["open", "-n", "-a", "ITK-SNAP", "--args", "-s", seg_path])
    else:
        verification_check = False

    return verification_check


def generate_itk_labels(labels, output_file):
    # Define colors for each label
    colors = [
        (0, 0, 0),     # Black for BKG
        (255, 255, 0), # Yellow for EDE
        (255, 0, 0),   # Red for ENH
        (0, 0, 255)    # Blue for NEC
    ]

    # Create the file content
    lines = [
        "# ITK-SNAP Label Description File",
        "# Columns = Index, Red, Green, Blue, Visibility, Opacity, Label Name"
    ]

    for name, index in labels.items():
        color = colors[index]
        if index == 0:
            line = f"{index:<2} {color[0]:<3} {color[1]:<3} {color[2]:<3}    0 0 0    \"{name}\""
        else:
            line = f"{index:<2} {color[0]:<3} {color[1]:<3} {color[2]:<3}    1 1 1    \"{name}\""
        lines.append(line)

    # Write the label file
    with open(output_file, 'w') as f:
        for line in lines:
            f.write(line + '\n')


def run_comparison_segmentation_itk_snap(path_seg, path_pred, case, labels=None):
    verification_check = True
    t1 = f"{path_seg}/{case}/{case}_t1.nii.gz"
    t1c = f"{path_seg}/{case}/{case}_t1ce.nii.gz"
    t2 = f"{path_seg}/{case}/{case}_t2.nii.gz"
    flair = f"{path_seg}/{case}/{case}_flair.nii.gz"
    seg = f"{path_seg}/{case}/{case}_seg.nii.gz"
    seg_ai = f"{path_pred}/{case}/{case}_pred.nii.gz"

    if labels:
        labels_path = f"/Users/caumente/Projects/robustness/itk_labels.txt"
        generate_itk_labels(labels, labels_path)
        command = [
                      "open", "-n", "-a", "ITK-SNAP", "--args",
                      "-g", t1c,
                      "-s", seg,
                      "-o", t1, t2, flair, seg_ai,
                      "-l", labels_path
                  ]
    else:
        command = [
                      "open", "-n", "-a", "ITK-SNAP", "--args",
                      "-g", t1c,
                      "-s", seg,
                      "-o", t1, t2, flair, seg_ai
                      # "-l", labels_path
                  ] + [seg_ai]

    # Checking if both path exist
    if os.path.exists(t1c) and os.path.exists(seg):
        subprocess.run(command)
    else:
        verification_check = False

    return verification_check



def remove_null_values_from_dataframe(data):
    return data.replace([np.inf, -np.inf], np.nan).dropna()


def remove_null_values_from_array(arr):
    """
    Remove NaN and infinite values from a numpy array.

    Parameters:
    arr (numpy array): The array from which to remove NaN and infinite values.

    Returns:
    numpy array: The array with NaN and infinite values removed.
    """
    return arr[~np.isnan(arr) & ~np.isinf(arr)]



def fancy_tqdm(**kwargs):
    bar_format = "{l_bar}%s{bar}%s{r_bar}" % (Fore.LIGHTBLUE_EX, Fore.CYAN)
    return tqdm(bar_format=bar_format, **kwargs)


def fancy_print(message, color=Fore.WHITE, symbol='•'):
    print(f" {color}{symbol}{message}{Style.RESET_ALL}")


