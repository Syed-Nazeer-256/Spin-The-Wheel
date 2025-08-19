import streamlit as st
from PIL import Image
import random
import base64
import time

# Set page layout
st.set_page_config(layout="wide", page_title="Spin the Wheel Game", page_icon="🎯")

# Clean, minimal title
st.markdown("""
<h1 style="
    text-align: center; 
    font-size: 2.5rem; 
    color: #2c3e50;
    font-weight: 300;
    margin: 30px 0 50px 0;
    letter-spacing: 3px;
">Spin the Wheel</h1>
""", unsafe_allow_html=True)

# Function to convert image to base64
def get_image_as_base64(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Image path
image_path = "spin-wheel-01.png"
image_base64 = get_image_as_base64(image_path)

# Initialize session state
if 'rotation' not in st.session_state:
    st.session_state.rotation = 0
if 'spinning' not in st.session_state:
    st.session_state.spinning = False
if 'spin_result' not in st.session_state:
    st.session_state.spin_result = ""

# Clean, minimal CSS for elegant styling
st.markdown(f'''
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

* {{
    font-family: 'Inter', sans-serif;
}}

body {{
    background: #fafafa;
}}

.wheel-container {{
    position: relative;
    width: 100%;
    height: auto; /* Let height adjust based on content */
    margin: 40px auto;
    filter: drop-shadow(0 8px 32px rgba(0,0,0,0.12));
}}

.wheel {{
    max-width: 75%; /* Ensure it scales down within its container */
    height: auto;    /* Maintain aspect ratio */
    transition: transform 3.5s cubic-bezier(0.23, 1, 0.32, 1);
    transform: rotate({st.session_state.rotation}deg);
    display: block;
    border-radius: 50%;
}}

.arrow {{
    position: absolute;
    top: -5px;
    left: 50%;
    transform: translateX(-50%);
    width: 0;
    height: 0;
    border-left: 20px solid transparent;
    border-right: 20px solid transparent;
    border-top: 40px solid #ffd700;
    z-index: 10;
}}

.result-container {{
    background: white;
    border-radius: 12px;
    padding: 32px;
    margin: 80px auto;
    max-width: 700px;
    text-align: center;
    box-shadow: 0 4px 24px rgba(0,0,0,0.08);
    border: 1px solid #e1e8ed;
    animation: fadeInUp 0.4s ease-out;
}}

@keyframes fadeInUp {{
    from {{
        opacity: 0;
        transform: translateY(20px);
    }}
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

.result-text {{
    font-size: 1.1rem;
    color: #657786;
    font-weight: 400;
    margin-bottom: 16px;
}}

.result-question {{
    font-size: 1.3rem;
    color: #2c3e50;
    font-weight: 500;
    line-height: 1.5;
}}

.spinning-text {{
    font-size: 1.2rem;
    color: #657786;
    font-weight: 400;
    text-align: center;
    margin: 30px 0;
}}

</style>
''', unsafe_allow_html=True)

# Remove floating particles background
# Clean, minimal approach

col_wheel, col_result = st.columns(2)

with col_wheel:
    # Clean wheel and arrow display
    wheel_class = "wheel spinning" if st.session_state.spinning else "wheel"
    st.markdown(f'''
    <div class="wheel-container">
        <div class="arrow"></div>
        <img src="data:image/jpeg;base64,{image_base64}" class="{wheel_class}">
    </div>
    ''', unsafe_allow_html=True)



# After the spin, determine the result
if st.session_state.spinning:
    # Show spinning indicator
    with st.spinner('🎪 The wheel is spinning...'):
        time.sleep(4) # Wait for animation to finish
    
    st.session_state.spinning = False
    final_angle = st.session_state.rotation % 360

    # There are 12 segments, each 30 degrees.
    # The questions are ordered clockwise on the wheel.
    # The arrow is at the top.
    questions = [
        "UPLOAD A CAT VIDEO TO S3 - HOW MANY COPIES ARE STORED BY DEFAULT?",
        "LOW LATENCY, FREQUENT DATA?",
        "AUTO MOVE TO CHEAPEST TIER?",
        "RARELY USED, BUT FAST ACCESS?",
        "SINGLE AZ, LOWER COST BACKUPS?",
        "MILLISECOND RETRIEVAL, ARCHIVAL?",
        "MINUTES-HOURS RETRIEVAL, CHEAPER ARCHIVE?",
        "CHEAPEST, LONG-TERM HOURS RETRIEVAL?",
        "CHEAPER THAN TAPE? (T/F)",
        "DURABILITY OF ALL TIERS?",
        "NAME 2 CLASSES + USES",
        "IF S3 WERE A SUPERHERO, WOULD IT BE INVISIBLE OR NEVER FORGETFUL?",
    ]
    
    # Determine the winning segment.
    # The arrow points downwards, so we are interested in the segment at the top.
    # We add 45 degrees to be in the middle of the segment and account for the offset in the image.
    segment_index = int(((360 - final_angle + 45) % 360) / 30)
    st.session_state.spin_result = questions[segment_index]
    st.rerun()

with col_result:
    # Clean result display
    if st.session_state.spin_result and not st.session_state.spinning:
        st.markdown(f'''
        <div class="result-container">
            <div class="result-text">Result:</div>
            <div class="result-question">{st.session_state.spin_result}</div>
        </div>
        ''', unsafe_allow_html=True)

    # Spin button logic, centered
    if st.session_state.spinning:
        st.markdown('<div class="spinning-text">Spinning...</div>', unsafe_allow_html=True)
    else:
        if st.button("Spin", key="spin_btn"):
            st.session_state.spinning = True
            base_rotation = random.randint(720, 1800)
            extra_rotation = random.randint(0, 359)
            st.session_state.rotation += base_rotation + extra_rotation
            st.session_state.spin_result = ""
            st.rerun()



# Golden button styling with lightning effects
st.markdown('''
<style>
/* Golden lightning button styling */
div.stButton > button {
    background: linear-gradient(145deg, #ffd700, #ffb347) !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 16px 40px !important; /* Increased padding */
    font-size: 1.2rem !important;   /* Increased font size */
    font-weight: 600 !important;
    color: #2c3e50 !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    width: 100% !important;
    letter-spacing: 0.5px !important;
    box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3) !important;
    position: relative !important;
    overflow: hidden !important;
}

div.stButton > button:hover {
    background: linear-gradient(145deg, #ffed4e, #ffd700) !important;
    transform: translateY(-2px) !important;
    box-shadow: 
        0 8px 25px rgba(255, 215, 0, 0.5),
        0 0 20px rgba(255, 215, 0, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
    color: #1a252f !important;
}

div.stButton > button:active {
    transform: translateY(0px) !important;
}

div.stButton > button:focus {
    outline: none !important;
    box-shadow: 
        0 0 0 3px rgba(255, 215, 0, 0.4),
        0 8px 25px rgba(255, 215, 0, 0.5) !important;
}

/* Lightning effect on hover */
div.stButton > button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
    transition: left 0.5s ease;
}

div.stButton > button:hover::before {
    left: 100%;
}



div.stButton {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
}

/* Hide streamlit elements for clean look */
.stDeployButton { display: none; }
#MainMenu { visibility: hidden; }
.stHeader { display: none; }
footer { visibility: hidden; }

</style>
''', unsafe_allow_html=True)