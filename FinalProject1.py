import streamlit as st
import json
from pathlib import Path
import datetime
import uuid
import time

st.set_page_config(page_title="The Sunshine Bakery and Shop Website",
    page_icon = "",
    layout = "centered")
backgroundcolor = "#FFFF93"
st.markdown(
    f"""<style>.stApp {{background-color: {backgroundcolor};
    }}</style>""",unsafe_allow_html=True
)

with st.sidebar:
    st.title("Navigate")
    if st.button("Home"):
        st.session_state["page"] = "home"
    if st.button("Register"):
        st.session_state["page"] = "register"
    

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "user" not in st.session_state:
    st.session_state["user"] = None
    
if "page" not in st.session_state:
    st.session_state["page"] = "home"

if "owner_logged_in" not in st.session_state:
    st.session_state["owner_logged_in"] = False

if "employee_logged_in" not in st.session_state:
    st.session_state["employee_logged_in"] = False

users = [
{
"id": "1",
"email": "owner@school.edu",
"full_name": "System Owner",
"password": "123",
"role": "Owner"
},
{
"id": "2",
"email": "employee@school.edu",
"full_name": "System Employee",
"password": "1234",
"role": "Employee"
}
]


json_path = Path("users.json")
if json_path.exists():
    with open(json_path, "r") as f:
        users = json.load(f)
def save_users(users, path):
    with open(path, "w") as f:
        json.dump(users, f)

if st.session_state["page"]== "home":
    st.title("The Sunshine Bakery and Shop")
    st.divider()
    st.subheader("About Us")
    with st.container(border =True):
        st.markdown("The Sunshine Bakery Shop is a family owned and operated business. Our goal is to make sure every customer has a great start to their morning! Our prices are extremely affordable and very high quality, we specialize in signature coffee and pasteries.")
    st.divider()
    st.subheader("Administrative Log In Options")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Owner Log In"):
            st.session_state["page"] = "owner_login"
            st.rerun()
    with col2:
        if st.button("Employee Log In"):
            st.session_state["page"] = "employee_login"
            st.rerun()

elif st.session_state["page"] == "owner_login":
    st.title ("Owner Login Page")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    

    if st.button("Log In"):
        owner = next((user for user in users if user["email"] == email and user["password"]== password and user["role"]== "Owner"), None)
        if owner:
            st.session_state["owner_logged_in"]= True
            st.session_state["user"] = owner
            st.session_state["page"] = "owner_dashboard"
    
        
            st.rerun()


        else:
            st.error("Invalid Credentials!")

#Owner Dashboard
elif st.session_state["page"] == "owner_dashboard":
    st.title("Owner Dashboard")
    st.success("Welcome to the Owner Dashboard")
    tab1, tab2, tab3, tab4= st.tabs(["Add Product", "Update Prices", "Restock Invenotry", "Delete Product" ])
    with tab1:
        st.subheader("Add Product")
        st.text_input("Enter Product Name")
    
    with tab2:
        st.subheader("Update Prices")
    with tab3:
        st.subheader("Restock Inventory")
    with tab4:
        st.subheader("Delete Product")

elif st.session_state["page"] == "employee_login":
    st.title ("Employee Login Page")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Log In employee"):
        employee = next((user for user in users if user["email"] == email and user["password"]== password and user["role"]== "Employee"), None)
        if employee:
            st.session_state["employee_logged_in"]= True
            st.session_state["user"] = employee
            st.session_state["page"] = "employee_dashboard"
            st.rerun()


        else:
            st.error("Invalid Credentials!")

#Employee Dashboard
elif st.session_state["page"] == "employee_dashboard":
    st.success("Welcome to the Employee Dashboard")
    st.title("Employee Dashboard")
    tab1, tab2, tab3= st.tabs(["Current Catalog", "Daily Sales", "Invenotry" ])
    with tab1:
        st.subheader("Current Catolog")
        st.text_input("Select Product")
    with tab2:
        st.subheader("Daily Sales")
        st.text_input("Enter Sale")
    with tab3:
        st.subheader("Inventory")

    
    
  
    

    

elif st.session_state["page"] == "register":
    st.title("Register")
    Full_name = st.text_input("Full Name")
    email = st.text_input("Emial")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["Employee", "Owner"])
    if st.button("Create Account"):
        email_available = any(user["email"]== email for user in users)
        if not Full_name or not email or not password:
            st.warning("One or more fields missing!")
        elif email_available:
            st.error("Email already taken! ")
        else:
            new_user = {
                "id": 3,
                "email": email,
                "full_name": Full_name,
                "password": password,
                "role": role

            }
            users.append(new_user)
            save_users(users, json_path)
            st.success(" Account Created!")
            st.session_state["page"] = "home"
            st.rerun()
