import pandas as pd
import streamlit as st
from modules.visualization import *
from modules.cleaning import *
#------------------------ APP --------------------------------       
def run_app():
    side_bar_option = side_bar()
    # ---------- Title-------------
    st.title("Adaptive Data Explorer 🕹️")
    st.markdown("*Upload any dataset, apply filters, and visualize your data your way.*")
    st.markdown('<style>div.block-container{padding-top:50px;padding-left:105px;}</style>', unsafe_allow_html=True)
    #--------- Converter -----------
    data_frame = dataframe_converter()
    #-------------------------------
    if side_bar_option == "Visualization":
        if data_frame is not None:
            st.subheader("📊 Preview of Uploaded Data")
            st.dataframe(data_frame.head(),use_container_width=True)

            st.warning("⚠️ Tip: Clean your dataset for more accurate visualizations.")

            # Display Columns
            st.subheader("🧾 Columns", divider=True)
            st.markdown(" ".join([f"- `{col}`" for col in data_frame.columns]))

            # User Selections
            chart_selection = select_chart("chart_select")

            if chart_selection:
                x,y,grouped_data,group_col,value_col = select_columns(data_frame)
                if x is not None and y is not None:
                    graph_plotter(chart_selection,data_frame,x_axis=x,y_axis=y)
                elif grouped_data is not None and group_col is not None and value_col is not None:
                    graph_plotter(chart_selection, grouped_data=grouped_data, group_col=group_col, value_col=value_col)
            else:
                st.info("📊Select a chart.") 
        else:
            st.info("📂 Please upload a dataset to start exploring.")

    # ---------- Cleaning Section ----------
    elif side_bar_option == "Cleaning":
        if data_frame is not None:
            st.subheader("📊 Preview of Uploaded Data")
            st.dataframe(data_frame.head(),use_container_width=True)
            data_frame = clean_data(data_frame)
            if data_frame is not None:
                st.success("You can download the csv file now.")
                csv = data_frame.to_csv(index = False).encode('utf-8')
                st.download_button(
                    "📥 Download CSV",
                    file_name="cleaned_data.csv",
                    data = csv,
                    mime="txt/csv")
                
        else:
            st.info("📂 Please upload a dataset to clean.")