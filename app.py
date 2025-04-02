import streamlit as st
import pandas as pd
import os
import calendar
import bcrypt
from face_utils import register_face, recognize_face

USER_FILE = "data/users.csv"
ATTENDANCE_FILE = "data/attendance.csv"

st.title("📷 Student Attendance System")
st.sidebar.header("⚙️ Options")

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def load_users():
    if os.path.exists(USER_FILE):
        return pd.read_csv(USER_FILE)
    return pd.DataFrame(columns=["Username", "Role", "Password"])

def save_user(username, role, password):
    df = load_users()
    if username in df["Username"].values:
        st.error("Username already exists.")
        return
    new_user = pd.DataFrame([[username, role, hash_password(password)]], columns=["Username", "Role", "Password"])
    new_user.to_csv(USER_FILE, mode="a", header=not os.path.exists(USER_FILE), index=False)
    st.success("User registered successfully!")

def authenticate(username, password):
    df = load_users()
    user = df[df["Username"] == username]
    if not user.empty and check_password(password, user.iloc[0]["Password"]):
        return user.iloc[0]["Role"]
    return None

# Login Section
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
login_button = st.sidebar.button("Login")

if login_button:
    role = authenticate(username, password)
    if role:
        st.session_state["username"] = username
        st.session_state["role"] = role
        st.success(f"Logged in as {role}")
    else:
        st.error("Invalid credentials")

# Registration (Admin only)
if "role" in st.session_state and st.session_state["role"] == "Admin":
    st.sidebar.subheader("Register New User")
    new_username = st.sidebar.text_input("New Username")
    new_password = st.sidebar.text_input("New Password", type="password")
    role = st.sidebar.selectbox("Role", ["Student", "Staff"])
    if st.sidebar.button("Register"):
        save_user(new_username, role, new_password)

if "role" in st.session_state:
    role = st.session_state["role"]
    username = st.session_state["username"]
    
    if role == "Student":
        if st.button("Mark Attendance"):
            name = recognize_face()
            if name == username:
                st.success(f"Attendance marked for {name}")
                pd.DataFrame([[name, pd.Timestamp.now()]], columns=["Name", "Timestamp"]).to_csv(ATTENDANCE_FILE, mode="a", header=not os.path.exists(ATTENDANCE_FILE), index=False)
            else:
                st.error("Face not recognized")
    
    elif role == "Staff":
        st.subheader("Post Period Attendance")
        students = pd.read_csv(USER_FILE)["Username"].tolist()
        selected_student = st.selectbox("Select Student", students)
        period = st.selectbox("Select Period", list(range(1, 8)))
        if st.button("Mark Period Attendance"):
            pd.DataFrame([[selected_student, pd.Timestamp.now(), period]], columns=["Name", "Timestamp", "Period"]).to_csv(ATTENDANCE_FILE, mode="a", header=not os.path.exists(ATTENDANCE_FILE), index=False)
            st.success(f"Attendance marked for {selected_student} in Period {period}")

    st.subheader("📊 Attendance Records")
    if os.path.exists(ATTENDANCE_FILE):
        df = pd.read_csv(ATTENDANCE_FILE)
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
        st.dataframe(df)
    else:
        st.warning("No attendance records available.")
else:
    st.warning("Please log in to access the system.")
