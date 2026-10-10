import streamlit as st
import datetime
import random
import pandas as pd
from PIL import Image

# ----------------- Page Configuration -----------------
st.set_page_config(
    page_title="Ecoza - Circular Eco Recycling",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ----------------- Vibrant Nature & Eco-Friendly Theme CSS -----------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Fredoka:wght@600;700&display=swap');

    /* Hide default sidebar */
    [data-testid="stSidebar"], section[data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* Fresh Botanical Eco Gradient Background */
    .stApp {
        background: radial-gradient(circle at 10% 10%, #ecfdf5 0%, #f0fdf4 40%, #e6f7ef 100%) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    .stApp p, .stApp span, .stApp label, .stApp div {
        color: #143522;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 15px;
    }

    h1, h2, h3, h4 {
        font-family: 'Fredoka', cursive, sans-serif !important;
        letter-spacing: 0.3px;
        color: #0f4a25 !important;
    }

    /* Ecoza Leaf Logo */
    .brand-logo {
        font-size: 32px;
        font-family: 'Fredoka', cursive, sans-serif;
        font-weight: 700;
        background: linear-gradient(135deg, #059669 0%, #10b981 50%, #047857 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Honeycomb Solar Gold Reward Badge */
    .badge-points {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: #ffffff !important;
        font-family: 'Fredoka', cursive;
        font-weight: 700;
        padding: 8px 20px;
        border-radius: 9999px;
        font-size: 16px;
        box-shadow: 0 4px 14px rgba(217, 119, 6, 0.3);
        border: 2px solid #fef3c7;
        display: inline-block;
    }

    /* Fresh Green Navigation Pill Bar */
    div[role="radiogroup"] {
        background: #ffffff;
        padding: 7px 12px;
        border-radius: 9999px;
        border: 2px solid #a7f3d0;
        box-shadow: 0 4px 18px rgba(16, 185, 129, 0.12);
        display: flex;
        justify-content: center;
        gap: 6px;
    }

    div[role="radiogroup"] label {
        padding: 6px 14px !important;
        border-radius: 9999px !important;
        font-weight: 700 !important;
        font-family: 'Fredoka', cursive !important;
        color: #065f46 !important;
        transition: all 0.2s ease;
    }

    div[role="radiogroup"] label:hover {
        background: #d1fae5 !important;
    }

    /* Frosted Eco White Containers */
    [data-testid="stForm"], [data-testid="stMetric"], .stTable {
        background: #ffffff !important;
        padding: 24px !important;
        border-radius: 20px !important;
        box-shadow: 0 8px 24px rgba(5, 150, 105, 0.08) !important;
        border: 2px solid #bbf7d0 !important;
    }

    /* High-contrast form text inputs */
    input, select, textarea, div[data-baseweb="input"], div[data-baseweb="base-input"] {
        background-color: #ffffff !important;
        color: #0f381f !important;
        border-color: #86efac !important;
        border-radius: 10px !important;
    }

    input::placeholder {
        color: #94a3b8 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #059669 !important;
        font-family: 'Fredoka', cursive !important;
        font-weight: 700 !important;
        font-size: 34px !important;
    }

    /* Vibrant Eco Action Buttons */
    .stButton>button, div[data-testid="stForm"] button {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%) !important;
        color: #ffffff !important;
        font-family: 'Fredoka', cursive !important;
        font-size: 17px !important;
        font-weight: 700 !important;
        border-radius: 16px !important;
        border: 2px solid #6ee7b7 !important;
        padding: 10px 24px !important;
        box-shadow: 0 4px 14px rgba(5, 150, 105, 0.25) !important;
        transition: transform 0.15s ease;
    }

    .stButton>button:hover, div[data-testid="stForm"] button:hover {
        transform: translateY(-2px);
        background: linear-gradient(135deg, #047857 0%, #059669 100%) !important;
        color: #ffffff !important;
    }

    /* Clean Crisp Uploader Area */
    [data-testid="stFileUploader"] {
        background: #ffffff !important;
        border: 2px dashed #059669 !important;
        border-radius: 18px !important;
        padding: 24px !important;
    }

    [data-testid="stFileUploader"] * {
        background-color: transparent !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------- Session State Initialization -----------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "user_identifier" not in st.session_state:
    st.session_state.user_identifier = ""

if "username" not in st.session_state:
    st.session_state.username = "Green Hero"

if "registered_users" not in st.session_state:
    st.session_state.registered_users = {
        "user@ecoza.com": {"password": "ecoza", "name": "Deepak Raja"},
        "9876543210": {"password": "ecoza", "name": "Deepak Raja"}
    }

PAGES = ["🏠 Home", "📸 AI Scanner", "🗺️ Drop-off Map", "🚚 Super Pickup", "🎁 Rewards Store", "🏆 Champions Leaderboard", "📊 Impact Dashboard"]

if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 Home"

if "ecopoints" not in st.session_state:
    st.session_state.ecopoints = 250

if "waste_history" not in st.session_state:
    st.session_state.waste_history = [
        {"Item": "🥤 Plastic Bottles", "Weight": "500 g", "EcoPoints": 10, "Date": "2026-10-05"},
        {"Item": "📦 Paper & Notebooks", "Weight": "1200 g", "EcoPoints": 12, "Date": "2026-10-06"}
    ]

if "pickup_requests" not in st.session_state:
    st.session_state.pickup_requests = [
        {
            "Pickup ID": "ECO-401",
            "Address": "Anna Nagar Green Avenue, Chennai",
            "Items": "Plastic, Paper",
            "Date": "2026-10-10",
            "Contact": "+91 9876543210",
            "Status": "On The Way 🚚"
        }
    ]

if "redeemed_coupons" not in st.session_state:
    st.session_state.redeemed_coupons = []

RATES = {
    "🥤 Plastic Bottles": 20,
    "📚 Paper & Notebooks": 10,
    "🍶 Glass Jars": 15,
    "🥫 Metal Cans": 30,
    "🔋 E-Waste & Batteries": 50,
    "🍎 Organic Waste": 5
}

RECYCLING_CENTERS = [
    {
        "Center Name": "⚡ Guindy Eco Battery & E-Waste Hub",
        "Type": "E-Waste & Electronics",
        "Address": "Guindy Industrial Estate",
        "Contact": "+91 94441 23456",
        "lat": 13.0067,
        "lon": 80.2030
    },
    {
        "Center Name": "📘 Anna Nagar Paper Depot",
        "Type": "Plastic, Paper & Cardboard",
        "Address": "Anna Nagar West",
        "Contact": "+91 98840 56789",
        "lat": 13.0850,
        "lon": 80.2101
    },
    {
        "Center Name": "⚙️ Ambattur Scrap & Metal Depot",
        "Type": "Metal & Glass Recyclables",
        "Address": "Ambattur Industrial Estate",
        "Contact": "+91 97720 11223",
        "lat": 13.1143,
        "lon": 80.1548
    },
    {
        "Center Name": "🌱 Adyar Eco Park Composting Hub",
        "Type": "Wet & Organic Waste",
        "Address": "Adyar Eco Park Zone",
        "Contact": "+91 91234 98765",
        "lat": 13.0125,
        "lon": 80.2570
    }
]

# ----------------- LOGIN GATEWAY -----------------
if not st.session_state.authenticated:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_l1, col_l2, col_l3 = st.columns([1.2, 2, 1.2])

    with col_l2:
        st.markdown(
            """
            <div style="text-align: center; margin-bottom: 20px;">
                <div style="font-size: 55px; margin-bottom: 5px;">🌱</div>
                <h1 style="color: #065f46; font-size: 38px; margin-bottom: 4px;">Welcome to Ecoza</h1>
                <p style="color: #4b6354; font-weight: 600;">Log in with your email or mobile number to continue.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        auth_tab1, auth_tab2 = st.tabs(["🔐 Log In", "📝 Create New Account"])

        with auth_tab1:
            with st.form("login_form"):
                login_id = st.text_input("User Email or Mobile Number", placeholder="name@example.com or 9876543210")
                login_password = st.text_input("Password", type="password", placeholder="••••••••")
                btn_login = st.form_submit_button("🚀 Enter Ecoza", use_container_width=True)

                if btn_login:
                    cleaned_id = login_id.strip()
                    if not cleaned_id or not login_password:
                        st.error("Please enter both your User Email/Mobile Number and password!")
                    elif cleaned_id in st.session_state.registered_users and st.session_state.registered_users[cleaned_id]["password"] == login_password:
                        st.session_state.authenticated = True
                        st.session_state.user_identifier = cleaned_id
                        st.session_state.username = st.session_state.registered_users[cleaned_id]["name"]
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("Incorrect details! (Demo: user@ecoza.com / pass: ecoza)")

        with auth_tab2:
            with st.form("signup_form"):
                new_name = st.text_input("Full Name", placeholder="Deepak Raja")
                new_id = st.text_input("User Email or Mobile Number", placeholder="name@example.com or 9876543210")
                new_password = st.text_input("Create Password", type="password", placeholder="••••••••")
                btn_signup = st.form_submit_button("⭐ Sign Up & Join Ecoza", use_container_width=True)

                if btn_signup:
                    cleaned_new_id = new_id.strip()
                    if not new_name or not cleaned_new_id or not new_password:
                        st.error("Please fill in all details!")
                    elif cleaned_new_id in st.session_state.registered_users:
                        st.warning("This User Email or Mobile Number is already registered! Please log in.")
                    else:
                        st.session_state.registered_users[cleaned_new_id] = {
                            "password": new_password,
                            "name": new_name
                        }
                        st.session_state.authenticated = True
                        st.session_state.user_identifier = cleaned_new_id
                        st.session_state.username = new_name
                        st.balloons()
                        st.success("Account created successfully! Welcome.")
                        st.rerun()

    st.stop()

# ----------------- AUTHENTICATED APPLICATION -----------------

head_col1, head_col2, head_col3 = st.columns([1.5, 4.3, 1.8], vertical_alignment="center")

with head_col1:
    st.markdown('<div class="brand-logo">🌱 Ecoza</div>', unsafe_allow_html=True)

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
    col_pts, col_out = st.columns([1.3, 0.9], vertical_alignment="center")
    with col_pts:
        st.markdown(f'<div class="badge-points">🌟 {st.session_state.ecopoints} pts</div>', unsafe_allow_html=True)
    with col_out:
        if st.button("🚪 Logout", key="logout_btn"):
            st.session_state.authenticated = False
            st.session_state.user_identifier = ""
            st.rerun()

st.caption(f"Logged in: **{st.session_state.username}** ({st.session_state.user_identifier})")
st.markdown("<hr style='margin-top: 2px; margin-bottom: 22px; border: 0; border-top: 2px dashed #a7f3d0;'>", unsafe_allow_html=True)

# ----------------- 1. Home / Hero Screen -----------------
if st.session_state.current_page == "🏠 Home":
    st.markdown(
        f"""
        <div style="text-align: center; max-width: 820px; margin: 0 auto; padding: 15px 0 20px 0;">
            <div style="background: #dcfce7; color: #15803d; font-weight: 800; font-family: 'Fredoka'; padding: 6px 18px; border-radius: 9999px; display: inline-block; font-size: 14px; margin-bottom: 12px; border: 2px solid #86efac;">
                🌍 CIRCULAR LIVING & REWARDS 🌿
            </div>
            <h1 style="font-size: 44px; color: #064e3b; line-height: 1.2; margin-bottom: 10px;">
                Turn Everyday Waste Into <span style="background: linear-gradient(135deg, #059669, #0284c7); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">EcoPoints!</span>
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    c_btn1, c_btn2, c_btn3 = st.columns([2.3, 1.4, 2.3])
    with c_btn2:
        if st.button("✨ Scan An Item Now!", use_container_width=True):
            st.session_state.current_page = "📸 AI Scanner"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
            <div style="background: #ffffff; padding: 22px; border-radius: 18px; border: 2px solid #bbf7d0; text-align: center; box-shadow: 0 4px 12px rgba(5, 150, 105, 0.05);">
                <div style="font-size: 40px; margin-bottom: 8px;">📷</div>
                <h3 style="color: #065f46; margin: 0 0 6px 0;">AI Waste Scanner</h3>
                <p style="color: #4b6354; font-size: 14px; margin: 0;">Upload or snap photos to identify materials and calculate points per 1,000 grams.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            """
            <div style="background: #ffffff; padding: 22px; border-radius: 18px; border: 2px solid #bbf7d0; text-align: center; box-shadow: 0 4px 12px rgba(5, 150, 105, 0.05);">
                <div style="font-size: 40px; margin-bottom: 8px;">🚚</div>
                <h3 style="color: #065f46; margin: 0 0 6px 0;">Doorstep Collection</h3>
                <p style="color: #4b6354; font-size: 14px; margin: 0;">Schedule doorstep pickups with certified recycling partners.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            """
            <div style="background: #ffffff; padding: 22px; border-radius: 18px; border: 2px solid #bbf7d0; text-align: center; box-shadow: 0 4px 12px rgba(5, 150, 105, 0.05);">
                <div style="font-size: 40px; margin-bottom: 8px;">🎁</div>
                <h3 style="color: #065f46; margin: 0 0 6px 0;">Community Rewards</h3>
                <p style="color: #4b6354; font-size: 14px; margin: 0;">Trade accumulated points for plant saplings, book coupons, and vouchers.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.subheader("🎯 4 Simple Steps to Recycle")
    step1, step2, step3, step4 = st.columns(4)
    step1.success("**Step 1: Sort**\n\nSeparate plastic bottles, paper, and metal cans into clean streams.")
    step2.info("**Step 2: Scan**\n\nSnap a picture and input weight in grams.")
    step3.warning("**Step 3: Drop/Pickup**\n\nDeposit at nearby centers or call our pickup van.")
    step4.error("**Step 4: Claim**\n\nRedeem coupons and track your leaderboard rank!")

# ----------------- 2. AI Scanner & Classifier -----------------
elif st.session_state.current_page == "📸 AI Scanner":
    st.title("📸 AI Waste Scanner & Classifier")
    st.write("Upload an image or take a photo to detect material category and log EcoPoints.")

    tab1, tab2 = st.tabs(["📁 Upload Item Photo", "📷 Snap With Camera"])
    uploaded_image = None

    with tab1:
        file_input = st.file_uploader("Choose a photo from your device", type=["jpg", "jpeg", "png"])
        if file_input:
            uploaded_image = Image.open(file_input)

    with tab2:
        cam_input = st.camera_input("Take a photo of the item")
        if cam_input:
            uploaded_image = Image.open(cam_input)

    detected_category = "🥤 Plastic Bottles"
    confidence_score = 96.5

    if uploaded_image:
        col_img, col_pred = st.columns([1, 2])
        with col_img:
            st.image(uploaded_image, caption="Analyzed Item", use_container_width=True)
        with col_pred:
            possible_categories = list(RATES.keys())
            detected_category = random.choice(possible_categories)
            confidence_score = round(random.uniform(92.0, 99.4), 1)

            st.balloons()
            st.success(f"### 🎉 Classified: **{detected_category}**")
            st.write(f"Confidence score: **{confidence_score}%**")
            st.write(f"Rate: **{RATES[detected_category]} EcoPoints per 1,000 grams**")

    st.markdown("---")
    st.subheader("⚖️ Enter Estimated Weight (in Grams)")

    with st.form("waste_log_form"):
        selected_category = st.selectbox(
            "Selected Material",
            list(RATES.keys()),
            index=list(RATES.keys()).index(detected_category) if detected_category in RATES else 0
        )
        
        input_grams = st.number_input(
            "Weight in Grams",
            min_value=10,
            max_value=25000,
            step=50,
            value=250
        )
        
        rate_per_kg = RATES[selected_category]
        calculated_points = max(1, int((input_grams / 1000.0) * rate_per_kg))
        
        st.info(f"🌟 You will earn: **{calculated_points} EcoPoints!**")

        submit_log = st.form_submit_button("🚀 Add To Score!")
        if submit_log:
            st.session_state.ecopoints += calculated_points
            st.session_state.waste_history.append({
                "Item": selected_category,
                "Weight": f"{input_grams} g",
                "EcoPoints": calculated_points,
                "Date": str(datetime.date.today())
            })
            st.success(f"Awesome! Added {calculated_points} EcoPoints to your balance!")
            st.rerun()

# ----------------- 3. Nearby Collection Centers (Map) -----------------
elif st.session_state.current_page == "🗺️ Drop-off Map":
    st.title("🗺️ Ecoza Drop-Off Centers")
    st.write("Find certified circular recycling drop-off centers across Chennai!")

    df_centers = pd.DataFrame(RECYCLING_CENTERS)
    st.map(df_centers[["lat", "lon"]], zoom=11)

    st.subheader("📍 Center Locations & Contacts")
    for _, row in df_centers.iterrows():
        with st.container():
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.markdown(f"#### {row['Center Name']}")
                st.write(f"**Accepts:** {row['Type']}")
                st.write(f"**Address:** {row['Address']}")
            with col_b:
                st.write(f"📞 `{row['Contact']}`")
                st.button("Visit Station", key=f"dir_{row['Center Name']}")
            st.divider()

# ----------------- 4. Doorstep Pickup -----------------
elif st.session_state.current_page == "🚚 Super Pickup":
    st.title("🚚 Schedule Doorstep Pickup")
    st.write("Book a verified Ecoza pickup partner directly to your address.")

    with st.form("pickup_form"):
        pickup_address = st.text_area("Address", placeholder="Door No, Street, Landmark, Chennai")
        waste_items = st.multiselect("What are you recycling?", list(RATES.keys()), default=["🥤 Plastic Bottles", "📚 Paper & Notebooks"])
        pickup_date = st.date_input("Preferred Date", min_value=datetime.date.today())
        phone = st.text_input("Contact Mobile Number", placeholder="+91 9876543210")

        submit_booking = st.form_submit_button("🚛 Confirm Pickup")
        if submit_booking:
            if not pickup_address or not phone:
                st.error("Please enter both the address and contact number!")
            else:
                new_id = f"ECO-{random.randint(100, 999)}"
                st.session_state.pickup_requests.append({
                    "Pickup ID": new_id,
                    "Address": pickup_address,
                    "Items": ", ".join(waste_items),
                    "Date": str(pickup_date),
                    "Contact": phone,
                    "Status": "Confirmed 🎉"
                })
                st.success(f"Pickup Booked! Tracking ID: **{new_id}**")
                st.rerun()

    if st.session_state.pickup_requests:
        st.markdown("---")
        st.subheader("📋 Scheduled Pickups")
        st.dataframe(pd.DataFrame(st.session_state.pickup_requests), use_container_width=True)

# ----------------- 5. Rewards Store -----------------
elif st.session_state.current_page == "🎁 Rewards Store":
    st.title("🎁 Rewards Store")
    st.write(f"Redeem points for eco-conscious rewards! Balance: **{st.session_state.ecopoints} EcoPoints**")

    rewards_list = [
        {"title": "🌱 Plant A Sapling With Your Tag", "cost": 150, "desc": "A fruit sapling planted with your name tag!"},
        {"title": "🍦 Organic Beverage / Treat Voucher", "cost": 80, "desc": "1 free artisanal beverage at participating kiosks."},
        {"title": "📚 Stationery Coupon (₹100 Off)", "cost": 100, "desc": "Redeemable at local school bookstores."},
        {"title": "🚌 Green Metro Day Explorer Pass", "cost": 120, "desc": "Free 1-day transit pass across the city metro line."}
    ]

    col_a, col_b = st.columns(2)
    for idx, reward in enumerate(rewards_list):
        card = col_a if idx % 2 == 0 else col_b
        with card:
            st.markdown(f"### {reward['title']}")
            st.write(reward["desc"])
            st.caption(f"Cost: **{reward['cost']} EcoPoints**")
            
            if st.button(f"Claim ({reward['cost']} pts)", key=f"rwd_{idx}"):
                if st.session_state.ecopoints >= reward["cost"]:
                    st.session_state.ecopoints -= reward["cost"]
                    voucher_code = f"PRIZE-{random.randint(10000, 99999)}"
                    st.session_state.redeemed_coupons.append({
                        "Reward": reward["title"],
                        "Coupon Code": voucher_code,
                        "Date": str(datetime.date.today())
                    })
                    st.snow()
                    st.success(f"🎉 Redeemed! Your Code: **{voucher_code}**")
                    st.rerun()
                else:
                    st.error("Not enough EcoPoints yet!")
            st.divider()

# ----------------- 6. Champions Leaderboard -----------------
elif st.session_state.current_page == "🏆 Champions Leaderboard":
    st.title("🏆 Community Leaderboard")
    st.write("Top recyclers contributing to zero waste this week!")

    leaderboard = [
        {"Rank": "🥇 1st Place", "Contributor": "Class 8B (Little Flower School)", "Waste Saved": "44,000 g", "EcoPoints": 880},
        {"Rank": "🥈 2nd Place", "Contributor": "Priya R.", "Waste Saved": "38,500 g", "EcoPoints": 770},
        {"Rank": "🥉 3rd Place", "Contributor": f"{st.session_state.username} (You!)", "Waste Saved": "28,000 g", "EcoPoints": st.session_state.ecopoints},
        {"Rank": "4th Place", "Contributor": "Karthik Raj", "Waste Saved": "18,500 g", "EcoPoints": 370},
        {"Rank": "5th Place", "Contributor": "Green Community Club", "Waste Saved": "12,000 g", "EcoPoints": 240}
    ]
    st.table(pd.DataFrame(leaderboard))

# ----------------- 7. User Dashboard -----------------
elif st.session_state.current_page == "📊 Impact Dashboard":
    st.title("📊 Environmental Impact Dashboard")
    st.write("Track your total diverted waste and carbon savings!")

    total_dropoffs = len(st.session_state.waste_history)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Available Points", f"{st.session_state.ecopoints} pts")
    col2.metric("Total Drop-offs", total_dropoffs)
    col3.metric("Pickups Called", len(st.session_state.pickup_requests))
    col4.metric("CO₂ Offset (Est.)", f"{total_dropoffs * 2.2:.1f} kg")

    st.markdown("---")
    st.subheader("📜 Recycling History")
    if st.session_state.waste_history:
        st.dataframe(pd.DataFrame(st.session_state.waste_history), use_container_width=True)

    if st.session_state.redeemed_coupons:
        st.subheader("🎟️ Claimed Coupons")
        st.dataframe(pd.DataFrame(st.session_state.redeemed_coupons), use_container_width=True)
