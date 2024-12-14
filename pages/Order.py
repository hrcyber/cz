import streamlit as st
import sqlite3
import pandas as pd

# Database setup
conn = sqlite3.connect("food_ordering_system.db")
c = conn.cursor()

# Create tables
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    food_item TEXT,
    price REAL,
    quantity INTEGER,
    total REAL,
    status TEXT,
    FOREIGN KEY(username) REFERENCES users(username)
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS food_items (
    item_name TEXT PRIMARY KEY,
    price REAL
)
''')
conn.commit()


# Helper functions
def register_user(username, password):
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def authenticate_user(username, password):
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    return c.fetchone()


def place_order(username, food_item, price, quantity):
    total = price * quantity
    c.execute("INSERT INTO orders (username, food_item, price, quantity, total, status) VALUES (?, ?, ?, ?, ?, ?)",
              (username, food_item, price, quantity, total, "Pending"))
    conn.commit()


def get_user_orders(username):
    c.execute("SELECT order_id, food_item, price, quantity, total, status FROM orders WHERE username=?", (username,))
    rows = c.fetchall()
    df = pd.DataFrame(rows, columns=["Order ID", "Food Item", "Price", "Quantity", "Total", "Status"])
    return df, df["Total"].sum()


def get_all_orders():
    c.execute("SELECT order_id, username, food_item, price, quantity, total, status FROM orders")
    rows = c.fetchall()
    df = pd.DataFrame(rows, columns=["Order ID", "Username", "Food Item", "Price", "Quantity", "Total", "Status"])
    return df


def update_order_status(order_id, new_status):
    c.execute("UPDATE orders SET status=? WHERE order_id=?", (new_status, order_id))
    conn.commit()


def delete_order(order_id):
    c.execute("DELETE FROM orders WHERE order_id=?", (order_id,))
    conn.commit()


def get_all_users():
    c.execute("SELECT username FROM users")
    rows = c.fetchall()
    return [row[0] for row in rows]


def delete_user(username):
    c.execute("DELETE FROM users WHERE username=?", (username,))
    conn.commit()


def get_food_items():
    c.execute("SELECT item_name, price FROM food_items")
    rows = c.fetchall()
    return pd.DataFrame(rows, columns=["Food Item", "Price"])


def add_food_item(item_name, price):
    try:
        c.execute("INSERT INTO food_items (item_name, price) VALUES (?, ?)", (item_name, price))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def update_food_item(item_name, new_price):
    c.execute("UPDATE food_items SET price=? WHERE item_name=?", (new_price, item_name))
    conn.commit()


# Main app
#st.markdown("<h1 style='color:red;'>Wellcome to Food Hut</h1>", unsafe_allow_html=True)
#st.title("Wellcome to Food Hut")

role = st.sidebar.radio("Select Role", ["Client", "Admin"])

if role == "Client":
    st.markdown("<h1 style='color:red;'>Wellcome to Food Hut</h1>", unsafe_allow_html=True)
    #st.header("Wellcome to Food Hut")

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
        st.session_state["username"] = None

    if not st.session_state["logged_in"]:
        st.subheader("Login or Register")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if authenticate_user(username, password):
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.success("Logged in successfully!")
            else:
                st.error("Invalid credentials.")

        if st.button("Register"):
            if register_user(username, password):
                st.success("Registered successfully! Please login.")
            else:
                st.error("Registration failed. Username may already exist.")
    else:
        st.subheader(f"Welcome, {st.session_state['username']}!")

        page = st.radio("Menu", ["Place Order", "View Orders", "Logout"])

        if page == "Place Order":
            st.header("Place an Order")
            food_menu = get_food_items()
            st.table(food_menu)
            food_item = st.selectbox("Select Food Item", food_menu["Food Item"])
            price = float(food_menu[food_menu["Food Item"] == food_item]["Price"].values[0])
            quantity = st.number_input("Quantity", min_value=1, value=1, step=1)
            total = price * quantity
            st.write(f"Price per item: ${price}")
            st.write(f"Total: ${total}")

            if st.button("Order Now"):
                place_order(st.session_state["username"], food_item, price, quantity)
                st.success("Order placed successfully!")

        elif page == "View Orders":
            st.header("Your Orders")
            orders, grand_total = get_user_orders(st.session_state["username"])
            st.table(orders)
            st.subheader(f"Grand Total: ${grand_total:.2f}")

        elif page == "Logout":
            st.session_state["logged_in"] = False
            st.session_state["username"] = None
            st.success("Logged out successfully!")
