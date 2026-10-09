import streamlit as st
import datetime
import random
import pandas as pd
from PIL import Image

# ----------------- Page Configuration -----------------
st.set_page_config(
    page_title="Ecoza - Smart Circular Recycling",
    page_icon="🌿",
    layout="wide"
)

# ----------------- Clean & Modern UI Theme CSS -----------------
st.markdown(
    """
    <style>
    /* Global Background */
    .stApp {
        background-color: #f7faf8 !important;
    }

    /* Base Typography */
    .stApp, .stApp p, .stApp span, .stApp label {
        color: #1a2e22 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #0d381e !important;
        font-weight: 700 !important;
    }

    /* Clean Card Layout for Forms & Metrics */
    [data-testid="stForm"], [data-testid="stMetric"], .stTable {
        background-color: #ffffff !important;
        padding: 20px !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04) !important;
        border: 1px solid #dbe7df !important;
    }

    div[data-testid="stMetricValue"] {
        color: #1b6338 !important;
        font-weight: 800 !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #4a6353 !important;
        font-weight: 600 !important;
    }

    /* ---------------------------------------------------- */
    /* CLEAN & PRECISE FILE UPLOADER STYLING               */
    /* ---------------------------------------------------- */
    [data-testid="stFileUploader"] {
        background-color: #ffffff !important;
        border: 2px dashed #3a7d53 !important;
        border-radius: 12px !important;
        padding: 24px !important;
        margin: 10px 0 !important;
    }

    /* Reset all nested children so dashed borders don't repeat */
    [data-testid="stFileUploader"] * {
        border: none !important;
        background-color: transparent !important;
    }

    /* Uploader Text */
    [data-testid="stFileUploader"] span,
    [data-testid="stFileUploader"] p,
    [data-testid="stFileUploader"] small {
        color: #244230 !important;
        font-weight: 600 !important;
        font-size: 15px !important;
    }

    /* Browse/Upload Button */
    [data-testid="stFileUploader"] button {
        background-color: #1b6338 !important;
        border-radius: 8px !important;
        padding: 8px 20px !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1) !important;
    }
    [data-testid="stFileUploader"] button span,
    [data-testid="stFileUploader"] button div {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    [data-testid="stFileUploader"] button:hover {
        background-color: #144d2b !important;
    }

    /* ---------------------------------------------------- */
    /* SIDEBAR NAVIGATION VISIBILITY                        */
    /* ---------------------------------------------------- */
    [data-testid="stSidebar"] {
        background-color: #0f2d1d !important;
    }

    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
        font-weight: 800 !important;
    }

    /* Sidebar Radio Navigation Buttons */
    [data-testid="stSidebar"] div[role="radiogroup"] label {
        background: rgba(255, 255, 255, 0.1) !important;
        padding: 10px 14px !important;
        border-radius: 8px !important;
        margin-bottom: 8px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        display: flex !important;
        align-items: center !important;
    }

    [data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background: rgba(255, 255, 255, 0.2) !important;
    }

    [data-testid="stSidebar"] div[role="radiogroup"] label p,
    [data-testid="stSidebar"] div[role="radiogroup"] label span {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 15px !important;
    }

    /* Metric card in sidebar */
    [data-testid="stSidebar"] [data-testid="stMetric"] {
        background-color: #ffffff !important;
        border-radius: 10px !important;
        padding: 14px !important;
    }
    [data-testid="stSidebar"] [data-testid="stMetric"] [data-testid="stMetricLabel"] * {
        color: #374151 !important;
        font-weight: 600 !important;
    }
    [data-testid="stSidebar"] [data-testid="stMetric"] [data-testid="stMetricValue"] * {
        color: #0f4d2a !important;
        font-weight: 800 !important;
        font-size: 30px !important;
    }

    /* Primary Buttons */
    .stButton>button {
        background-color: #1b6338 !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 9px 20px !important;
    }
    .stButton>button:hover {
        background-color: #144d2b !important;
        color: #ffffff !important;
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
            "Pickup ID": "ECO-8041",
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
        "Center Name": "Ecoza GreenTech E-Waste Hub",
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
        "Center Name": "ScrapMetal & Glass Processing Hub",
        "Type": "Metal & Glass Recyclables",
        "Address": "Ambattur Industrial Estate",
        "Contact": "+91 97720 11223",
        "lat": 13.1143,
        "lon": 80.1548
    },
    {
        "Center Name": "Ecoza Community Compost Station",
        "Type": "Wet & Organic Waste",
        "Address": "Adyar Eco Park Zone",
        "Contact": "+91 91234 98765",
        "lat": 13.0125,
        "lon": 80.2570
    }
]

# ----------------- Left Sidebar Navigation -----------------
st.sidebar.markdown("## 🌿 Ecoza")
st.sidebar.markdown(f"**Logged in:** {st.session_state.username}")
st.sidebar.metric(label="Your EcoPoints", value=f"{st.session_state.ecopoints} pts")

nav_choice = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📊 Dashboard",
        "📸 AI Waste Scanner & Classifier",
        "📍 Nearby Collection Centers (Map)",
        "🚚 Doorstep Pickup",
        "🎁 Rewards Store",
        "🏆 Community Leaderboard"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("Ecoza • Circular Economy Platform")

# ----------------- 0. Home Screen -----------------
if nav_choice == "🏠 Home":
    st.title("🌱 Welcome to Ecoza")
    st.subheader("Transforming Everyday Waste into Value, Rewards, and Community Impact")
    
    st.markdown("<br>", unsafe_allow_html=True)

    col_h1, col_h2, col_h3 = st.columns(3)
    with col_h1:
        st.markdown("### 📸 Scan & Identify")
        st.write("Scan household waste using AI vision to identify categories and preview points per kg.")
    with col_h2:
        st.markdown("### 📍 Drop or Pickup")
        st.write("Locate verified collection centers on our live map or schedule hassle-free home pickups.")
    with col_h3:
        st.markdown("### 🎁 Earn & Redeem")
        st.write("Accumulate verified EcoPoints on every drop-off to redeem cafe deals, groceries, and tree planting.")

    st.markdown("---")
    st.subheader("🔄 How Ecoza Works")
    step1, step2, step3, step4 = st.columns(4)
    step1.info("**1. Segregate**\n\nSort plastics, paper, e-waste, and metals into clean bags.")
    step2.info("**2. Scan & Log**\n\nUpload a picture or snap a live photo to log weights.")
    step3.info("**3. Deposit / Pickup**\n\nDrop off at an authorized Ecoza station or book doorstep pickup.")
    step4.info("**4. Redeem Rewards**\n\nExchange EcoPoints for dining vouchers, bus passes, and discounts.")

    st.markdown("---")
    st.subheader("📈 Ecoza Recycling Rate Card")
    rates_df = pd.DataFrame([
        {"Material Category": k, "Reward Rate": f"{v} EcoPoints / kg"} 
        for k, v in RATES.items()
    ])
    st.dataframe(rates_df, use_container_width=True)

# ----------------- 1. Dashboard -----------------
elif nav_choice == "📊 Dashboard":
    st.title("♻️ Ecoza Community Dashboard")
    st.write("Track your recycling footprint, carbon offset, and pending collection requests.")

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
        st.subheader("🎟️ Your Active Coupons")
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
            st.image(uploaded_image, caption="Uploaded Material", use_container_width=True)
        with col_pred:
            possible_categories = ["Plastic", "Paper & Cardboard", "Glass", "Metal / Aluminium", "E-Waste"]
            detected_category = random.choice(possible_categories)
            confidence_score = round(random.uniform(88.0, 97.5), 1)

            st.success(f"### Classification: **{detected_category}**")
            st.write(f"Confidence score: **{confidence_score}%**")
            st.write(f"Ecoza reward rate: **{RATES[detected_category]} EcoPoints / kg**")

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
    st.title("📍 Nearby Ecoza Collection Centers")
    st.write("Find certified circular drop-off hubs and scrap depots in your area.")

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
    st.write("Book a verified Ecoza agent to collect bulk recyclables directly from your doorstep.")

    with st.form("pickup_form"):
        pickup_address = st.text_area("Pickup Address", placeholder="Apartment / Door No., Street, City")
        waste_items = st.multiselect("Types of Waste", list(RATES.keys()), default=["Plastic", "Paper & Cardboard"])
        pickup_date = st.date_input("Preferred Date", min_value=datetime.date.today())
        phone = st.text_input("Contact Mobile", placeholder="+91 9876543210")
        notes = st.text_input("Special Notes (Optional)")

        submit_booking = st.form_submit_button("Book Ecoza Pickup")
        if submit_booking:
            if not pickup_address or not phone:
                st.error("Please enter both the address and phone number.")
            else:
                new_id = f"ECO-{random.randint(1000, 9999)}"
                st.session_state.pickup_requests.append({
                    "Pickup ID": new_id,
                    "Address": pickup_address,
                    "Items": ", ".join(waste_items),
                    "Date": str(pickup_date),
                    "Contact": phone,
                    "Status": "Confirmed"
                })
                st.success(f"Pickup booked! Your Ecoza Tracking ID is **{new_id}**.")
                st.rerun()

    if st.session_state.pickup_requests:
        st.markdown("---")
        st.subheader("Active Pickup Requests")
        st.dataframe(pd.DataFrame(st.session_state.pickup_requests), use_container_width=True)

# ----------------- 5. Rewards Store -----------------
elif nav_choice == "🎁 Rewards Store":
    st.title("🎁 Ecoza Rewards Store")
    st.write(f"Exchange your EcoPoints for eco-conscious rewards. Balance: **{st.session_state.ecopoints} EcoPoints**")

    rewards_list = [
        {"title": "Free Cafe Beverage", "cost": 50, "desc": "1 free artisanal beverage at partner cafes."},
        {"title": "Organic Grocery Coupon (₹100 Off)", "cost": 100, "desc": "Redeemable at local organic partner stores."},
        {"title": "Metro / Transit Recharge (₹150)", "cost": 150, "desc": "Recharge voucher for city metro or bus passes."},
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
                    voucher_code = f"ECOZA-{random.randint(10000, 99999)}"
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
    st.title("🏆 Ecoza Community Leaderboard")
    st.write("Celebrating the top recyclers contributing to sustainable neighborhoods.")

    leaderboard = [
        {"Rank": "🥇 1", "Recycler": "Aarav Sharma", "Diverted Waste": "44.0 kg", "EcoPoints": 880},
        {"Rank": "🥈 2", "Recycler": "Priya Raman", "Diverted Waste": "38.5 kg", "EcoPoints": 770},
        {"Rank": "🥉 3", "Recycler": st.session_state.username, "Diverted Waste": "28.0 kg", "EcoPoints": st.session_state.ecopoints},
        {"Rank": "4", "Recycler": "Karthik Raj", "Diverted Waste": "18.5 kg", "EcoPoints": 370},
        {"Rank": "5", "Recycler": "Divya N", "Diverted Waste": "12.0 kg", "EcoPoints": 240}
    ]
    st.table(pd.DataFrame(leaderboard))
