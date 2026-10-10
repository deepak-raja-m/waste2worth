import streamlit as st
import datetime
import random
import pandas as pd
from PIL import Image

# ----------------- Page Configuration -----------------
st.set_page_config(
    page_title="Ecoza - Super Recycling Adventure",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ----------------- Playful, High-Energy Palette for School Students -----------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600;700&family=Nunito:wght@700;800;900&display=swap');

    /* Hide default sidebar completely */
    [data-testid="stSidebar"], section[data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* Playful Sunshine & Mint Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #f0fdf4 0%, #ecfeff 50%, #fffbeb 100%) !important;
        font-family: 'Nunito', sans-serif !important;
    }
    
    .stApp p, .stApp span, .stApp label, .stApp div {
        color: #1e293b;
        font-family: 'Nunito', sans-serif;
        font-size: 16px;
    }

    h1, h2, h3, h4 {
        font-family: 'Fredoka', cursive, sans-serif !important;
        letter-spacing: 0.5px;
    }

    /* Chunky Logo */
    .brand-logo {
        font-size: 32px;
        font-family: 'Fredoka', cursive, sans-serif;
        font-weight: 700;
        background: linear-gradient(45deg, #10b981, #06b6d4, #f59e0b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Gamified Super Points Badge */
    .badge-points {
        background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);
        color: #78350f !important;
        font-family: 'Fredoka', cursive;
        font-weight: 700;
        padding: 8px 20px;
        border-radius: 9999px;
        font-size: 16px;
        box-shadow: 0 4px 14px rgba(245, 158, 11, 0.4);
        border: 2px solid #fef3c7;
        display: inline-block;
    }

    /* Pill-Style Navigation Radio */
    div[role="radiogroup"] {
        background: #ffffff;
        padding: 8px 12px;
        border-radius: 9999px;
        border: 2px solid #a7f3d0;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.12);
        display: flex;
        justify-content: center;
        gap: 6px;
    }

    div[role="radiogroup"] label {
        padding: 6px 14px !important;
        border-radius: 9999px !important;
        font-weight: 800 !important;
        font-family: 'Fredoka', cursive !important;
    }

    div[role="radiogroup"] label:hover {
        background: #e0f2fe !important;
    }

    /* Rounded Card Containers */
    [data-testid="stForm"], [data-testid="stMetric"], .stTable {
        background: #ffffff !important;
        padding: 24px !important;
        border-radius: 24px !important;
        box-shadow: 0 10px 25px rgba(16, 185, 129, 0.08) !important;
        border: 3px solid #d1fae5 !important;
    }

    /* High-contrast form text inputs */
    input, select, textarea, div[data-baseweb="input"], div[data-baseweb="base-input"] {
        background-color: #ffffff !important;
        color: #1e293b !important;
        border-color: #a7f3d0 !important;
    }

    input::placeholder {
        color: #94a3b8 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #059669 !important;
        font-family: 'Fredoka', cursive !important;
        font-weight: 700 !important;
        font-size: 36px !important;
    }

    /* Super Action Buttons */
    .stButton>button, div[data-testid="stForm"] button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: #ffffff !important;
        font-family: 'Fredoka', cursive !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        border-radius: 18px !important;
        border: 2px solid #6ee7b7 !important;
        padding: 10px 24px !important;
        box-shadow: 0 6px 16px rgba(16, 185, 129, 0.35) !important;
        transition: transform 0.1s ease;
    }

    .stButton>button:hover, div[data-testid="stForm"] button:hover {
        transform: scale(1.03);
        background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
        color: #ffffff !important;
    }

    /* Big Bright File Drop Box */
    [data-testid="stFileUploader"] {
        background: #f0fdf4 !important;
        border: 3px dashed #10b981 !important;
        border-radius: 20px !important;
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
    st.session_state.username = "Eco Champion"

if "registered_users" not in st.session_state:
    # Demo credentials accepting email or mobile
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
        {"Item": "📦 School Notebooks", "Weight": "1200 g", "EcoPoints": 12, "Date": "2026-10-06"}
    ]

if "pickup_requests" not in st.session_state:
    st.session_state.pickup_requests = [
        {
            "Pickup ID": "HERO-401",
            "Address": "Green Valley School, Classroom 5B",
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
    "🥫 Juice Cans (Metal)": 30,
    "🔋 E-Waste & Batteries": 50,
    "🍎 Fruit Peels (Organic)": 5
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
        "Center Name": "📘 Anna Nagar Paper & Craft Station",
        "Type": "Plastic, Paper & Cardboard",
        "Address": "Anna Nagar West",
        "Contact": "+91 98840 56789",
        "lat": 13.0850,
        "lon": 80.2101
    },
    {
        "Center Name": "⚙️ Ambattur Can & Scrap Depot",
        "Type": "Metal & Glass Recyclables",
        "Address": "Ambattur Industrial Estate",
        "Contact": "+91 97720 11223",
        "lat": 13.1143,
        "lon": 80.1548
    },
    {
        "Center Name": "🌱 Adyar Nature Park Composting Hub",
        "Type": "Wet & Organic Waste",
        "Address": "Adyar Eco Park Zone",
        "Contact": "+91 91234 98765",
        "lat": 13.0125,
        "lon": 80.2570
    }
]

# ----------------- LOGIN & REGISTRATION GATEWAY -----------------
if not st.session_state.authenticated:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_l1, col_l2, col_l3 = st.columns([1.2, 2, 1.2])

    with col_l2:
        st.markdown(
            """
            <div style="text-align: center; margin-bottom: 20px;">
                <div style="font-size: 55px; margin-bottom: 5px;">🌍</div>
                <h1 style="color: #065f46; font-size: 40px; margin-bottom: 4px;">Welcome to Ecoza!</h1>
                <p style="color: #64748b; font-weight: 700;">Please log in with your user email or mobile number.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        auth_tab1, auth_tab2 = st.tabs(["🔐 Log In", "📝 Create New Account"])

        with auth_tab1:
            with st.form("login_form"):
                login_id = st.text_input("User Email or Mobile Number", placeholder="name@example.com or 9876543210")
                login_password = st.text_input("Password", type="password", placeholder="••••••••")
                btn_login = st.form_submit_button("🚀 Enter Ecoza Adventure", use_container_width=True)

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
                        st.error("Incorrect User Email/Mobile Number or password! (Demo: user@ecoza.com / pass: ecoza)")

        with auth_tab2:
            with st.form("signup_form"):
                new_name = st.text_input("Full Name", placeholder="Deepak Raja")
                new_id = st.text_input("User Email or Mobile Number", placeholder="name@example.com or 9876543210")
                new_password = st.text_input("Create Password", type="password", placeholder="••••••••")
                btn_signup = st.form_submit_button("⭐ Sign Up & Become A Hero", use_container_width=True)

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
                        st.success("Account created successfully! Welcome aboard.")
                        st.rerun()

    st.stop()

# ----------------- AUTHENTICATED APP -----------------

# Top Navigation Bar with User Profile & Logout
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
        st.markdown(f'<div class="badge-points">⭐ {st.session_state.ecopoints} pts</div>', unsafe_allow_html=True)
    with col_out:
        if st.button("🚪 Logout", key="logout_btn"):
            st.session_state.authenticated = False
            st.session_state.user_identifier = ""
            st.rerun()

st.caption(f"Logged in as: **{st.session_state.username}** ({st.session_state.user_identifier})")
st.markdown("<hr style='margin-top: 2px; margin-bottom: 22px; border: 0; border-top: 2px dashed #a7f3d0;'>", unsafe_allow_html=True)

# ----------------- 1. Home / Hero Screen -----------------
if st.session_state.current_page == "🏠 Home":
    st.markdown(
        f"""
        <div style="text-align: center; max-width: 820px; margin: 0 auto; padding: 15px 0 20px 0;">
            <div style="background: #fef3c7; color: #b45309; font-weight: 800; font-family: 'Fredoka'; padding: 6px 18px; border-radius: 9999px; display: inline-block; font-size: 14px; margin-bottom: 12px; border: 2px solid #fde68a;">
                🚀 WELCOME HERO {st.session_state.username.upper()}! 🦸‍♀️🦸‍♂️
            </div>
            <h1 style="font-size: 46px; color: #065f46; line-height: 1.2; margin-bottom: 10px;">
                Turn Everyday Waste Into <span style="background: linear-gradient(135deg, #059669, #0284c7); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Awesome Rewards!</span>
            </h1>
            <p style="font-size: 18px; color: #475569; margin-bottom: 20px; font-weight: 700;">
                Learn how recycling protects animals, cleans up cities, and earns you cool badges!
            </p>
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
            <div style="background: #eff6ff; padding: 22px; border-radius: 20px; border: 3px solid #bfdbfe; text-align: center;">
                <div style="font-size: 44px; margin-bottom: 8px;">📷</div>
                <h3 style="color: #1e40af; margin: 0 0 6px 0;">Magic AI Scanner</h3>
                <p style="color: #3b82f6; font-size: 15px; font-weight: 700; margin: 0;">Snap a photo of any bottle or box, and our AI detective names it instantly!</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            """
            <div style="background: #f0fdf4; padding: 22px; border-radius: 20px; border: 3px solid #bbf7d0; text-align: center;">
                <div style="font-size: 44px; margin-bottom: 8px;">🚚</div>
                <h3 style="color: #166534; margin: 0 0 6px 0;">Eco-Van Pickup</h3>
                <p style="color: #22c55e; font-size: 15px; font-weight: 700; margin: 0;">Book our friendly green truck to pick up paper and bottles right from your school!</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            """
            <div style="background: #fffbeb; padding: 22px; border-radius: 20px; border: 3px solid #fde68a; text-align: center;">
                <div style="font-size: 44px; margin-bottom: 8px;">🎁</div>
                <h3 style="color: #92400e; margin: 0 0 6px 0;">Win Cool Prizes</h3>
                <p style="color: #f59e0b; font-size: 15px; font-weight: 700; margin: 0;">Trade your EcoPoints for plant saplings, book coupons, and fruit treats!</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.subheader("🎯 4 Super Easy Steps to Play")
    step1, step2, step3, step4 = st.columns(4)
    step1.success("**Step 1: Sort!**\n\nSeparate plastic bottles, paper, and metal cans.")
    step2.info("**Step 2: Snap!**\n\nTake a picture and let the AI detective weigh it.")
    step3.warning("**Step 3: Collect!**\n\nDrop it at a station or book the eco-van.")
    step4.error("**Step 4: Win!**\n\nSpend your points and climb the school leaderboard!")

# ----------------- 2. AI Scanner & Classifier -----------------
elif st.session_state.current_page == "📸 AI Scanner":
    st.title("📸 Magic AI Waste Detective")
    st.write("Upload a picture or click a photo using your camera to identify the recyclable item!")

    tab1, tab2 = st.tabs(["📁 Upload Item Photo", "📷 Snap With Camera"])
    uploaded_image = None

    with tab1:
        file_input = st.file_uploader("Choose a photo from your device", type=["jpg", "jpeg", "png"])
        if file_input:
            uploaded_image = Image.open(file_input)

    with tab2:
        cam_input = st.camera_input("Smile & take a photo of the item!")
        if cam_input:
            uploaded_image = Image.open(cam_input)

    detected_category = "🥤 Plastic Bottles"
    confidence_score = 96.5

    if uploaded_image:
        col_img, col_pred = st.columns([1, 2])
        with col_img:
            st.image(uploaded_image, caption="Your Mystery Item", use_container_width=True)
        with col_pred:
            possible_categories = list(RATES.keys())
            detected_category = random.choice(possible_categories)
            confidence_score = round(random.uniform(92.0, 99.4), 1)

            st.balloons()
            st.success(f"### 🎉 Detective Result: **{detected_category}**!")
            st.write(f"Confidence score: **{confidence_score}% Match!**")
            st.write(f"Reward value: **{RATES[detected_category]} EcoPoints per 1,000 grams**")

    st.markdown("---")
    st.subheader("⚖️ Enter Estimated Weight (in Grams)")

    with st.form("waste_log_form"):
        selected_category = st.selectbox(
            "Selected Material",
            list(RATES.keys()),
            index=list(RATES.keys()).index(detected_category) if detected_category in RATES else 0
        )
        
        input_grams = st.number_input(
            "Weight in Grams (e.g. 1 bottle is ~50g, 1 notebook is ~250g)",
            min_value=10,
            max_value=25000,
            step=50,
            value=250
        )
        
        rate_per_kg = RATES[selected_category]
        calculated_points = max(1, int((input_grams / 1000.0) * rate_per_kg))
        
        st.info(f"🌟 You will earn: **{calculated_points} Super EcoPoints!**")

        submit_log = st.form_submit_button("🚀 Add To My Hero Score!")
        if submit_log:
            st.session_state.ecopoints += calculated_points
            st.session_state.waste_history.append({
                "Item": selected_category,
                "Weight": f"{input_grams} g",
                "EcoPoints": calculated_points,
                "Date": str(datetime.date.today())
            })
            st.success(f"Awesome job! Added {calculated_points} EcoPoints to your score!")
            st.rerun()

# ----------------- 3. Nearby Collection Centers (Map) -----------------
elif st.session_state.current_page == "🗺️ Drop-off Map":
    st.title("🗺️ Ecoza Drop-Off Treasure Map")
    st.write("Find authorized recycling drop-off centers across Chennai!")

    df_centers = pd.DataFrame(RECYCLING_CENTERS)
    st.map(df_centers[["lat", "lon"]], zoom=11)

    st.subheader("📍 Secret Base Locations & Contacts")
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
    st.title("🚚 Call The Green Eco-Van")
    st.write("Too much paper or cardboard at school or home? Call our recycling superhero van!")

    with st.form("pickup_form"):
        pickup_address = st.text_area("School or Home Address", placeholder="Class 6A, XYZ School, Chennai")
        waste_items = st.multiselect("What are you recycling?", list(RATES.keys()), default=["🥤 Plastic Bottles", "📚 Paper & Notebooks"])
        pickup_date = st.date_input("Preferred Date", min_value=datetime.date.today())
        phone = st.text_input("Contact Mobile Number", placeholder="+91 9876543210")

        submit_booking = st.form_submit_button("🚛 Send The Eco-Van!")
        if submit_booking:
            if not pickup_address or not phone:
                st.error("Please enter both the address and contact number!")
            else:
                new_id = f"HERO-{random.randint(100, 999)}"
                st.session_state.pickup_requests.append({
                    "Pickup ID": new_id,
                    "Address": pickup_address,
                    "Items": ", ".join(waste_items),
                    "Date": str(pickup_date),
                    "Contact": phone,
                    "Status": "Confirmed 🎉"
                })
                st.success(f"Eco-Van Booked! Mission ID: **{new_id}**")
                st.rerun()

    if st.session_state.pickup_requests:
        st.markdown("---")
        st.subheader("📋 Scheduled Eco-Van Trips")
        st.dataframe(pd.DataFrame(st.session_state.pickup_requests), use_container_width=True)

# ----------------- 5. Rewards Store -----------------
elif st.session_state.current_page == "🎁 Rewards Store":
    st.title("🎁 Earth Hero Treasure Store")
    st.write(f"Trade in your hard-earned points for awesome rewards! Balance: **{st.session_state.ecopoints} EcoPoints**")

    rewards_list = [
        {"title": "🌱 Plant A Real Tree With Your Name", "cost": 150, "desc": "A fruit sapling planted in your school garden with your name tag!"},
        {"title": "🍦 Organic Ice Cream Treat Voucher", "cost": 80, "desc": "1 free artisanal fruit popsicle at participating stalls."},
        {"title": "📚 Comic & Stationery Coupon (₹100 Off)", "cost": 100, "desc": "Redeemable at local school bookstores."},
        {"title": "🚌 Green Metro Day Explorer Pass", "cost": 120, "desc": "Free 1-day student transit pass across the city metro line."}
    ]

    col_a, col_b = st.columns(2)
    for idx, reward in enumerate(rewards_list):
        card = col_a if idx % 2 == 0 else col_b
        with card:
            st.markdown(f"### {reward['title']}")
            st.write(reward["desc"])
            st.caption(f"Cost: **{reward['cost']} EcoPoints**")
            
            if st.button(f"Claim Prize ({reward['cost']} pts)", key=f"rwd_{idx}"):
                if st.session_state.ecopoints >= reward["cost"]:
                    st.session_state.ecopoints -= reward["cost"]
                    voucher_code = f"PRIZE-{random.randint(10000, 99999)}"
                    st.session_state.redeemed_coupons.append({
                        "Reward": reward["title"],
                        "Coupon Code": voucher_code,
                        "Date": str(datetime.date.today())
                    })
                    st.snow()
                    st.success(f"🎉 Prize Unlocked! Your Code: **{voucher_code}**")
                    st.rerun()
                else:
                    st.error("Not enough EcoPoints yet! Recycle more to unlock!")
            st.divider()

# ----------------- 6. Champions Leaderboard -----------------
elif st.session_state.current_page == "🏆 Champions Leaderboard":
    st.title("🏆 School District Champions Leaderboard")
    st.write("Check out which classrooms and student leaders saved the most waste this week!")

    leaderboard = [
        {"Rank": "🥇 1st Place", "Student / Class": "Class 8B (Little Flower School)", "Waste Saved": "44,000 g", "EcoPoints": 880},
        {"Rank": "🥈 2nd Place", "Student / Class": "Priya R. (St. Mary's Academy)", "Waste Saved": "38,500 g", "EcoPoints": 770},
        {"Rank": "🥉 3rd Place", "Student / Class": f"{st.session_state.username} (You!)", "Waste Saved": "28,000 g", "EcoPoints": st.session_state.ecopoints},
        {"Rank": "4th Place", "Student / Class": "Karthik Raj (DAV Senior School)", "Waste Saved": "18,500 g", "EcoPoints": 370},
        {"Rank": "5th Place", "Student / Class": "Green Club (PSBB School)", "Waste Saved": "12,000 g", "EcoPoints": 240}
    ]
    st.table(pd.DataFrame(leaderboard))

# ----------------- 7. User Dashboard -----------------
elif st.session_state.current_page == "📊 Impact Dashboard":
    st.title("📊 Your Planet Saving Scorecard")
    st.write("Track how many trees and clean air credits you have earned so far!")

    total_dropoffs = len(st.session_state.waste_history)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Available Points", f"{st.session_state.ecopoints} pts")
    col2.metric("Total Items Recycled", total_dropoffs)
    col3.metric("Eco-Vans Called", len(st.session_state.pickup_requests))
    col4.metric("Fresh Air Created (Est.)", f"{total_dropoffs * 2.2:.1f} kg CO₂")

    st.markdown("---")
    st.subheader("📜 Your Recycling Badge History")
    if st.session_state.waste_history:
        st.dataframe(pd.DataFrame(st.session_state.waste_history), use_container_width=True)

    if st.session_state.redeemed_coupons:
        st.subheader("🎟️ Your Unlocked Prizes & Coupons")
        st.dataframe(pd.DataFrame(st.session_state.redeemed_coupons), use_container_width=True)
