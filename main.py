import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO


def generate_invoice_pdf(shop_details, bill_to, items):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    # Shop details
    c.setFont("Helvetica-Bold", 16)
    c.drawString(30, 750, shop_details["name"])
    c.setFont("Helvetica", 12)
    c.drawString(30, 735, f"Address: {shop_details['address']}")
    c.drawString(30, 720, f"GSTIN: {shop_details['gstin']}")
    c.drawString(30, 705, f"Contact: {shop_details['contact']}")

    # Bill to
    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, 680, "Bill To:")
    c.setFont("Helvetica", 12)
    c.drawString(30, 665, bill_to)

    # Table headers
    c.setFont("Helvetica-Bold", 12)
    headers = ["Item Name", "Qty", "Price", "HSN", "GST", "Amount"]
    x_positions = [30, 150, 200, 250, 300, 400]
    for i, header in enumerate(headers):
        c.drawString(x_positions[i], 640, header)

    # Table content
    c.setFont("Helvetica", 12)
    y_position = 625
    total_amount = 0
    for item in items:
        c.drawString(30, y_position, item["name"])
        c.drawString(150, y_position, str(item["qty"]))
        c.drawString(200, y_position, f"{item['price']:.2f}")
        c.drawString(250, y_position, item["hsn"])
        c.drawString(300, y_position, f"{item['gst']}%")
        amount = item["qty"] * item["price"] * (1 + item["gst"] / 100)
        total_amount += amount
        c.drawString(400, y_position, f"{amount:.2f}")
        y_position -= 15

    # Total
    c.setFont("Helvetica-Bold", 12)
    c.drawString(30, y_position - 15, f"Total: {total_amount:.2f}")

    c.save()
    buffer.seek(0)
    return buffer


# Streamlit app
st.title("Invoice Generator")

# Shop details
st.sidebar.header("Shop Details")
shop_name = st.sidebar.text_input("Shop Name", "My Shop")
shop_address = st.sidebar.text_area("Address", "123 Market Street")
shop_gstin = st.sidebar.text_input("GSTIN", "22AAAAA0000A1Z5")
shop_contact = st.sidebar.text_input("Contact", "9876543210")

# Bill to details
bill_to = st.text_input("Bill To", "Customer Name, Address")

# Items
st.subheader("Add Items")
item_name = st.text_input("Item Name")
item_qty = st.number_input("Quantity", min_value=1, value=1, step=1)
item_price = st.number_input("Price", min_value=0.0, value=0.0, step=0.1)
item_hsn = st.text_input("HSN Code", "1234")
item_gst = st.number_input("GST (%)", min_value=0.0, value=5.0, step=0.1)

# Initialize session state for items
if "items" not in st.session_state:
    st.session_state["items"] = []

# Add item to the list
if st.button("Add Item"):
    if item_name and item_hsn:
        st.session_state["items"].append({
            "name": item_name,
            "qty": item_qty,
            "price": item_price,
            "hsn": item_hsn,
            "gst": item_gst
        })
        st.success("Item added successfully!")
    else:
        st.error("Please fill in all required fields.")

# Clear items
if st.button("Clear Items"):
    st.session_state["items"] = []
    st.success("Items cleared!")

# Display added items
if st.session_state["items"]:
    st.write("### Items List")
    st.table(st.session_state["items"])

# Generate PDF
if st.button("Generate Invoice"):
    if shop_name and shop_address and shop_gstin and bill_to and st.session_state["items"]:
        shop_details = {
            "name": shop_name,
            "address": shop_address,
            "gstin": shop_gstin,
            "contact": shop_contact
        }

        pdf_buffer = generate_invoice_pdf(shop_details, bill_to, st.session_state["items"])

        st.download_button(
            label="Download Invoice as PDF",
            data=pdf_buffer,
            file_name="invoice.pdf",
            mime="application/pdf"
        )
    else:
        st.error("Please fill in all required details and add at least one item.")
