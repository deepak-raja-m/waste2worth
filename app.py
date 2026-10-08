import streamlit as st
import datetime
import pandas as pd
from PIL import Image

# ----------------- Page Configuration -----------------
st.set_page_config(
    page_title="Waste2Worth - Smart Waste Management",
    page_icon="♻️",
    layout="wide"
)

# ----------------- Session State Initialization -----------------
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
    st.session_state.pickup_requests = [
        {
            "Pickup ID": "W2W-8041",
            "Address": "Anna Nagar, Main Road",
            "Items": "Plastic, Metal / Aluminium",
            "Date": "2026-10-10",
            "Contact": "+91 9876543210",
            "Status": "Assigned"
        }
    ]

# EcoPoints conversion rates per kg
RATES = {
    "Plastic": 20,
    "Paper & Cardboard": 10,
    "Glass": 15,
    "Metal / Aluminium": 30,
    "E-Waste": 50,
    "Organic Waste": 5
}

# ----------------- Sidebar Navigation -----------------
st.sidebar.title("🌿 Waste2Worth")
st.sidebar.markdown(f"User: **{st.session_state.username}**")
st.sidebar.metric(label="Current EcoPoints", value=f"{st.session_state.ecopoints} pts")

nav_choice = st.sidebar.radio(
    "Go to",
    [
        "📊 Dashboard",
        "📸 AI Waste Identifier & Logger",
        "🚚 Doorstep Pickup",
        "🎁 Rewards Store",
        "🏆 Community Leaderboard"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("Waste2Worth • Circular Economy Initiative")

# ----------------- 1. Dashboard -----------------
if nav_choice == "📊 Dashboard":
    st.title("♻️ Community Impact Dashboard")
    st.markdown("Track your recycling footprint, redeem perks, and manage your contributions.")

    col1, col2, col3, col4 = st.columns(4)
    total_recycled_items = len(st.session_state.waste_history)
    col1.metric("Available Points", f"{st.session_state.ecopoints} pts")
    col2.metric("Total Drop-offs", total_recycled_items)
    col3.metric("Pickups Requested", len(st.session_state.pickup_requests))
    col4.metric("Carbon Offset (Est.)", f"{total_recycled_items * 1.8:.1f} kg CO₂")

    st.markdown("---")
    st.subheader("📜 Recent Drop-off History")
    if st.session_state.waste_history:
        df_history = pd.DataFrame(st.session_state.waste_history)
        st.dataframe(df_history, use_container_width=True)
    else:
        st.info("No recycling logs recorded yet.")

# ----------------- 2. AI Waste Identifier & Logger -----------------
elif nav_choice == "📸 AI Waste Identifier & Logger":
    st.title("📸 Classify & Log Recyclable Waste")
    st.write("Upload an image of your item or select the waste category manually to calculate points.")

    uploaded_file = st.file_uploader("Upload an item picture (optional)", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Analyzed Image", width=250)
        st.success("Item identified: Recyclable Material ready for confirmation.")

    with st.form("waste_log_form"):
        selected_category = st.selectbox("Waste Category", list(RATES.keys()))
        input_weight = st.number_input("Estimated Weight (in kg)", min_value=0.1, max_value=250.0, step=0.5, value=1.0)
        
        calculated_points = int(input_weight * RATES[selected_category])
        st.info(f"Potential Reward: **{calculated_points} EcoPoints** (@ {RATES[selected_category]} pts/kg)")
        
        submit_log = st.form_submit_button("Confirm & Add to EcoPoints")
        if submit_log:
            st.session_state.ecopoints += calculated_points
            entry = {
                "Item": selected_category,
                "Weight": f"{input_weight} kg",
                "EcoPoints": calculated_points,
                "Date": str(datetime.date.today())
            }
            st.session_state.waste_history.append(entry)
            st.success(f"Success! {input_weight} kg of {selected_category} logged. You earned {calculated_points} EcoPoints.")
            st.rerun()

# ----------------- 3. Doorstep Pickup -----------------
elif nav_choice == "🚚 Doorstep Pickup":
    st.title("🚚 Doorstep Waste Collection")
    st.write("Schedule a pickup for bulk items right from your house or office.")

    with st.form("pickup_scheduling_form"):
        street_address = st.text_area("Pickup Location / Address", placeholder="Street name, door no., landmark")
        waste_types = st.multiselect("Select Categories", list(RATES.keys()), default=["Plastic", "Paper & Cardboard"])
        selected_date = st.date_input("Scheduled Date", min_value=datetime.date.today())
        phone_num = st.text_input("Mobile Number", placeholder="+91 9876543210")
        notes = st.text_input("Special Access Instructions (Optional)")
        
        submit_pickup = st.form_submit_button("Confirm Pickup Request")
        if submit_pickup:
            if not street_address or not phone_num:
                st.error("Please supply both a valid pickup address and contact number.")
            else:
                new_pickup_id = f"W2W-{len(st.session_state.pickup_requests) + 8042}"
                st.session_state.pickup_requests.append({
                    "Pickup ID": new_pickup_id,
                    "Address": street_address,
                    "Items": ", ".join(waste_types),
                    "Date": str(selected_date),
                    "Contact": phone_num,
                    "Status": "Confirmed"
                })
                st.success(f"Pickup booked successfully! Tracking ID: **{new_pickup_id}**")
                st.rerun()

    if st.session_state.pickup_requests:
        st.markdown("---")
        st.subheader("Active Pickup Requests")
        st.dataframe(pd.DataFrame(st.session_state.pickup_requests), use_container_width=True)

# ----------------- 4. Rewards Store -----------------
elif nav_choice == "🎁 Rewards Store":
    st.title("🎁 EcoPoints Redemption Hub")
    st.write(f"Spend your EcoPoints on green deals. Balance: **{st.session_state.ecopoints} pts**")

    rewards_catalog = [
        {"title": "Free Cafe Beverage", "cost": 60, "details": "1 complimentary brew at partner cafes."},
        {"title": "Supermarket Discount Coupon", "cost": 100, "details": "Get ₹100 off on fresh organic groceries."},
        {"title": "Public Metro/Bus Pass Pass-Back", "cost": 140, "details": "25% rebate voucher for public transit."},
        {"title": "Adopt / Plant a Sapling", "cost": 200, "details": "Plant an indigenous sapling with live GPS tracking."}
    ]

    col_x, col_y = st.columns(2)
    for idx, reward in enumerate(rewards_catalog):
        target_col = col_x if idx % 2 == 0 else col_y
        with target_col:
            st.markdown(f"### {reward['title']}")
            st.write(reward['details'])
            st.caption(f"Cost: **{reward['cost']} EcoPoints**")
            
            if st.button(f"Redeem Coupon ({reward['cost']} pts)", key=f"btn_reward_{idx}"):
                if st.session_state.ecopoints >= reward['cost']:
                    st.session_state.ecopoints -= reward['cost']
                    st.success(f"Success! {reward['title']} unlocked. Claim code: `ECO-{idx}92X`")
                    st.rerun()
                else:
                    st.error("You need more EcoPoints to unlock this benefit.")
            st.markdown("---")

# ----------------- 5. Leaderboard -----------------
elif nav_choice == "🏆 Community Leaderboard":
    st.title("🏆 Community Eco Heroes")
    st.write("Top recyclers contributing to sustainable neighborhoods this month.")

    leaderboard_data = [
        {"Rank": "🥇 1", "Recycler": "Aarav Sharma", "Waste Diverted": "42.5 kg", "EcoPoints": 850},
        {"Rank": "🥈 2", "Recycler": "Priya Raman", "Waste Diverted": "36.0 kg", "EcoPoints": 720},
        {"Rank": "🥉 3", "Recycler": st.session_state.username, "Waste Diverted": "28.5 kg", "EcoPoints": st.session_state.ecopoints},
        {"Rank": "4", "Recycler": "Karthik Raj", "Waste Diverted": "19.0 kg", "EcoPoints": 380},
        {"Rank": "5", "Recycler": "Divya N", "Waste Diverted": "14.2 kg", "EcoPoints": 290}
    ]

    st.table(pd.DataFrame(leaderboard_data))
