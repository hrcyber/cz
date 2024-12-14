import streamlit as st
import sqlite3
import pandas as pd

# Database connection
conn = sqlite3.connect("food_ordering_system.db")
c = conn.cursor()

# Ensure food_items table exists
c.execute('''
CREATE TABLE IF NOT EXISTS food_items (
    item_name TEXT PRIMARY KEY,
    price REAL
)
''')
conn.commit()


# Helper functions
def add_food_item(item_name, price):
    try:
        c.execute("INSERT INTO food_items (item_name, price) VALUES (?, ?)", (item_name, price))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def delete_food_item(item_name):
    c.execute("DELETE FROM food_items WHERE item_name=?", (item_name,))
    conn.commit()


def update_food_item(item_name, new_price):
    c.execute("UPDATE food_items SET price=? WHERE item_name=?", (new_price, item_name))
    conn.commit()


def search_food_items(search_query):
    c.execute("SELECT * FROM food_items WHERE item_name LIKE ?", (f"%{search_query}%",))
    rows = c.fetchall()
    return pd.DataFrame(rows, columns=["Food Item", "Price"])


def get_all_food_items():
    c.execute("SELECT * FROM food_items")
    rows = c.fetchall()
    return pd.DataFrame(rows, columns=["Food Item", "Price"])


# Streamlit app
st.markdown("<h1 style='color:red;'>MANAGE FOOD ITEMS</h1>", unsafe_allow_html=True)
#st.title("MAGE FOOD ITEMS")

operation = st.sidebar.radio("Food Operation", ["Add", "Delete", "Update", "Search"])

if operation == "Add":
    st.markdown("<h2 style='color:gold;'>Add New Food Item</h2>", unsafe_allow_html=True)
    #st.header("Add New Food Item")
    item_name = st.text_input("Food Item Name")
    price = st.number_input("Price", min_value=0.0, step=0.01)

    if st.button("Add Food Item"):
        if add_food_item(item_name, price):
            st.success("Food item added successfully!")
        else:
            st.error("Failed to add food item. It might already exist.")

elif operation == "Delete":
    st.header("Delete a Food Item")
    food_items = get_all_food_items()
    if not food_items.empty:
        st.table(food_items)
        item_name = st.text_input("Food Item Name to delete")

        if st.button("Delete Food Item"):
            delete_food_item(item_name)
            st.success("Food item deleted successfully!")
    else:
        st.write("No food items available.")

elif operation == "Update":
    st.header("Update a Food Item")
    food_items = get_all_food_items()
    if not food_items.empty:
        st.table(food_items)
        item_name = st.text_input("Food Item Name to update")
        new_price = st.number_input("New Price", min_value=0.0, step=0.01)

        if st.button("Update Food Item"):
            update_food_item(item_name, new_price)
            st.success("Food item updated successfully!")
    else:
        st.write("No food items available.")

elif operation == "Search":
    st.header("Search Food Items")
    search_query = st.text_input("Enter search query (Food Item Name)")
    if search_query:
        search_results = search_food_items(search_query)
        if not search_results.empty:
            st.table(search_results)
        else:
            st.write("No matching food items found.")
    else:
        all_items = get_all_food_items()
        if not all_items.empty:
            st.table(all_items)
        else:
            st.write("No food items available.")
##################################################################################################################################

import streamlit as st
import sqlite3
import pandas as pd

# Database connection
conn = sqlite3.connect("food_ordering_system.db")
c = conn.cursor()

# Ensure orders table exists
c.execute('''
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    food_item TEXT,
    price REAL,
    quantity INTEGER,
    total REAL,
    status TEXT
)
''')
conn.commit()


# Helper functions
def delete_order(order_id):
    c.execute("DELETE FROM orders WHERE order_id=?", (order_id,))
    conn.commit()


def update_order_status(order_id, status):
    c.execute("UPDATE orders SET status=? WHERE order_id=?", (status, order_id))
    conn.commit()


def search_orders(search_query):
    c.execute("""
        SELECT * FROM orders 
        WHERE username LIKE ? OR food_item LIKE ? OR status LIKE ? OR CAST(order_id AS TEXT) LIKE ?
    """,
              (f"%{search_query}%", f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"))
    rows = c.fetchall()
    return pd.DataFrame(rows, columns=["Order ID", "Username", "Food Item", "Price", "Quantity", "Total", "Status"])


def get_all_orders():
    c.execute("SELECT * FROM orders")
    rows = c.fetchall()
    return pd.DataFrame(rows, columns=["Order ID", "Username", "Food Item", "Price", "Quantity", "Total", "Status"])


# Streamlit app
st.markdown("<h1 style='color:blue;'>MANAGE ORDERS</h1>", unsafe_allow_html=True)
#st.title("MANAGE ORDERS")

operation = st.sidebar.radio("Order Operation", ["Delete", "Update Status", "Search"])

if operation == "Delete":
    st.markdown("<h2 style='color:gold;'>Delete an Order</h2>", unsafe_allow_html=True)
    #st.header("Delete an Order")
    orders = get_all_orders()
    if not orders.empty:
        st.table(orders)
        order_id = st.number_input("Order ID to delete", min_value=1, step=1)

        if st.button("Delete Order"):
            delete_order(order_id)
            st.success("Order deleted successfully!")
    else:
        st.write("No orders available.")

elif operation == "Update Status":
    st.header("Update Order Status")
    orders = get_all_orders()
    if not orders.empty:
        st.table(orders)
        order_id = st.number_input("Order ID to update status", min_value=1, step=1)
        status = st.selectbox("Updated Status", ["Pending", "In Progress", "Completed","canceled","In 2hours","Not Available","Closed"])

        if st.button("Update Status"):
            update_order_status(order_id, status)
            st.success("Order status updated successfully!")
    else:
        st.write("No orders available.")

elif operation == "Search":
    st.header("Search Orders")
    search_query = st.text_input("Enter search query (Order ID, Username, Food Item, Status)")
    if search_query:
        search_results = search_orders(search_query)
        if not search_results.empty:
            st.table(search_results)
        else:
            st.write("No matching orders found.")
    else:
        all_orders = get_all_orders()
        if not all_orders.empty:
            st.table(all_orders)
        else:
            st.write("No orders available.")
#########################################################################################################################3


# Database connection
conn = sqlite3.connect("food_ordering_system.db")
c = conn.cursor()

# Ensure users table exists with username and password
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    username TEXT,
    password TEXT
)
''')
conn.commit()


# Helper functions
def delete_user(username, password):
    c.execute("DELETE FROM users WHERE username=? AND password=?", (username, password))
    conn.commit()


def search_users(search_query):
    c.execute("""
        SELECT * FROM users 
        WHERE username LIKE ? OR password LIKE ?
    """,
              (f"%{search_query}%", f"%{search_query}%"))
    rows = c.fetchall()
    return pd.DataFrame(rows, columns=["Username", "Password"])


def get_all_users():
    c.execute("SELECT * FROM users")
    rows = c.fetchall()
    return pd.DataFrame(rows, columns=["Username", "Password"])


# Streamlit app
st.markdown("<h1 style='color:blue;'>MANAGE USERS</h1>", unsafe_allow_html=True)
#st.title("MANAGE USERS")

operation = st.sidebar.radio("User Operation", ["Delete", "Search"])

if operation == "Delete":
    st.markdown("<h2 style='color:gold;'>Delete a User</h2>", unsafe_allow_html=True)
    #st.header("Delete a User")
    users = get_all_users()
    if not users.empty:
        st.table(users)
        username = st.text_input("Username to delete")
        password = st.text_input("Password to delete", type="password")

        if st.button("Delete User"):
            delete_user(username, password)
            st.success("User deleted successfully!")
    else:
        st.write("No users available.")

elif operation == "Search":
    st.header("Search Users")
    search_query = st.text_input("Enter search query (Username or Password)")
    if search_query:
        search_results = search_users(search_query)
        if not search_results.empty:
            st.table(search_results)
        else:
            st.write("No matching users found.")
    else:
        all_users = get_all_users()
        if not all_users.empty:
            st.table(all_users)
        else:
            st.write("No users available.")
