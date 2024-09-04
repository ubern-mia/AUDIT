import warnings

import streamlit as st

from src.app.util.pages.Home_Page import home_page
from src.app.util.pages.Longitudinal_Measurements import longitudinal
from src.app.util.pages.Model_Performance_Analysis import performance
from src.app.util.pages.Multi_Model_Performance_Comparison import multi_model
from src.app.util.pages.Multivariate_Feature_Analysis import multivariate
from src.app.util.pages.Pairwise_Model_Performance_Comparison import pairwise_comparison
from src.app.util.pages.Segmentation_Error_Matrix import matrix
from src.app.util.pages.Subjects_Exploration import subjects
from src.app.util.pages.Univariate_Feature_Analysis import univariate

warnings.simplefilter(action="ignore", category=FutureWarning)


class AUDITApp:
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
        app = st.sidebar.selectbox("Select Page", self.apps, format_func=lambda app: app["title"])
        st.sidebar.markdown("---")
        app["function"]()


app = AUDITApp()
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
