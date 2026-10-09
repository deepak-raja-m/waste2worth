import streamlit as st
import datetime
import random
import pandas as pd
from PIL import Image

# ----------------- Page Configuration -----------------
st.set_page_config(
    page_title="Ecoza - Smart Waste Solutions",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ----------------- Vibrant High-End Theme & Glassmorphism CSS -----------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* Hide default sidebar */
    [data-testid="stSidebar"], section[data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* Global Background with Soft Mesh Gradient Glow */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(16, 185, 129, 0.08) 0%, transparent 40%),
                    radial-gradient(circle at 90% 80%, rgba(6, 182, 212, 0.08) 0%, transparent 40%),
                    #f8fafc !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    .stApp p, .stApp span, .stApp label, .stApp div {
        color: #1e293b;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Gradient Brand Logo */
    .brand-logo {
        font-size: 28px;
        font-weight: 800;
        background: linear-gradient(135deg, #059669 0%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: flex;
        align-items: center;
        gap: 8px;
        letter-spacing: -0.5px;
    }

    /* Floating Pill Badge */
    .badge-points {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        color: #ffffff !important;
        font-weight: 700;
        padding: 9px 20px;
        border-radius: 9999px;
        font-size: 14px;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.3);
    }

    /* Top Radio Navbar Container */
    div[role="radiogroup"] {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(12px);
        padding: 6px 10px;
        border-radius: 9999px;
        border: 1px solid rgba(226, 232, 240, 0.8);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
        display: flex;
        justify-content: center;
        gap: 8px;
    }

    div[role="radiogroup"] label {
        padding: 6px 14px !important;
        border-radius: 9999px !important;
        transition: all 0.2s ease;
    }

    div[role="radiogroup"] label:hover {
        background: rgba(241, 245, 249, 0.8) !important;
    }

    /* Frosted Glass Cards & Containers */
    [data-testid="stForm"], [data-testid="stMetric"], .stTable {
        background: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(16px) !important;
        padding: 24px !important;
        border-radius: 18px !important;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.04) !important;
        border: 1px solid rgba(226, 232, 240, 0.9) !important;
    }

    /* Metric Values Accent */
    div[data-testid="stMetricValue"] {
        background: linear-gradient(135deg, #059669 0%, #0284c7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
    }

    /* Sleek Input Fields */
    input, select, textarea, div[data-baseweb="select"], div[data-baseweb="input"] {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 10px !important;
    }

    /* Gradient Buttons */
    .stButton>button, div[data-testid="stForm"] button {
        background: linear-gradient(135deg, #059669 0%, #0d9488 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 10px 24px !important;
        box-shadow: 0 4px 14px rgba(13, 148, 136, 0.25) !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    
    .stButton>button:hover, div[data-testid="stForm"] button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(13, 148, 136, 0.35) !important;
        color: #ffffff !important;
    }

    /* File Uploader Container */
    [data-testid="stFileUploader"] {
        background: #ffffff !important;
        border: 2px dashed #10b981 !important;
        border-radius: 16px !important;
        padding: 28px !important;
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.05);
    }

    [data-testid="stFileUploader"] * {
        background-color: transparent !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------- Session State Initialization -----------------
PAGES = ["Home", "AI Scanner", "Drop-off Map", "Doorstep Pickup", "Rewards Store", "Leaderboard", "Dashboard"]

if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

if "username" not in st.session_state:
    st.session_state.username = "Green Hero"

if "ecopoints" not in st.session_state:
    st.session_state.ecopoints = 150

if "waste_history" not in st.session_state:
    st.session_state.waste_history = [
        {"Item": "Plastic Bottles", "Weight": "500 g", "EcoPoints": 10, "Date": "2026-10-05"},
        {"Item": "Cardboard Box", "Weight": "1200 g", "EcoPoints": 12, "Date": "2026-10-06"}
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

RATES = {
    "Plastic": 20,
    "Paper & Cardboard": 10,
    "Glass": 15,
    "Metal / Aluminium": 30,
    "E-Waste": 50,
    "Organic Waste": 5
}

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

# ----------------- Top Header / Modern Navbar -----------------
head_col1, head_col2, head_col3 = st.columns([1.5, 4.5, 1.5], vertical_alignment="center")

with head_col1:
    st.markdown('<div class="brand-logo">🌿 Ecoza</div>', unsafe_allow_html=True)

with head_col2:
    current_index = PAGES.index(st.session_state.current_page) if st.session_state.current_page in PAGES else 0
    selected = st.radio(
        "Navigation Bar",
        PAGES,
        index=current_index,
        horizontal=True,
        label_visibility="collapsed"
    )
    if selected != st.session_state.current_page:
        st.session_state.current_page = selected

with head_col3:
    st.markdown(f'<div class="badge-points">✨ {st.session_state.ecopoints} EcoPoints</div>', unsafe_allow_html=True)

st.markdown("<hr style='margin-top: 4px; margin-bottom: 24px; border: 0; border-top: 1px solid rgba(226, 232, 240, 0.6);'>", unsafe_allow_html=True)

# ----------------- 1. Home / Hero Screen -----------------
if st.session_state.current_page == "Home":
    st.markdown(
        """
        <div style="text-align: center; max-width: 820px; margin: 0 auto; padding: 25px 0 20px 0;">
            <span style="background: rgba(16, 185, 129, 0.1); color: #059669; font-weight: 700; padding: 6px 16px; border-radius: 9999px; font-size: 13px; text-transform: uppercase; letter-spacing: 0.8px;">
                🌱 Circular Living Made Effortless
            </span>
            <h1 style="font-size: 48px; font-weight: 800; color: #0f172a; line-height: 1.15; margin-top: 16px; margin-bottom: 12px; letter-spacing: -1px;">
                Join the movement for smarter <span style="background: linear-gradient(135deg, #059669, #06b6d4); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">waste solutions</span>
            </h1>
            <p style="font-size: 18px; color: #64748b; margin-bottom: 24px; font-weight: 500;">
                Discover the power of responsible waste management and circular recycling right at your fingertips.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    c_btn1, c_btn2, c_btn3 = st.columns([2.5, 1.2, 2.5])
    with c_btn2:
        if st.button("🚀 Get started today", use_container_width=True):
            st.session_state.current_page = "AI Scanner"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
            <div style="background: #ffffff; padding: 24px; border-radius: 16px; border: 1px solid #e2e8f0; box-shadow: 0 4px 16px rgba(0,0,0,0.02);">
                <div style="font-size: 28px; margin-bottom: 10px;">📸</div>
                <h3 style="margin: 0 0 8px 0; color: #0f172a;">Scan & Classify</h3>
                <p style="color: #64748b; font-size: 14px; margin: 0;">Instant AI computer vision to detect material categories and reward point rates per gram.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            """
            <div style="background: #ffffff; padding: 24px; border-radius: 16px; border: 1px solid #e2e8f0; box-shadow: 0 4px 16px rgba(0,0,0,0.02);">
                <div style="font-size: 28px; margin-bottom: 10px;">📍</div>
                <h3 style="margin: 0 0 8px 0; color: #0f172a;">Drop or Pickup</h3>
                <p style="color: #64748b; font-size: 14px; margin: 0;">Locate verified collection centers on our interactive map or schedule door-to-door pickups.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            """
            <div style="background: #ffffff; padding: 24px; border-radius: 16px; border: 1px solid #e2e8f0; box-shadow: 0 4px 16px rgba(0,0,0,0.02);">
                <div style="font-size: 28px; margin-bottom: 10px;">🎁</div>
                <h3 style="margin: 0 0 8px 0; color: #0f172a;">Earn & Redeem</h3>
                <p style="color: #64748b; font-size: 14px; margin: 0;">Convert saved EcoPoints into merchant vouchers, bus discounts, and tree plantations.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.subheader("🔄 How It Works")
    step1, step2, step3, step4 = st.columns(4)
    step1.info("**1. Segregate**\n\nSort plastics, paper, e-waste, and metals into clean streams.")
    step2.info("**2. Scan & Log**\n\nUpload an image or use your camera to log estimated weight in grams.")
    step3.info("**3. Deposit / Pickup**\n\nDrop off at an authorized center or book doorstep collection.")
    step4.info("**4. Enjoy Perks**\n\nTurn EcoPoints into coffee coupons, grocery vouchers, or saplings.")

# ----------------- 2. AI Scanner & Classifier -----------------
elif st.session_state.current_page == "AI Scanner":
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
            st.write(f"Ecoza reward rate: **{RATES[detected_category]} EcoPoints / 1000g**")

    st.markdown("---")
    st.subheader("Confirm Weight & Claim EcoPoints")

    with st.form("waste_log_form"):
        selected_category = st.selectbox(
            "Confirmed Waste Category",
            list(RATES.keys()),
            index=list(RATES.keys()).index(detected_category) if detected_category in RATES else 0
        )
        
        input_grams = st.number_input(
            "Estimated Weight (in grams)",
            min_value=10,
            max_value=50000,
            step=50,
            value=250
        )
        
        rate_per_kg = RATES[selected_category]
        calculated_points = max(1, int((input_grams / 1000.0) * rate_per_kg))
        
        st.info(f"Points to earn: **{calculated_points} EcoPoints** (Rate: {rate_per_kg} pts per 1000g)")

        submit_log = st.form_submit_button("Confirm & Add EcoPoints")
        if submit_log:
            st.session_state.ecopoints += calculated_points
            st.session_state.waste_history.append({
                "Item": selected_category,
                "Weight": f"{input_grams} g",
                "EcoPoints": calculated_points,
                "Date": str(datetime.date.today())
            })
            st.success(f"Logged {input_grams} g of {selected_category}! You earned **{calculated_points} EcoPoints**.")
            st.rerun()

# ----------------- 3. Nearby Collection Centers (Map) -----------------
elif st.session_state.current_page == "Drop-off Map":
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
elif st.session_state.current_page == "Doorstep Pickup":
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
elif st.session_state.current_page == "Rewards Store":
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
elif st.session_state.current_page == "Leaderboard":
    st.title("🏆 Ecoza Community Leaderboard")
    st.write("Celebrating the top recyclers contributing to sustainable neighborhoods.")

    leaderboard = [
        {"Rank": "🥇 1", "Recycler": "Aarav Sharma", "Diverted Waste": "44,000 g", "EcoPoints": 880},
        {"Rank": "🥈 2", "Recycler": "Priya Raman", "Diverted Waste": "38,500 g", "EcoPoints": 770},
        {"Rank": "🥉 3", "Recycler": st.session_state.username, "Diverted Waste": "28,000 g", "EcoPoints": st.session_state.ecopoints},
        {"Rank": "4", "Recycler": "Karthik Raj", "Diverted Waste": "18,500 g", "EcoPoints": 370},
        {"Rank": "5", "Recycler": "Divya N", "Diverted Waste": "12,000 g", "EcoPoints": 240}
    ]
    st.table(pd.DataFrame(leaderboard))

# ----------------- 7. User Dashboard -----------------
elif st.session_state.current_page == "Dashboard":
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
