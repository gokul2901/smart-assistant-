import streamlit as st
import pandas as pd
import datetime
import os
from dotenv import load_dotenv
from src.utils.db_helper import load_products_df, save_products_df, reindex_chromadb

# Page Config
st.set_page_config(
    page_title="Admin Inventory Dashboard",
    page_icon="🔒",
    layout="wide"
)

# Load env variables
load_dotenv()
ADMIN_USER = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASS = os.getenv("ADMIN_PASSWORD", "admin123")

# Custom Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main-title {
        font-weight: 700;
        font-size: 2.5rem;
        color: #1e293b;
        margin-bottom: 0.5rem;
    }
    
    .stats-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        border: 1px solid #e2e8f0;
        text-align: center;
    }
    
    .stats-num {
        font-size: 2.25rem;
        font-weight: 700;
        color: #4f46e5;
    }
    
    .stats-label {
        font-size: 0.875rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Session State for Authentication
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# Login Flow
if not st.session_state.admin_logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h2 style='text-align: center; color: #4f46e5; font-weight: 700; margin-top: 5rem;'>Store Admin Portal</h2>", unsafe_allow_html=True)
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter admin username")
            password = st.text_input("Password", type="password", placeholder="Enter admin password")
            submit = st.form_submit_button("Sign In", use_container_width=True)
            
            if submit:
                if username == ADMIN_USER and password == ADMIN_PASS:
                    st.session_state.admin_logged_in = True
                    st.success("Login Successful!")
                    time_placeholder = st.empty()
                    time_placeholder.info("Redirecting...")
                    st.rerun()
                else:
                    st.error("Invalid Username or Password")
else:
    # Header area
    header_col1, header_col2 = st.columns([8, 2])
    with header_col1:
        st.markdown("<div class='main-title'>📦 Store Inventory Management</div>", unsafe_allow_html=True)
        st.markdown("<p style='color: #64748b; font-size: 1.1rem;'>Add, update, or delete products and automatically re-index search systems.</p>", unsafe_allow_html=True)
    with header_col2:
        st.write("")
        st.write("")
        if st.button("🔒 Sign Out", use_container_width=True):
            st.session_state.admin_logged_in = False
            st.rerun()
            
    # Load current CSV data
    try:
        df = load_products_df()
    except Exception as e:
        st.error(f"Failed to load inventory: {e}")
        st.stop()

    # Admin Dashboard Summary Cards
    st.markdown("### Inventory Stats")
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    with stat_col1:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-num">{len(df)}</div>
            <div class="stats-label">Total Products</div>
        </div>
        """, unsafe_allow_html=True)
    with stat_col2:
        categories_count = df['Category'].nunique() if 'Category' in df.columns else 0
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-num">{categories_count}</div>
            <div class="stats-label">Categories</div>
        </div>
        """, unsafe_allow_html=True)
    with stat_col3:
        # Stock Quantity < 10
        low_stock = len(df[df['Stock Quantity'] < 10]) if 'Stock Quantity' in df.columns else 0
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-num" style="color: {'#ef4444' if low_stock > 0 else '#10b981'};">{low_stock}</div>
            <div class="stats-label">Low Stock Items</div>
        </div>
        """, unsafe_allow_html=True)
    with stat_col4:
        total_items = int(df['Stock Quantity'].sum()) if 'Stock Quantity' in df.columns else 0
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-num">{total_items}</div>
            <div class="stats-label">Total Stock Count</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Core Tabs
    tab_view, tab_add, tab_update, tab_delete = st.tabs([
        "📋 View Stock", 
        "➕ Add Product", 
        "✏️ Update Product", 
        "❌ Delete Product"
    ])

    # TAB 1: VIEW STOCK
    with tab_view:
        st.subheader("Inventory Stock List")
        
        # Filters
        filter_col1, filter_col2 = st.columns([4, 8])
        with filter_col1:
            categories = ["All"] + sorted(list(df['Category'].dropna().unique()))
            selected_cat = st.selectbox("Category Filter", categories)
        with filter_col2:
            search_query = st.text_input("Search Product Name", placeholder="Type name to filter...")
            
        filtered_df = df.copy()
        if selected_cat != "All":
            filtered_df = filtered_df[filtered_df['Category'] == selected_cat]
        if search_query:
            filtered_df = filtered_df[filtered_df['Name'].str.lower().str.contains(search_query.lower())]
            
        st.dataframe(filtered_df, use_container_width=True)

    # TAB 2: ADD PRODUCT
    with tab_add:
        st.subheader("Add New Product to Inventory")
        
        # Auto generate Product ID
        if not df.empty:
            # Try to parse numeric parts of ID e.g. P001 -> 1
            try:
                numeric_ids = df['Product ID'].str.replace('P', '').astype(int)
                next_id_num = numeric_ids.max() + 1
            except Exception:
                next_id_num = len(df) + 1
        else:
            next_id_num = 1
            
        suggested_id = f"P{next_id_num:03d}"
        
        with st.form("add_product_form"):
            col_left, col_right = st.columns(2)
            
            with col_left:
                pid = st.text_input("Product ID", value=suggested_id, help="Product identifier")
                name = st.text_input("Product Name", placeholder="e.g. Atta Premium")
                category = st.selectbox("Category", sorted(list(df['Category'].dropna().unique())), index=0)
                brand = st.text_input("Brand", placeholder="e.g. Aashirvaad")
                price = st.number_input("Price (RS)", min_value=0.0, value=100.0, step=1.0)
                expiry_dt = st.date_input("Expiry Date", value=datetime.date.today() + datetime.timedelta(days=365))
                
            with col_right:
                supplier = st.text_input("Supplier Name", placeholder="e.g. City Wholesale")
                supplier_ph = st.text_input("Supplier Phone No:", placeholder="e.g. 9876543210")
                supplier_email = st.text_input("Supplier Email:", placeholder="e.g. supplier@mail.com")
                stock_qty = st.number_input("Stock Quantity", min_value=0, value=100)
                block_name = st.selectbox("Block Name", ["A", "B", "C", "D", "E"], index=0)
                rack_no = st.number_input("Rack No", min_value=1, value=1, step=1)
                session = st.selectbox("Section (Session)", sorted(list(df['Session'].dropna().unique())), index=0)
                discount = st.number_input("Discount %", min_value=0, max_value=100, value=10)
                
            submit_add = st.form_submit_button("Add Product to Inventory", use_container_width=True)
            
            if submit_add:
                if not name.strip():
                    st.error("Product name cannot be empty!")
                elif pid in df['Product ID'].values:
                    st.error(f"Product ID {pid} already exists!")
                else:
                    # Format Expiry date to DD-MM-YYYY
                    formatted_expiry = expiry_dt.strftime("%d-%m-%Y")
                    
                    new_row = {
                        "Product ID": pid,
                        "Category": category,
                        "Name": name,
                        "Brand": brand,
                        "Price/RS": price,
                        "Expiry Date": formatted_expiry,
                        "Supplier": supplier,
                        "supplier ph No:": supplier_ph,
                        "supplier Email:": supplier_email,
                        "Stock Quantity": int(stock_qty),
                        "Block Name": block_name,
                        "Rack No": int(rack_no),
                        "Session": session,
                        "Discount%": discount
                    }
                    
                    # Add to df
                    new_df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                    save_products_df(new_df)
                    
                    # Re-index
                    with st.spinner("Re-indexing ChromaDB search vector space..."):
                        reindex_chromadb()
                        
                    st.success(f"Successfully added product: {name} ({pid}) and re-indexed store search.")
                    st.rerun()

    # TAB 3: UPDATE PRODUCT
    with tab_update:
        st.subheader("Modify Product Properties")
        
        # Product selector
        product_options = {f"{row['Product ID']} - {row['Name']}": row['Product ID'] for _, row in df.iterrows()}
        selected_key = st.selectbox("Select Product to Update", list(product_options.keys()))
        
        if selected_key:
            selected_pid = product_options[selected_key]
            prod_row = df[df['Product ID'] == selected_pid].iloc[0]
            
            # Parse existing expiry date
            try:
                existing_date = datetime.datetime.strptime(str(prod_row['Expiry Date']), "%d-%m-%Y").date()
            except Exception:
                existing_date = datetime.date.today()
                
            with st.form("update_product_form"):
                col_left, col_right = st.columns(2)
                
                with col_left:
                    st.text_input("Product ID (Disabled)", value=selected_pid, disabled=True)
                    up_name = st.text_input("Product Name", value=str(prod_row['Name']))
                    up_category = st.text_input("Category", value=str(prod_row['Category']))
                    up_brand = st.text_input("Brand", value=str(prod_row['Brand']))
                    up_price = st.number_input("Price (RS)", min_value=0.0, value=float(prod_row['Price/RS']), step=1.0)
                    up_expiry_dt = st.date_input("Expiry Date", value=existing_date)
                    
                with col_right:
                    up_supplier = st.text_input("Supplier Name", value=str(prod_row['Supplier']))
                    up_supplier_ph = st.text_input("Supplier Phone No:", value=str(prod_row['supplier ph No:']))
                    up_supplier_email = st.text_input("Supplier Email:", value=str(prod_row['supplier Email:']))
                    up_stock_qty = st.number_input("Stock Quantity", min_value=0, value=int(prod_row['Stock Quantity']))
                    up_block_name = st.text_input("Block Name", value=str(prod_row['Block Name']))
                    up_rack_no = st.number_input("Rack No", min_value=1, value=int(prod_row['Rack No']), step=1)
                    up_session = st.text_input("Section (Session)", value=str(prod_row['Session']))
                    up_discount = st.number_input("Discount %", min_value=0, max_value=100, value=int(prod_row['Discount%']))
                    
                submit_update = st.form_submit_button("Save Product Changes", use_container_width=True)
                
                if submit_update:
                    # Update row in DataFrame
                    df.loc[df['Product ID'] == selected_pid, 'Name'] = up_name
                    df.loc[df['Product ID'] == selected_pid, 'Category'] = up_category
                    df.loc[df['Product ID'] == selected_pid, 'Brand'] = up_brand
                    df.loc[df['Product ID'] == selected_pid, 'Price/RS'] = up_price
                    df.loc[df['Product ID'] == selected_pid, 'Expiry Date'] = up_expiry_dt.strftime("%d-%m-%Y")
                    df.loc[df['Product ID'] == selected_pid, 'Supplier'] = up_supplier
                    df.loc[df['Product ID'] == selected_pid, 'supplier ph No:'] = up_supplier_ph
                    df.loc[df['Product ID'] == selected_pid, 'supplier Email:'] = up_supplier_email
                    df.loc[df['Product ID'] == selected_pid, 'Stock Quantity'] = up_stock_qty
                    df.loc[df['Product ID'] == selected_pid, 'Block Name'] = up_block_name
                    df.loc[df['Product ID'] == selected_pid, 'Rack No'] = up_rack_no
                    df.loc[df['Product ID'] == selected_pid, 'Session'] = up_session
                    df.loc[df['Product ID'] == selected_pid, 'Discount%'] = up_discount
                    
                    save_products_df(df)
                    
                    with st.spinner("Re-indexing ChromaDB vector store..."):
                        reindex_chromadb()
                        
                    st.success(f"Successfully updated product: {up_name} ({selected_pid}) and re-indexed.")
                    st.rerun()

    # TAB 4: DELETE PRODUCT
    with tab_delete:
        st.subheader("Delete Product from Store Database")
        
        product_options = {f"{row['Product ID']} - {row['Name']}": row['Product ID'] for _, row in df.iterrows()}
        selected_del_key = st.selectbox("Select Product to Remove", list(product_options.keys()), key="del_selectbox")
        
        if selected_del_key:
            selected_del_pid = product_options[selected_del_key]
            del_prod_row = df[df['Product ID'] == selected_del_pid].iloc[0]
            
            st.warning(f"⚠️ Warning: Are you sure you want to permanently delete **{del_prod_row['Name']}** ({selected_del_pid})?")
            
            confirm_del = st.button("🔴 Confirm Delete", use_container_width=True)
            
            if confirm_del:
                # Filter out the deleted row
                new_df = df[df['Product ID'] != selected_del_pid]
                save_products_df(new_df)
                
                with st.spinner("Re-indexing ChromaDB vector store..."):
                    reindex_chromadb()
                    
                st.success(f"Successfully deleted product: {del_prod_row['Name']} ({selected_del_pid}) and re-indexed store.")
                st.rerun()