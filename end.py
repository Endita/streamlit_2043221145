import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import scipy.stats as stats

def write():
    st.title("Data Analysis")
    uploaded_file = st.file_uploader("Upload your data as a CSV file", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        data_raw = df.copy()
        st.dataframe(df.head())

        selected_columns = st.multiselect("Select columns for analysis", df.columns)

        if selected_columns:
            chart_options = ['Histogram', 'Line Chart', 'Bar Chart', 'Pie Chart']
            chart_type = st.selectbox("Select chart type", chart_options)

            df_selected = df[selected_columns].copy()
            df_selected.dropna(inplace=True)

            st.write("This is a dashboard showing the aggregated data by the selected columns.")

            for column in selected_columns:
                if df_selected[column].dtype == 'object':
                    if chart_type == 'Bar Chart':
                        st.write(f"Bar chart of total count by {column}:")
                        column_counts = df_selected[column].value_counts().reset_index()
                        column_counts.columns = [column, 'Count']
                        st.bar_chart(column_counts)

                    elif chart_type == 'Pie Chart':
                        st.write(f"Pie chart of total count by {column}:")
                        fig = px.pie(df_selected, names=column)
                        st.plotly_chart(fig)

                else:
                    if chart_type == 'Histogram':
                        st.write(f"Histogram of {column}:")
                        fig = px.histogram(df_selected, x=column)
                        data = df_selected[column].values
                        mean = np.mean(data)
                        std_dev = np.std(data)
                        x = np.linspace(mean - 3 * std_dev, mean + 3 * std_dev, 100)
                        y = np.abs(stats.norm.pdf(x, mean, std_dev) * len(data) * np.diff(fig.data[0].x)[0])

                        fig.add_trace(px.line(x=x, y=y).data[0])

                        st.plotly_chart(fig)

                    elif chart_type == 'Line Chart':
                        st.write(f"Line chart of {column}:")
                        st.plotly_chart(px.line(df_selected, x=df_selected.index, y=column))

                    elif chart_type == 'Bar Chart':
                        st.write(f"Bar chart of {column}:")
                        st.plotly_chart(px.bar(df_selected, x=df_selected.index, y=column))

write()
