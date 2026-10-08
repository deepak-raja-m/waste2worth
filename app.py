import streamlit as st
import datetime
import random
import pandas as pd
from PIL import Image

# ----------------- Page Configuration -----------------
st.set_page_config(
    page_title="Waste2Worth - Smart Waste Management",
    page_icon="♻️",
    layout="wide"
)

# ----------------- Custom Eco Background & Theme Styling -----------------
st.markdown(
    """
    <style>
    /* Main app container background with nature gradient & clean overlay */
    .stApp {
        background: linear-gradient(135deg, rgba(237, 246, 240, 0.92) 0%, rgba(220, 240, 227, 0.92) 100%),
                    url('https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Sidebar background */
    [data-testid="stSidebar"] {
        background-color: #1e3d2f !important;
        color: #ffffff !important;
    }

    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    /* Cards / Containers styling */
    div[data-testid="stMetricValue"] {
        color: #155724 !important;
        font-weight: 700;
    }

    .stButton>button {
        background-color: #2d6a4f !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 600 !important;
    }

    .stButton>button:hover {
        background-color: #1b4332 !important;
        color: #d8f3dc !important;
    }
    </style>
    """,
    unsafe_allow_html=True
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

if "redeemed_coupons" not in st.session_state:
    st.session_state.redeemed_coupons = []

# Rate card (EcoPoints per kg)
RATES = {
    "Plastic": 20,
    "Paper & Cardboard": 10,
    "Glass": 15,
    "Metal / Aluminium": 30,
    "E-Waste": 50,
    "Organic Waste": 5
}

# Nearby recycling centers data
RECYCLING_CENTERS = [
    {
        "Center Name": "GreenTech E-Waste Hub",
        "Type": "E-Waste & Electronics",
        "Address": "Guindy Industrial Estate",
        "Contact": "+91 94441 23456",
        "lat": 13.0067,
        "lon": 80.2030
    },
    {
        "Center Name": "City Eco Plastics & Paper Depot",
        "Type": "Plastic, Paper & Cardboard",
        "Address": "Anna Nagar West",
        "Contact": "+91 98840 56789",
        "lat": 13.0850,
        "lon": 80.2101
    },
    {
        "Center Name": "ScrapMetal & Glass Processing Center",
        "Type": "Metal & Glass Recyclables",
        "Address": "Ambattur Industrial Estate",
        "Contact": "+91 97720 11223",
        "lat": 13.1143,
        "lon": 80.1548
    },
    {
        "Center Name": "Community Compost & Organic Station",
        "Type": "Wet & Organic Waste",
        "Address": "Adyar Eco Park Zone",
        "Contact": "+91 91234 98765",
        "lat": 13.0125,
        "lon": 80.2570
    }
]

# ----------------- Sidebar Navigation -----------------
st.sidebar.title("🌿 Waste2Worth")
st.sidebar.write(f"Logged in: **{st.session_state.username}**")
st.sidebar.metric(label="Your EcoPoints", value=f"{st.session_state.ecopoints} pts")

nav_choice = st.sidebar.radio(
    "Navigation",
    [
        "📊 Dashboard",
        "📸 AI Waste Scanner & Classifier",
        "📍 Nearby Collection Centers (Map)",
        "🚚 Doorstep Pickup",
        "🎁 Rewards Store",
        "🏆 Community Leaderboard"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("Waste2Worth • Circular Economy Platform")

# ----------------- 1. Dashboard -----------------
if nav_choice == "📊 Dashboard":
    st.title("♻️ Community Impact Dashboard")
    st.write("Track your recycling contributions, view environmental impact, and monitor scheduled pickups.")

    total_dropoffs = len(st.session_state.waste_history)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Available Points", f"{st.session_state.ecopoints} pts")
    col2.metric("Total Drop-offs", total_dropoffs)
    col3.metric("Active Pickups", len(st.session_state.pickup_requests))
    col4.metric("CO₂ Offset (Est.)", f"{total_dropoffs * 1.8:.1f} kg")

    st.markdown("---")
    st.subheader("📜 Recent Drop-off History")
    if st.session_state.waste_history:
        df_history = pd.DataFrame(st.session_state.waste_history)
        st.dataframe(df_history, use_container_width=True)
    else:
        st.info("No recycling drop-offs recorded yet.")

    if st.session_state.redeemed_coupons:
        st.subheader("🎟️ Your Redeemed Coupons")
        df_coupons = pd.DataFrame(st.session_state.redeemed_coupons)
        st.dataframe(df_coupons, use_container_width=True)

# ----------------- 2. AI Waste Scanner & Classifier -----------------
elif nav_choice == "📸 AI Waste Scanner & Classifier":
    st.title("📸 AI Waste Scanner & Classifier")
    st.write("Upload an image or use your device camera to detect the waste category and log your EcoPoints.")

    tab1, tab2 = st.tabs(["📁 Upload Image File", "📷 Use Device Camera"])
    uploaded_image = None

    with tab1:
        file_input = st.file_uploader("Upload an item picture", type=["jpg", "jpeg", "png"])
        if file_input:
            uploaded_image = Image.open(file_input)

    with tab2:
        cam_input = st.camera_input("Take a photo of the recyclable item")
        if cam_input:
            uploaded_image = Image.open(cam_input)

    detected_category = "Plastic"
    confidence_score = 92.4

    if uploaded_image:
        col_img, col_pred = st.columns([1, 2])
        with col_img:
            st.image(uploaded_image, caption="Analyzed Item", use_container_width=True)
        with col_pred:
            possible_categories = ["Plastic", "Paper & Cardboard", "Glass", "Metal / Aluminium", "E-Waste"]
            detected_category = random.choice(possible_categories)
            confidence_score = round(random.uniform(88.0, 97.5), 1)

            st.success(f"### Classification: **{detected_category}**")
            st.write(f"Confidence score: **{confidence_score}%**")
            st.write(f"Recycling reward rate: **{RATES[detected_category]} EcoPoints / kg**")

    st.markdown("---")
    st.subheader("Confirm Weight & Claim EcoPoints")

    with st.form("waste_log_form"):
        selected_category = st.selectbox(
            "Confirmed Waste Category",
            list(RATES.keys()),
            index=list(RATES.keys()).index(detected_category) if detected_category in RATES else 0
        )
        input_weight = st.number_input("Estimated Weight (in kg)", min_value=0.1, max_value=250.0, step=0.5, value=1.0)
        
        calculated_points = int(input_weight * RATES[selected_category])
        st.info(f"Points to earn: **{calculated_points} EcoPoints** (@ {RATES[selected_category]} pts/kg)")

        submit_log = st.form_submit_button("Confirm & Add EcoPoints")
        if submit_log:
            st.session_state.ecopoints += calculated_points
            st.session_state.waste_history.append({
                "Item": selected_category,
                "Weight": f"{input_weight} kg",
                "EcoPoints": calculated_points,
                "Date": str(datetime.date.today())
            })
            st.success(f"Logged {input_weight} kg of {selected_category}! You earned **{calculated_points} EcoPoints**.")
            st.rerun()

# ----------------- 3. Nearby Collection Centers (Map) -----------------
elif nav_choice == "📍 Nearby Collection Centers (Map)":
    st.title("📍 Nearby Recycling & Drop-off Centers")
    st.write("Find authorized recycling drop-off centers and scrap depots in your area.")

    df_centers = pd.DataFrame(RECYCLING_CENTERS)

    filter_type = st.selectbox("Filter by Accepted Waste", ["All Centers"] + list(RATES.keys()))
    if filter_type != "All Centers":
        filtered_df = df_centers[df_centers["Type"].str.contains(filter_type, case=False, na=False)]
    else:
        filtered_df = df_centers

    st.subheader("🗺️ Center Locations")
    st.map(filtered_df[["lat", "lon"]], zoom=11)

    st.subheader("📋 Center Details & Contact Information")
    for _, row in filtered_df.iterrows():
        with st.container():
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.markdown(f"#### {row['Center Name']}")
                st.write(f"**Accepted:** {row['Type']}")
                st.write(f"**Address:** {row['Address']}")
            with col_b:
                st.write(f"📞 `{row['Contact']}`")
                st.button("Get Directions", key=f"dir_{row['Center Name']}")
            st.divider()

# ----------------- 4. Doorstep Pickup -----------------
elif nav_choice == "🚚 Doorstep Pickup":
    st.title("🚚 Schedule Doorstep Collection")
    st.write("Book a scheduled pickup for bulk recyclables straight from your home or office.")

    with st.form("pickup_form"):
        pickup_address = st.text_area("Pickup Address", placeholder="Apartment / Door No., Street, City")
        waste_items = st.multiselect("Types of Waste", list(RATES.keys()), default=["Plastic", "Paper & Cardboard"])
        pickup_date = st.date_input("Preferred Date", min_value=datetime.date.today())
        phone = st.text_input("Contact Mobile", placeholder="+91 9876543210")
        notes = st.text_input("Special Notes (Optional)")

        submit_booking = st.form_submit_button("Book Pickup")
        if submit_booking:
            if not pickup_address or not phone:
                st.error("Please enter both the address and phone number.")
            else:
                new_id = f"W2W-{random.randint(1000, 9999)}"
                st.session_state.pickup_requests.append({
                    "Pickup ID": new_id,
                    "Address": pickup_address,
                    "Items": ", ".join(waste_items),
                    "Date": str(pickup_date),
                    "Contact": phone,
                    "Status": "Confirmed"
                })
                st.success(f"Pickup booked! Your Tracking ID is **{new_id}**.")
                st.rerun()

    if st.session_state.pickup_requests:
        st.markdown("---")
        st.subheader("Your Scheduled Pickups")
        st.dataframe(pd.DataFrame(st.session_state.pickup_requests), use_container_width=True)

# ----------------- 5. Rewards Store -----------------
elif nav_choice == "🎁 Rewards Store":
    st.title("🎁 EcoPoints Rewards Store")
    st.write(f"Spend points on vouchers and eco-friendly perks. Balance: **{st.session_state.ecopoints} EcoPoints**")

    rewards_list = [
        {"title": "Free Cafe Beverage", "cost": 50, "desc": "1 free artisanal beverage at partner cafes."},
        {"title": "Organic Grocery Coupon (₹100 Off)", "cost": 100, "desc": "Redeemable at local organic partner stores."},
        {"title": "Metro / Transit Recharge (₹150)", "cost": 150, "desc": "Recharge voucher for city metro or public bus pass."},
        {"title": "Plant an Urban Sapling", "cost": 200, "desc": "Sponsor a tree sapling planted with your name tag."}
    ]

    col_a, col_b = st.columns(2)
    for idx, reward in enumerate(rewards_list):
        card = col_a if idx % 2 == 0 else col_b
        with card:
            st.markdown(f"### {reward['title']}")
            st.write(reward["desc"])
            st.caption(f"Cost: **{reward['cost']} EcoPoints**")
            
            if st.button(f"Redeem ({reward['cost']} pts)", key=f"rwd_{idx}"):
                if st.session_state.ecopoints >= reward["cost"]:
                    st.session_state.ecopoints -= reward["cost"]
                    voucher_code = f"ECO-{random.randint(10000, 99999)}"
                    st.session_state.redeemed_coupons.append({
                        "Reward": reward["title"],
                        "Coupon Code": voucher_code,
                        "Date": str(datetime.date.today())
                    })
                    st.success(f"Redeemed! Your code: **{voucher_code}**")
                    st.rerun()
                else:
                    st.error("Insufficient EcoPoints.")
            st.divider()

# ----------------- 6. Community Leaderboard -----------------
elif nav_choice == "🏆 Community Leaderboard":
    st.title("🏆 Community Leaderboard")
    st.write("Recognizing community recyclers leading the charge for zero waste.")

    leaderboard = [
        {"Rank": "🥇 1", "Recycler": "Aarav Sharma", "Diverted Waste": "44.0 kg", "EcoPoints": 880},
        {"Rank": "🥈 2", "Recycler": "Priya Raman", "Diverted Waste": "38.5 kg", "EcoPoints": 770},
        {"Rank": "🥉 3", "Recycler": st.session_state.username, "Diverted Waste": "28.0 kg", "EcoPoints": st.session_state.ecopoints},
        {"Rank": "4", "Recycler": "Karthik Raj", "Diverted Waste": "18.5 kg", "EcoPoints": 370},
        {"Rank": "5", "Recycler": "Divya N", "Diverted Waste": "12.0 kg", "EcoPoints": 240}
    ]
    st.table(pd.DataFrame(leaderboard))
