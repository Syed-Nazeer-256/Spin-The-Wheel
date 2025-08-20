import streamlit as st
from PIL import Image
import random
import base64
import time

# Set page layout
st.set_page_config(layout="wide", page_title="Spin the Wheel Game", page_icon="🎯")

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

# Enhanced CSS for better layout and responsiveness
st.markdown(f'''
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans&display=swap');

* {{
    font-family: 'DM Sans', sans-serif;
}}

body {{
    background: #fafafa;
}}

.main-container {{
    display: flex;
    flex-direction: column;
    align-items: center;
    min-height: 80vh;
    padding: 20px;
}}

.wheel-section {{
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 30px;
    width: 100%;
}}

.wheel-container {{
    position: relative;
    width: 400px;
    height: 400px;
    margin: 20px auto;
    filter: drop-shadow(0 8px 32px rgba(0,0,0,0.12));
    display: flex;
    justify-content: center;
    align-items: center;
}}

.wheel {{
    width: 100%;
    height: 100%;
    transition: transform 3s cubic-bezier(0.23, 1, 0.32, 1);
    transform: rotate({st.session_state.rotation}deg);
    border-radius: 50%;
    object-fit: contain;
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
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
}}



.result-container {{
    background: white;
    border-radius: 12px;
    padding: 32px;
    margin: 20px auto;
    max-width: 600px;
    text-align: center;
    box-shadow: 0 4px 24px rgba(0,0,0,0.08);
    border: 1px solid #e1e8ed;
    animation: fadeInUp 0.4s ease-out;
    width: 90%;
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
    font-size: 1.2rem;
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
    animation: pulse 1.5s infinite;
}}

@keyframes pulse {{
    0%, 100% {{
        opacity: 1;
    }}
    50% {{
        opacity: 0.6;
    }}
}}

/* Golden button styling with lightning effects */
div.stButton > button {{
    background: linear-gradient(145deg, #ffd700, #ffb347) !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 18px 50px !important;
    font-size: 1.3rem !important;
    font-weight: 600 !important;
    color: #2c3e50 !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    letter-spacing: 1px !important;
    box-shadow: 0 6px 20px rgba(255, 215, 0, 0.3) !important;
    position: relative !important;
    overflow: hidden !important;
    min-width: 200px !important;
}}

div.stButton > button:hover {{
    background: linear-gradient(145deg, #ffed4e, #ffd700) !important;
    transform: translateY(-3px) !important;
    box-shadow: 
        0 10px 30px rgba(255, 215, 0, 0.5),
        0 0 25px rgba(255, 215, 0, 0.4),
        inset 0 2px 0 rgba(255, 255, 255, 0.3) !important;
    color: #1a252f !important;
}}

div.stButton > button:active {{
    transform: translateY(-1px) !important;
}}

div.stButton > button:focus {{
    outline: none !important;
    box-shadow: 
        0 0 0 4px rgba(255, 215, 0, 0.4),
        0 10px 30px rgba(255, 215, 0, 0.5) !important;
}}

/* Lightning effect on hover */
div.stButton > button::before {{
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.6), transparent);
    transition: left 0.6s ease;
}}

div.stButton > button:hover::before {{
    left: 100%;
}}

div.stButton {{
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    width: 100% !important;
    margin: 0 auto !important;
}}

/* Hide streamlit elements for clean look */
.stDeployButton {{ display: none; }}
#MainMenu {{ visibility: hidden; }}
.stHeader {{ display: none; }}
footer {{ visibility: hidden; }}

.content-container {{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100%;
}}

/* Responsive design */
@media (max-width: 768px) {{
    .wheel-container {{
        width: 300px;
        height: 300px;
    }}
    
    .result-container {{
        padding: 24px;
        margin: 15px;
    }}
    
    .result-question {{
        font-size: 1.1rem;
    }}
}}

</style>
''', unsafe_allow_html=True)





# Create a two-column layout
col_wheel, col_content = st.columns([1.2, 1])

with col_wheel:
    # Wheel display
    wheel_class = "wheel spinning" if st.session_state.spinning else "wheel"
    st.markdown(f'''
    <div class="wheel-container">
        <div class="arrow"></div>
        <img src="data:image/jpeg;base64,{image_base64}" class="{wheel_class}">
    </div>
    ''', unsafe_allow_html=True)

with col_content:
    st.markdown('<div class="content-container">', unsafe_allow_html=True)
    # Result section first
    if st.session_state.spin_result and not st.session_state.spinning:
        st.markdown(f'''
        <div class="result-container">
            <div class="result-text"><b style="color: #FC3030;">Question?</b></div>
            <div class="result-question">{st.session_state.spin_result}</div>
        </div>
        ''', unsafe_allow_html=True)
    elif not st.session_state.spinning:
        st.markdown('''
        <div class="result-container" style="background: #f8f9fa; border: 2px dashed #dee2e6;">
            <div class="result-text">Ready to spin?</div>
            <div class="result-question">Click the button below to get your AWS S3 question!</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Button section - positioned below result
    if st.session_state.spinning:
        st.markdown('<div class="spinning-text">🎪 The wheel is spinning...</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="display: flex; justify-content: center;">', unsafe_allow_html=True)
        if st.button("Spin The Wheel", key="spin_btn"):
            st.session_state.spinning = True
            base_rotation = random.randint(720, 1800)
            extra_rotation = random.randint(0, 359)
            st.session_state.rotation += base_rotation + extra_rotation
            st.session_state.spin_result = ""
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# After the spin, determine the result
if st.session_state.spinning:
    # Removed st.spinner and adjusted sleep time to match CSS transition
    time.sleep(3) # Wait for animation to finish
    
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
        "NAME 2 CLASSES",
        "IF S3 WERE A SUPERHERO, WOULD IT BE INVISIBLE OR NEVER FORGETFUL?",
    ]
    
    # Determine the winning segment.
    # The arrow points downwards, so we are interested in the segment at the top.
    # We add 45 degrees to be in the middle of the segment and account for the offset in the image.
    segment_index = int(((360 - final_angle + 45) % 360) / 30)
    st.session_state.spin_result = questions[segment_index]
    st.rerun()
