import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

def file_uploader():
    uploaded_file = st.file_uploader(
        label="Upload a file",
        type=["csv", "xlsx", "xls"]
    )

    if uploaded_file is None:
        return None

    file_name = uploaded_file.name.lower()

    if file_name.endswith(".csv"):
        st.success("CSV file detected ✅")
        return uploaded_file, "csv"

    elif file_name.endswith(".xlsx") or file_name.endswith(".xls"):
        st.success("Excel file detected ✅")
        return uploaded_file, "excel"

    else:
        st.warning("Unknown or unsupported file type ❓")
        return None


def dataframe_converter():
    result = file_uploader()
    if result is None:
        return None

    file_address, file_type = result

    try:
        if file_type == "csv":
            df = pd.read_csv(file_address)

        elif file_type == "excel":
            df = pd.read_excel(file_address, engine="openpyxl")

        return df  # ✅ only return if successful

    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None  # ✅ prevents UnboundLocalError


def side_bar():
    with st.sidebar:

        st.title("Control Panel ⚙️")
        control_panel_option = option_menu(
            menu_title=None,
            options=["Visualization","Cleaning"],
            default_index=0,
            menu_icon='cast',
            icons=['clipboard2-data-fill','clipboard2-data-fill']
        )
        return control_panel_option

def select_chart(key):
    chart_selection = st.selectbox("Select Chart: ",["Select Chart","Bar","Line","Scatter Plot"],index=0,key=key)
    if chart_selection != "Select Chart":
        return chart_selection
    else: 
        return None
    
def group(data):
    col1,col2 = st.columns(2)
    with col1:
        group_col = st.selectbox("Select column to group BY:", ["Select"] + list(data.columns),key="group_data")
    with col2:
        value_col = st.selectbox("Select column to perform operation ON:", ["Select"] + list(data.columns),key="value_group")
    grouped_data = None
    if (group_col != "Select") and (value_col != "Select"):
        operation = st.selectbox("Select operation:", ["count", "sum", "mean", "max", "min"],key="group_Operatrion")
        if st.button("Group Data",key="group_button"):
            try:
                if operation == "count":
                    grouped_data = data.groupby(group_col)[value_col].count().reset_index()
                elif operation == "sum":
                    grouped_data = data.groupby(group_col)[value_col].sum().reset_index()
                elif operation == "mean":
                    grouped_data = data.groupby(group_col)[value_col].mean().reset_index()
                elif operation == "max":
                    grouped_data = data.groupby(group_col)[value_col].max().reset_index()
                elif operation == "min":
                    grouped_data = data.groupby(group_col)[value_col].min().reset_index()
            except Exception as e:
                st.error(e)
    return grouped_data,group_col,value_col


def select_columns(data_set):
    data_operation_choice = option_menu(menu_title=None,options=['Individual','Group'],default_index=0,orientation='horizontal')
    st.info(
    """
    ℹ️ **About Data Operation Modes**

    - **Individual:** Work with a single column at a time.  
      Choose any two columns (X and Y) to create visualizations or perform analysis on individual values.

    - **Merge:** Combine two or more columns into one.  
      Useful for creating new derived columns — for example, merging `First Name` and `Last Name`, or adding multiple numeric columns together.

    - **Group:** Group your data based on one or more columns.  
      Typically used for aggregation — for example, calculating the total sales per region or the average marks per student.

    Select an option above to choose how you want to handle your dataset.
    """
    )

    if data_operation_choice == "Individual":
        x_axis = st.selectbox("Select the X-Axis:",["Select"]+[col for col in data_set.columns],index=0,key="Select_Xcolumn")
        y_axis = st.selectbox("Select the Y-Axis:",["Select"]+[col for col in data_set.columns],index=0,key="Select_Ycolumn")
        if x_axis != "Select" and y_axis != "Select":
            return x_axis,y_axis,None,None,None
    elif data_operation_choice == "Group":
        grouped_data,group_col,value_col = group(data_set)
        return None,None,grouped_data,group_col,value_col
        
    return None,None,None,None,None

def graph_plotter(chart_type, data=None, x_axis=None, y_axis=None, grouped_data=None, group_col=None, value_col=None):
    try:
        # Case 1: Individual columns
        if data is not None and x_axis and y_axis:
            if chart_type == "Bar":
                st.bar_chart(data=data, x=x_axis, y=y_axis, use_container_width=True)
            elif chart_type == "Line":
                st.line_chart(data=data, x=x_axis, y=y_axis, use_container_width=True)
            elif chart_type == "Scatter Plot":
                st.scatter_chart(data=data, x=x_axis, y=y_axis, size=75, color="#60e3af")
            elif chart_type == "Horizontal Bar":
                pass
        # Case 2: Grouped columns
        elif grouped_data is not None and group_col and value_col:
            if chart_type == "Bar":
                st.bar_chart(data=grouped_data, x=group_col, y=value_col, use_container_width=True)
            elif chart_type == "Line":
                st.line_chart(data=grouped_data, x=group_col, y=value_col, use_container_width=True)
            elif chart_type == "Scatter Plot":
                st.scatter_chart(data=grouped_data, x=group_col, y=value_col, size=75, color="#60e3af")
    except Exception as e:
        st.error(f"Error while plotting chart: {e}")