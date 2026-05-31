# =========================== app.py ===========================
import streamlit as st
import pandas as pd

# ------------------------------
# Page Config
# ------------------------------
st.set_page_config(page_title="PathLab Compare", page_icon="🔬", layout="wide")

# ------------------------------
# Load Data
# ------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("lab_tests (1).csv")

    # Fix column names
    df.columns = df.columns.str.lower().str.replace(" ", "_")

    # Convert types
    df["price"] = df["price"].astype(int)
    df["home_collection_fee"] = df["home_collection_fee"].astype(int)

    # Total price
    df["total_price"] = df["price"] + df["home_collection_fee"]

    return df

df = load_data()

# ------------------------------
# Title
# ------------------------------
st.title("🔬 PathLab Test Price Comparison")
st.markdown("Find the **cheapest pathology lab** for your test!")

# ------------------------------
# Sidebar Filters
# ------------------------------
st.sidebar.header("Filters")

available_cities = ["All"] + sorted(df["city"].unique().tolist())
selected_city = st.sidebar.selectbox("Select City", available_cities)

# Price range
max_price = int(df["total_price"].max()) + 1
price_range = st.sidebar.slider(
    "Max Budget",
    0, max_price, (0, max_price), 10
)

# Sorting
sort_option = st.sidebar.selectbox(
    "Sort By",
    ["Low to High", "High to Low", "Lab Name"]
)

# ------------------------------
# Search (simple contains)
# ------------------------------
query = st.text_input("🔍 Search test (e.g., CBC, thyroid)")

filtered_df = df.copy()

# City filter
if selected_city != "All":
    filtered_df = filtered_df[filtered_df["city"] == selected_city]

# Price filter
filtered_df = filtered_df[
    (filtered_df["total_price"] >= price_range[0]) &
    (filtered_df["total_price"] <= price_range[1])
]

# Simple search (no fuzz)
if query:
    filtered_df = filtered_df[
        filtered_df["test_name"].str.contains(query, case=False)
    ]

# Sorting
if sort_option == "Low to High":
    filtered_df = filtered_df.sort_values(by="total_price")
elif sort_option == "High to Low":
    filtered_df = filtered_df.sort_values(by="total_price", ascending=False)
elif sort_option == "Lab Name":
    filtered_df = filtered_df.sort_values(by="lab_name")

# ------------------------------
# Display
# ------------------------------
if not filtered_df.empty:
    st.success(f"✅ Found {len(filtered_df)} results")

    for _, row in filtered_df.iterrows():
        st.markdown(f"### {row['test_name']}")
        st.write(f"Lab: {row['lab_name']} | City: {row['city']}")

        col1, col2, col3 = st.columns(3)
        col1.metric("Price", f"₹{row['price']}")
        col2.metric("Home Collection", f"₹{row['home_collection_fee']}")
        col3.metric("Total", f"₹{row['total_price']}")

        st.divider()
else:
    st.warning("No results found")

# Footer
st.caption("Built with ❤️ for Final Year Project")