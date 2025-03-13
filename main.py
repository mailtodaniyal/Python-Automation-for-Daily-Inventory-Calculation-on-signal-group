import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

def create_db():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS inventory (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT,
                        item TEXT,
                        quantity INTEGER)''')
    conn.commit()
    conn.close()

def insert_data(date, item, quantity):
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO inventory (date, item, quantity) VALUES (?, ?, ?)", (date, item, quantity))
    conn.commit()
    conn.close()

def fetch_data():
    conn = sqlite3.connect("inventory.db")
    df = pd.read_sql("SELECT * FROM inventory", conn)
    conn.close()
    return df

def delete_data(item):
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inventory WHERE item=?", (item,))
    conn.commit()
    conn.close()

def app():
    st.set_page_config(page_title="Daily Inventory Tracker", layout="wide")
    st.sidebar.title("Navigation")
    menu = st.sidebar.radio("Go to", ["Home", "Add Inventory", "View Inventory", "Delete Inventory"])
    
    if menu == "Home":
        st.title("📊 Daily Inventory Management")
        st.write("Use this app to track and manage inventory based on manual inputs.")
    
    elif menu == "Add Inventory":
        st.title("➕ Add Inventory")
        date = st.date_input("Select Date", datetime.today())
        item = st.text_input("Item Name")
        quantity = st.number_input("Quantity", min_value=0, step=1)
        
        if st.button("Submit"):
            if item and quantity > 0:
                insert_data(date, item, quantity)
                st.success("Inventory added successfully!")
            else:
                st.error("Please enter valid data!")
    
    elif menu == "View Inventory":
        st.title("📜 View Inventory")
        df = fetch_data()
        st.dataframe(df)
        
        if not df.empty:
            st.download_button("Download Data", df.to_csv(index=False), "inventory.csv", "text/csv")
    
    elif menu == "Delete Inventory":
        st.title("❌ Delete Inventory")
        df = fetch_data()
        items = df["item"].unique().tolist() if not df.empty else []
        
        if items:
            item_to_delete = st.selectbox("Select Item to Delete", items)
            if st.button("Delete"):
                delete_data(item_to_delete)
                st.success(f"{item_to_delete} removed from inventory!")
        else:
            st.write("No inventory data available to delete.")
    
if __name__ == "__main__":
    create_db()
    app()
