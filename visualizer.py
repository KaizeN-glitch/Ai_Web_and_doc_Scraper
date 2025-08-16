import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import re

def extract_table_from_text(text):
    # Try extracting markdown-style tables
    table_regex = r"((?:\|.*?\|\n)+)"
    match = re.search(table_regex, text)
    if match:
        try:
            table = pd.read_csv(io.StringIO(match.group(1)), sep='|', engine='python', skipinitialspace=True)
            table = table.loc[:, ~table.columns.str.contains('^Unnamed')]
            table.columns = [col.strip() for col in table.columns]

            # Clean the Percentage column
            if "Percentage" in table.columns:
                table["Percentage"] = table["Percentage"].str.extract(r"(\d+)%").astype(float)

            return table
        except Exception as e:
            st.error(f"Error parsing table: {e}")
    return None

def show_graphs(df):
    st.markdown("### 📊 Visualize the table")
    chart_type = st.selectbox("Choose chart type", ["Bar", "Line", "Pie"])

    try:
        if chart_type == "Bar":
            x_axis = st.selectbox("X-axis", df.columns)
            y_axis = st.selectbox("Y-axis", [col for col in df.columns if col != x_axis])

            fig, ax = plt.subplots(figsize=(8, 4))  # Smaller, fixed size
            sns.barplot(data=df, x=x_axis, y=y_axis, ax=ax, palette="Set2")
            ax.set_title(f"{y_axis} by {x_axis}")
            ax.set_xlabel(x_axis)
            ax.set_ylabel(y_axis)
            plt.tight_layout()
            st.pyplot(fig)

        elif chart_type == "Line":
            x_axis = st.selectbox("X-axis", df.columns)
            y_axis = st.selectbox("Y-axis", [col for col in df.columns if col != x_axis])

            fig, ax = plt.subplots(figsize=(8, 4))
            sns.lineplot(data=df, x=x_axis, y=y_axis, ax=ax, marker="o", color="purple")
            ax.set_title(f"{y_axis} over {x_axis}")
            ax.set_xlabel(x_axis)
            ax.set_ylabel(y_axis)
            plt.tight_layout()
            st.pyplot(fig)

        elif chart_type == "Pie":
            label_col = st.selectbox("Column for Labels", df.columns)
            value_col = st.selectbox("Column for Values", [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col]) and col != label_col])

            if value_col:
                pie_data = df.groupby(label_col)[value_col].sum()

                fig, ax = plt.subplots(figsize=(6, 6))  # Square = circle
                colors = sns.color_palette("pastel")[0:len(pie_data)]

                wedges, texts, autotexts = ax.pie(
                    pie_data,
                    labels=pie_data.index,
                    autopct="%1.1f%%",
                    startangle=140,
                    colors=colors,
                    textprops={"fontsize": 10}
                )

                ax.axis("equal")  # Circle
                ax.set_title(f"{value_col} distribution by {label_col}")
                st.pyplot(fig)
            else:
                st.warning("Please select a valid numeric column for pie chart values.")

    except Exception as e:
        st.error(f"Visualization error: {e}")
