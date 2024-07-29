
import warnings
import os
warnings.simplefilter(action="ignore", category=FutureWarning)

import streamlit as st


def get_dir_name(dir_path):

    if "/" in dir_path:
        dir_name = dir_path.rsplit("/", 1)[0]
    else:
        dir_name = os.getcwd()

    return dir_name


def get_dir_path(dir_str=None, dir_path=None):

    if dir_path is None:
        dir_path = os.getcwd()

    if dir_str is not None:
        dir_path += f"/{dir_str}"

    return dir_path

def get_file_path(file_name, dir_str=None, dir_path=None, pre_str=True):

    file_path = get_dir_path(dir_str=dir_str, dir_path=dir_path)
    file_path += "/"
    if pre_str and dir_str != None:
        file_path += dir_str
        file_path += "_"
    file_path += file_name

    return file_path


from src.app.util.pages.Home_Page import home_page
from src.app.util.pages.Univariate_Feature_Analysis import univariate
from src.app.util.pages.Multivariate_Feature_Analysis import multivariate
from src.app.util.pages.Segmentation_Error_Matrix import matrix
from src.app.util.pages.Model_Performance_Analysis import performance
from src.app.util.pages.Pairwise_Model_Performance_Comparison import pairwise_comparison
from src.app.util.pages.Multi_Model_Performance_Comparison import multi_model
from src.app.util.pages.Longitudinal_Measurements import longitudinal
from src.app.util.pages.Subjects_Exploration import subjects



class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({"title": title, "function": func})

    def run(self):
        # img = Image.open(
        #     get_file_path(
        #         "rascore_logo.png",
        #         dir_path=f"{get_dir_name(__file__)}/{util_str}/{data_str}",
        #     ),
        # )

        st.set_page_config(page_title="AUDIT", page_icon=":brain", layout="wide")

        st.sidebar.markdown("## Main Menu")
        app = st.sidebar.selectbox(
            "Select Page", self.apps, format_func=lambda app: app["title"]
        )
        st.sidebar.markdown("---")
        app["function"]()


app = MultiApp()

app.add_app("Home Page", home_page)
app.add_app("Univariate Analysis", univariate)
app.add_app("Multivariate Analysis", multivariate)
app.add_app("Segmentation Error Matrix", matrix)
app.add_app("Model Performance Analysis", performance)
app.add_app("Pairwise Model Performance Comparison", pairwise_comparison)
app.add_app("Multi-model Performance Comparison", multi_model)
app.add_app("Longitudinal Measurements", longitudinal)
app.add_app("Subjects Exploration", subjects)

app.run()
