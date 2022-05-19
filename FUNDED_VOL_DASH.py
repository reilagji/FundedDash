

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Funded Dashboard", page_icon=":bar_chart:", layout="wide")

@st.cache
def get_data():
    df = pd.read_csv('FUNDED_VOL_YTD.csv')

    df["FUNDED_DATE"] = pd.to_datetime(df["FUNDED_DATE"])
    df["YEAR"] = pd.DatetimeIndex(df["FUNDED_DATE"]).year
    df["MONTH"] = pd.DatetimeIndex(df["FUNDED_DATE"]).month
    return df

df = get_data()


# ---- SIDEBAR ------ #
st.sidebar.header("Filters:")

YEAR = st.sidebar.multiselect(
"Year Funded:",
options = df["YEAR"].unique(),
default = df["YEAR"].unique()
)
COUNTRY = st.sidebar.multiselect(
    "Select Country:",
    options=df["COUNTRY"].unique(),
    default=df["COUNTRY"].unique()
)

INDUSTRY = st.sidebar.multiselect(
"Industry:",
options = df["INDUSTRY"].unique(),
default = df["INDUSTRY"].unique()
)

ANNUAL_REVENUE = st.sidebar.multiselect(
"Customer Annual Revenue:",
options = df["ANNUAL_REVENUE"].unique(),
default = df["ANNUAL_REVENUE"].unique()
)

YEARS_IN_BUS = st.sidebar.multiselect(
"Select Years In Business:",
options = df["YEARS_IN_BUS"].unique(),
default = df["YEARS_IN_BUS"].unique()
)



df_selection = df.query(
    "COUNTRY == @COUNTRY & INDUSTRY == @INDUSTRY & ANNUAL_REVENUE == @ANNUAL_REVENUE & YEARS_IN_BUS == @YEARS_IN_BUS & YEAR == @YEAR"
)



# ----- MAINPAGE ----- #

st.title(":bar_chart: Funded Dashboard 2021 - 2022 YTD")
st.markdown("##")

# TOP KPIs

total_vol = int(df_selection["AMOUNT_FUNDED"].sum())
avg_vol = int(df_selection["AMOUNT_FUNDED"].mean())
series = df_selection["APP_NUMBER"]
series.count()
total_closed = series.count()

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Volume:")
    st.subheader(f"Agnostic $ {total_vol:,}")
with middle_column:
    st.subheader("Average Volume per App:")
    st.subheader(f"$ {avg_vol:,}")
with right_column:
    st.subheader("Total Apps Funded:")
    st.subheader(f"{total_closed:,}")

st.markdown("""---""")

#VISUALIZATIONS#


# COUNTRY SALES


# INDUSTRY SALES
sales_by_industry = (
    df_selection.groupby(by=["INDUSTRY"]).sum()[["AMOUNT_FUNDED"]].sort_values(by="AMOUNT_FUNDED")
)

fig_industry_sales = px.bar(
    sales_by_industry,
    x = "AMOUNT_FUNDED",
    y = sales_by_industry.index, orientation = "h",
    title = "<b>Funded Volume by Month</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_industry),
    template="plotly_white",
)
fig_industry_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# MONTHLY SALES
sales_by_month = (
    df_selection.groupby(by=["MONTH"]).sum()[["AMOUNT_FUNDED"]]
)

fig_monthly_sales = px.bar(
    sales_by_month,
    x=sales_by_month.index,
    y="AMOUNT_FUNDED",
    title="<b>Funded Volume by Month</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_month),
    template="plotly_white",
)
fig_monthly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

# COUNTRY SALES
sales_by_country = (
    df_selection.groupby(by=["COUNTRY"]).sum()[["AMOUNT_FUNDED"]].sort_values(by="AMOUNT_FUNDED")
)

fig_country_sales = px.bar(
    sales_by_country,
    x = "AMOUNT_FUNDED",
    y = sales_by_country.index, orientation = "h",
    title = "<b>Funded Volume by Geography</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_country),
    template="plotly_white",
)
fig_country_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

left_column, middle_column, right_column = st.columns(3)
left_column.plotly_chart(fig_monthly_sales, use_container_width=True)
middle_column.plotly_chart(fig_industry_sales, use_container_width=True)
right_column.plotly_chart(fig_country_sales, use_container_width=True)
