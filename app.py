import streamlit as st
import datetime

# Page configuration
st.set_page_config(
    page_title="Waste2Worth - Smart Waste Management",
    page_icon="♻️",
    layout="wide"
)

# Local storage initialization (Session State)
if "username" not in st.session_state:
    st.session_state.username = "Green Hero"
if "ecopoints" not in st.session_state:
    st.session_state.ecopoints = 150
if "waste_history" not in st.session_state:
    st.session_state.waste_history = [
        {"Item": "Plastic Bottles", "Weight": "2.0 kg", "EcoPoints": 40, "Date": "2026-10-05"},
        {"Item": "Cardboard Box", "Weight": "3.5 kg", "EcoPoints": 35, "Date": "2026-10-06"}
    ]
if "pickup_requests" not in st.session_state:
    st.session_state.pickup_requests = []

# EcoPoints calculation rate per kg
RATES = {
    "Plastic": 20,
    "Paper & Cardboard": 10,
    "Glass": 15,
    "Metal / Aluminium": 30,
    "E-Waste (Electronics)": 50,
    "Organic Waste": 5
}

# Sidebar Navigation
st.sidebar.title("♻️ Waste2Worth")
st.sidebar.caption("Smart Waste Management System")
menu = st.sidebar.radio(
    "Navigation Menu",
    ["🏠 Home", "📊 Dashboard", "📤 Upload & Recycle", "🚚 Request Pickup", "🏆 Leaderboard"]
)

# 1. HOME PAGE
if menu == "🏠 Home":
    st.title("🌱 Waste2Worth: Smart Waste Management System")
    st.subheader("Recycle household waste responsibly and earn valuable EcoPoints!")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("### 🔍 1. Identify\nCategorize and upload your recyclable waste.")
    with col2:
        st.success("### ♻️ 2. Recycle\nSchedule doorstep collection or locate drop-off points.")
    with col3:
        st.warning("### 🎁 3. Earn Rewards\nCollect EcoPoints for every kilogram recycled.")

    st.markdown("---")
    st.write(
        "Waste2Worth encourages responsible waste segregation, reduces landfill dumping, "
        "and rewards sustainable living habits."
    )

# 2. DASHBOARD PAGE
elif menu == "📊 Dashboard":
    st.title("📊 User Dashboard")
    st.write(f"Welcome back, **{st.session_state.username}**!")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Total EcoPoints", f"{st.session_state.ecopoints} pts", delta="+40 pts")
    m2.metric("Total Submissions", len(st.session_state.waste_history))
    m3.metric("Pickup Requests", len(st.session_state.pickup_requests))

    st.markdown("---")
    st.subheader("📜 Waste Submission History")
    if st.session_state.waste_history:
        st.table(st.session_state.waste_history)
    else:
        st.info("No activity logged yet! Start by uploading your waste.")

# 3. UPLOAD & RECYCLE PAGE
elif menu == "📤 Upload & Recycle":
    st.title("📤 Log Waste & Calculate Points")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        waste_type = st.selectbox("Select Waste Category:", list(RATES.keys()))
        weight = st.number_input("Estimated Weight (in kg):", min_value=0.5, max_value=100.0, value=1.0, step=0.5)
        uploaded_image = st.file_uploader("Upload Item Photo (Optional):", type=["jpg", "png", "jpeg"])
        
        if uploaded_image:
            st.image(uploaded_image, caption="Uploaded Waste Preview", width=250)

    with col2:
        st.subheader("Estimated EcoPoints")
        earned_points = int(weight * RATES[waste_type])
        st.markdown(f"## **+{earned_points} Points**")
        st.caption(f"Conversion Rate: {RATES[waste_type]} points / kg")
        
        if st.button("Submit & Claim Points", type="primary"):
            st.session_state.ecopoints += earned_points
            st.session_state.waste_history.append({
                "Item": waste_type,
                "Weight": f"{weight} kg",
                "EcoPoints": earned_points,
                "Date": str(datetime.date.today())
            })
            st.balloons()
            st.success(f"Added {earned_points} EcoPoints to your account balance!")

# 4. REQUEST PICKUP PAGE
elif menu == "🚚 Request Pickup":
    st.title("🚚 Schedule a Doorstep Collection")
    
    with st.form("pickup_form"):
        name = st.text_input("Full Name")
        phone = st.text_input("Contact Phone Number")
        address = st.text_area("Pickup Address")
        date = st.date_input("Preferred Pickup Date", min_value=datetime.date.today())
        
        submitted = st.form_submit_button("Submit Request")
        if submitted:
            if address and phone:
                st.session_state.pickup_requests.append({
                    "Name": name,
                    "Date": str(date),
                    "Address": address,
                    "Status": "Pending"
                })
                st.success("Your pickup request has been scheduled successfully!")
            else:
                st.error("Please provide both your phone number and pickup address.")

    if st.session_state.pickup_requests:
        st.subheader("Recent Pickup Bookings")
        st.dataframe(st.session_state.pickup_requests)

# 5. LEADERBOARD PAGE
elif menu == "🏆 Leaderboard":
    st.title("🏆 Community Eco Champions")
    st.write("Top recyclers contributing to sustainable waste management:")
    
    leaderboard_data = [
        {"Rank": "🥇 1", "User": "Priya S.", "EcoPoints": 1500, "Badge": "🌟 Green Hero"},
        {"Rank": "🥈 2", "User": "Karthik R.", "EcoPoints": 1200, "Badge": "♻️ Recycler Pro"},
        {"Rank": "🥉 3", "User": "Aravind M.", "EcoPoints": 950, "Badge": "🌱 Eco Warrior"},
        {"Rank": "4", "User": st.session_state.username, "EcoPoints": st.session_state.ecopoints, "Badge": "🔰 Rising Star"}
    ]
    st.table(leaderboard_data)
  python -m pip install streamlit 
python -m streamlit run app.py
