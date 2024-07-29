
# -*- coding: utf-8 -*-
"""
  Copyright 2022 Mitchell Isaac Parker

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

"""

import streamlit as st
from PIL import Image


def home_page():
    import streamlit as st
    import base64

    def img_to_base64(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()

    # Load and display sidebar image with glowing effect
    img_path = "./src/app/util/images/artorg_logo.gif"
    audit_logo = Image.open("/Users/caumente/Projects/AUDIT/src/app/util/images/audit_logo.png")
    audit_schema = Image.open("/Users/caumente/Projects/AUDIT/src/app/util/images/audit_schema.png")
    img_base64 = img_to_base64(img_path)


    # Set page title and favicon
    # st.set_page_config(page_title="Project Homepage", page_icon=":brain:", layout="wide",
    #                    initial_sidebar_state="expanded", )

    left_col, right_col = st.columns([2, 1])

    left_col.title("Welcome to AUDIT")
    left_col.markdown("""
        <h3>A tool for analyzing dataset distribution and comparing model performance</h3>
        <p style="margin: 5px 0;"><b>Created by Carlos Aumente Maestro</b></p>
        <p style="margin: 5px 0;"><b>Artificial Intelligence Center, University of Oviedo</b></p>
        <p style="margin: 5px 0;"><b>ARTORG - Center for Biomedical Engineering Research, University of Bern</b></p>
    """, unsafe_allow_html=True)


    right_col.image(audit_logo, output_format="PNG")
    # st.sidebar.image("./src/app/util/images/artorg_logo.gif", use_column_width=False)
    # st.sidebar.image("./src/app/util/images/uniovi_logo.png", use_column_width=False)

    st.markdown("---")

    st.header("""Summary""")

    st.write("""AUDIT, Analysis & evalUation Dashboard of artIficial inTelligence, is a tool designed to analyze,
    visualize, and detect biases in brain MRI data and models. It provides tools for loading and processing MRI data,
    extracting relevant features, and visualizing model performance and biases in predictions. AUDIT presents the 
    following features:""")

    st.markdown("""
        - **Data management**: Easily work with MRI data from various sources.
        - **Feature extraction**: Extract relevant features from MRI images and their segmentations for analysis.
        - **Visualization**: Visualize model performance, including false positives and negatives, using interactive plots.
        - **Model robustness**: Assess the robustness of the model by evaluating its performance across different datasets and conditions.
        - **Bias detection**: Identify potential biases in model predictions and performance.
        - **Longitudinal analysis**: Track your model performance over different timepoints.
    """)

    st.markdown("""
    Details of our work are provided in the -------- paper. We hope that researchers will use AUDIT to gain novel 
    insights into data and model evaluation.
    """)

    st.image(audit_schema, output_format="PNG")

    st.header("""Usage""")
    st.markdown("""
        - **Home Page**: The main landing page of the tool.
        - **Univariate Analysis**: Analysis of individual variables to understand their distributions and characteristics.
        - **Multivariate Analysis**: Examination of multiple variables simultaneously to explore relationships and patterns.
        - **Segmentation Error Matrix**: A table displaying the errors associated with different segmentation tasks.
        - **Model Performance Analysis**: Evaluation of the effectiveness and accuracy of a single model.
        - **Pairwise Model Performance Comparison**: Comparison of performance metrics between two different models.
        - **Multi-model Performance Comparison**: Comparative analysis of performance metrics across multiple models.
        - **Longitudinal Measurements**: Analysis of data collected over time to observe trends and changes.
        - **Subjects Exploration**: Detailed examination of individual subjects within the dataset.
        """)

    st.markdown("---")


    left_info_col, right_info_col = st.columns(2)

    left_info_col.markdown(
        f"""
        ### Authors
        Please feel free to contact us with any issues, comments, or questions. [Contact Us](UO297103@uniovi.es)

        ##### Carlos Aumente [![Twitter URL](https://img.shields.io/twitter/url/https/twitter.com/bukotsunikki.svg?style=social&label=Follow%20%40Mitch_P)](https://twitter.com/Mitch_P)

        - Email:  <carlosaumente@gmail.com> or <UO297103@uniovi.es>
        - GitHub: https://github.com/caumente/

        ##### Mauricio Reyes [![Twitter URL](https://img.shields.io/twitter/url/https/twitter.com/bukotsunikki.svg?style=social&label=Follow%20%40RolandDunbrack)](https://twitter.com/RolandDunbrack)

        - Email: <------------>
        """,
        unsafe_allow_html=True,
    )

    right_info_col.markdown(
        """
        ### Funding

        - NIH NIGMS F30 GM142263 (to M.P.)
        - NIH NIGMS R35 GM122517 (to R.D.)
         """
    )

    right_info_col.markdown(
        """
        ### License
        Apache License 2.0
        """
    )
    right_info_col.markdown(
        """
        ### Documentation
        [Documentation](#) 
        [GitHub Repository](#) 
        Under Apache License 2.0
        """
    )

    # Add a footer
    st.markdown("---")
    st.write("© 2024 AUDIT project")
