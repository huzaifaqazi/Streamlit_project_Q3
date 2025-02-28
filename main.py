import streamlit as st
import os
from io import BytesIO
import pandas as pd

st.set_page_config(page_title="Data Sweeper", layout="wide")

st.markdown(
    """"
    <style>
    stApp {
        background-color: blacl;
        color: white;
        }
    """,
    unsafe_allow_html=True
)

# Title and description
st.title("Data Sweeper Sterling integration")
st.write("This app is designed to help you clean your data before you upload it to Sterling.")

file_upload = st.file_uploader("Upload your data", type=["csv","xlsx"] , accept_multiple_files=(True))

if file_upload:
    for file in file_upload:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error("unsupported file format")
            continue
        

        # file details
        st.write("Preview of the data")
        st.dataframe(df.head())

        # data cleaning options
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"cleaning data for {file.name}"):
            col1,col2 = st.columns(2)
            with col1:
                if st.button("Remove Duplicates file {file.name}"):
                    df = df.drop_duplicates(inplace=True)
                    st.write("Duplicates removed")
            with col2:
                if st.button(f"file missing Values {file.name}"):
                    numeric_cols = df.select_dtypes(include=["number"]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values filled" )


        st.subheader("Select Column to keep")
        cols = st.multiselect(f"Choose columns for {file.name}", df.columns , default=df.columns)
        df = df[cols]


        # Data visualization
        st.subheader("Data Visualization")
        if st.checkbox(f"Show data visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include="number").iloc[:100, :])

        # conversion
        st.subheader("Data Conversion options")
        conversions = st.radio(f"Select {file.name} to:", [" CSV", "Excel"] , key=file.name)
        if st.button(f"Convert {file.name}"):
            Buffeer = BytesIO()
            if conversions == "CSV":
                df.to_csv(Buffeer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversions == "Excel":
                df.to_excel(Buffeer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            Buffeer.seek(0)

            st.download_button(
                label=f"Download {file.name} as {conversions}",
                data=Buffeer,
                file_name=file_name,
                mime=mime_type
            )