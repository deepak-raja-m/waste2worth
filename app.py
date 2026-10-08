import streamlit as st
import datetime
import pandas as pd

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
    "E-Waste": 50,
    "Organic Waste": 5
}

# Sidebar navigation
st.sidebar.title("🌿 Waste2Worth")
st.sidebar.write(f"Logged in as: **{st.session_state.username}**")
st.sidebar.metric(label="Your EcoPoints", value=st.session_state.ecopoints)

menu = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Log Recyclable Waste", "Schedule Pickup", "Redeem Rewards"]
)

# ----------------- Dashboard -----------------
if menu == "Dashboard":
    st.title("♻️ Welcome to Waste2Worth")
    st.write("Turn your everyday waste into valuable rewards while keeping your community clean!")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total EcoPoints", f"{st.session_state.ecopoints} pts")
    col2.metric("Total Deliveries", len(st.session_state.waste_history))
    col3.metric("Pending Pickups", len(st.session_state.pickup_requests))

    st.subheader("📜 Recent Recycling History")
    if st.session_state.waste_history:
        df_history = pd.DataFrame(st.session_state.waste_history)
        st.dataframe(df_history, use_container_width=True)
    else:
        st.info("No recycling activity recorded yet.")

# ----------------- Log Waste -----------------
elif menu == "Log Recyclable Waste":
    st.title("📦 Log Recyclable Waste")
    st.write("Log items you drop off at a collection facility to earn instant EcoPoints.")

    with st.form("log_waste_form"):
        category = st.selectbox("Waste Category", list(RATES.keys()))
        weight = st.number_input("Estimated Weight (in kg)", min_value=0.1, max_value=200.0, step=0.5, value=1.0)
        submitted = st.form_submit_button("Submit & Earn Points")

        if submitted:
            earned_points = int(weight * RATES[category])
            st.session_state.ecopoints += earned_points
            
            new_entry = {
                "Item": category,
                "Weight": f"{weight} kg",
                "EcoPoints": earned_points,
                "Date": str(datetime.date.today())
            }
            st.session_state.waste_history.append(new_entry)
            st.success(f"Successfully logged {weight} kg of {category}! You earned **{earned_points} EcoPoints**.")
            st.rerun()

# ----------------- Schedule Pickup -----------------
elif menu == "Schedule Pickup":
    st.title("🚚 Schedule a Doorstep Pickup")
    st.write("Have bulk recyclable items picked up straight from your doorstep.")

    with st.form("pickup_form"):
        address = st.text_area("Pickup Address", placeholder="Street name, Flat/House No., City")
        category = st.multiselect("Types of Waste", list(RATES.keys()), default=["Plastic"])
        pickup_date = st.date_input("Preferred Date", min_value=datetime.date.today())
        contact_number = st.text_input("Contact Number", placeholder="+91 9876543210")
        notes = st.text_input("Special instructions (optional)")

        request_submitted = st.form_submit_button("Confirm Pickup Request")

        if request_submitted:
            if not address or not contact_number:
                st.error("Please fill in both the address and contact number.")
            else:
                pickup_details = {
                    "Address": address,
                    "Items": ", ".join(category),
                    "Date": str(pickup_date),
                    "Contact": contact_number,
                    "Status": "Scheduled"
                }
                st.session_state.pickup_requests.append(pickup_details)
                st.success("Your pickup has been successfully scheduled! A partner will contact you.")

    if st.session_state.pickup_requests:
        st.subheader("Your Scheduled Pickups")
        st.dataframe(pd.DataFrame(st.session_state.pickup_requests), use_container_width=True)

# ----------------- Redeem Rewards -----------------
elif menu == "Redeem Rewards":
    st.title("🎁 Redeem EcoPoints")
    st.write(f"Available Balance: **{st.session_state.ecopoints} EcoPoints**")

    rewards = [
        {"Title": "Free Coffee Coupon", "Cost": 50, "Desc": "Get 1 complimentary coffee at partner cafes."},
        {"Title": "Grocery Voucher (₹100 Off)", "Cost": 100, "Desc": "Redeemable on local partner grocery stores."},
        {"Title": "Bus Pass Discount", "Cost": 150, "Desc": "Get 20% off your next public transport recharge."},
        {"Title": "Plant a Tree in Your Name", "Cost": 200, "Desc": "Sponsor an indigenous sapling planting."}
    ]

    col_a, col_b = st.columns(2)
    for i, reward in enumerate(rewards):
        target_col = col_a if i % 2 == 0 else col_b
        with target_col:
            st.markdown(f"### {reward['Title']}")
            st.write(reward["Desc"])
            st.caption(f"Cost: **{reward['Cost']} EcoPoints**")
            
            if st.button(f"Redeem for {reward['Cost']} pts", key=f"reward_{i}"):
                if st.session_state.ecopoints >= reward["Cost"]:
                    st.session_state.ecopoints -= reward["Cost"]
                    st.success(f"Redeemed '{reward['Title']}'! Voucher code sent to your notifications.")
                    st.rerun()
                else:
                    st.error("Insufficient EcoPoints balance.")
            st.divider()
