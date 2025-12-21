import pandas as pd
import streamlit as st
import time
def duplicates(data):
    duplicates = data.duplicated().sum()
    return duplicates

def missing_val(data):
        missing_values = data.isna().any().any()
        return missing_values

def fill_NaN(data):
        fillna_selection = st.selectbox("Choose a method to fill NaN values",options=["Select method","Forward Fill","Backward Fill"],index=0)
        if fillna_selection != "Select method":
            if fillna_selection == "Forward Fill":
                time.sleep(1.5)
                data.fillna(method = "ffill",inplace = True)
                st.success("Forward Fill completed.")
                return data
            elif fillna_selection == "Backward Fill":
                time.sleep(1.5)
                data.fillna(method = "bfill",inplace = True)
                st.success("Forward Fill completed.")
                return data
        else:
            st.info("Select a method.")


def clean_data(data):
    if duplicates(data) or missing_val(data):
        if duplicates(data) and not missing_val(data): 
            st.info("We founded some duplicated rows")
            st.write(f"Duplicated rows: {duplicates(data)}")
            time.sleep(2.5)
            data.drop_duplicates(inplace = True)
            st.success("Duplicates removed successfully.")
            return data
        elif not duplicates(data) and missing_val(data):
            st.info("We founded some missing values.")
            st.write(data.isna().sum().reset_index(name = "NaN_Counts").rename({"index": "Columns"}))
            data = fill_NaN(data)
            return data
        elif duplicates(data) and missing_val(data):
            st.info("We founded some duplicated rows and missing values.")
            st.write(f"Duplicated rows: {duplicates(data)}")
            st.write(data.isna().sum().reset_index(name = "NaN_Counts").rename({"index": "Columns"}))
            time.sleep(1.5)
            data.drop_duplicates(inplace = True)
            st.success("Duplicates removed successfully.")
            data = fill_NaN(data)
            return data
    else:
        st.info("Data is clean.")
        return None