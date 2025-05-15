
import streamlit as st
import time
import base64

# Set page configuration
st.set_page_config(
    page_title="Gentrification Awareness App",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
def local_css():
    st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stApp {
        background-image: linear-gradient(to bottom right, #f8f9fa, #e9ecef);
    }
    h1, h2, h3 {
        color: #495057;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stButton button {
        background-color: #007bff;
        color: white;
        border-radius: 6px;
        border: none;
        padding: 8px 16px;
        font-weight: 500;
    }
    .stButton button:hover {
        background-color: #0069d9;
    }
    .info-box {
        background-color: #e9ecef;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border-left: 5px solid #007bff;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border-left: 5px solid #ffc107;
    }
    .success-box {
        background-color: #d4edda;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border-left: 5px solid #28a745;
    }
    .danger-box {
        background-color: #f8d7da;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border-left: 5px solid #dc3545;
    }
    .scenario-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .location-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        transition: transform 0.3s;
    }
    .location-card:hover {
        transform: translateY(-5px);
    }
    .module-header {
        background-color: #007bff;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Apply CSS
local_css()

# Initialize session state variables if they don't exist
if 'page' not in st.session_state:
    st.session_state.page = 'main'
if 'learn_module' not in st.session_state:
    st.session_state.learn_module = 1
if 'completed_scenarios' not in st.session_state:
    st.session_state.completed_scenarios = []
if 'donation_info' not in st.session_state:
    st.session_state.donation_info = {
        'name': '',
        'phone': '',
        'email': '',
        'bank': '',
        'amount': ''
    }
if 'donation_confirmed' not in st.session_state:
    st.session_state.donation_confirmed = False

# Function to simulate loading animation
def loading_animation():
    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.01)
        progress_bar.progress(i + 1)
    progress_bar.empty()

# Navigation Functions
def navigate_to(page):
    st.session_state.page = page
    if page == 'main':
        st.session_state.learn_module = 1
        st.session_state.completed_scenarios = []
        st.session_state.donation_confirmed = False
    
# Sidebar navigation
with st.sidebar:
    st.image("https://via.placeholder.com/150x150.png?text=Gentrification+App", width=150)
    st.title("Navigation")
    st.button("Main Menu", on_click=navigate_to, args=('main',), key="nav_main")
    st.button("Learn", on_click=navigate_to, args=('learn',), key="nav_learn")
    st.button("Play", on_click=navigate_to, args=('play',), key="nav_play")
    st.button("Donate", on_click=navigate_to, args=('donate',), key="nav_donate")
    st.button("Source", on_click=navigate_to, args=('source',), key="nav_source")
    st.button("Check Your Area", on_click=navigate_to, args=('check',), key="nav_check")
    
    st.markdown("---")
    st.write("© 2025 Gentrification Awareness")

# Main page
if st.session_state.page == 'main':
    st.title("Welcome to the Gentrification Awareness App! 🏙️")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        <div class="info-box">
        <h3>What is this app about?</h3>
        <p>This interactive application aims to educate people about gentrification, its impacts, and potential solutions. Navigate through different sections to learn, play educational games, check areas at risk, and even donate to support affordable housing initiatives.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Choose an option to begin:")
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.button("Learn About Gentrification", on_click=navigate_to, args=('learn',), key="main_learn")
        with col_b:
            st.button("Play Scenarios Game", on_click=navigate_to, args=('play',), key="main_play")
        with col_c:
            st.button("Check Your Area", on_click=navigate_to, args=('check',), key="main_check")
            
    with col2:
        st.image("https://via.placeholder.com/400x300.png?text=Urban+Development", caption="Urban Development and Change")
        st.markdown("""
        <div class="warning-box">
        <h4>Did you know?</h4>
        <p>Gentrification can lead to the displacement of entire communities and the erasure of cultural heritage.</p>
        </div>
        """, unsafe_allow_html=True)

# Learn page
elif st.session_state.page == 'learn':
    st.title("Learn About Gentrification")
    
    # Module 1
    if st.session_state.learn_module == 1:
        st.markdown("""
        <div class="module-header">
        <h2>Module 1: WHAT IS GENTRIFICATION?</h2>
        </div>
        """, unsafe_allow_html=True)
        
        user_explanation = st.text_area("Try explaining gentrification in your own words:", height=100)
        
        if st.button("Submit"):
            words = ["process", "wealthy", "displacement", "displaced", "displace", "move out"]
            count = sum(1 for word in words if word in user_explanation.lower())
            
            if count > 0:
                st.success("You are on the right track!")
            else:
                st.warning("Not perfect! Allow me to help you!")
            
            st.markdown("""
            <div class="info-box">
            <h3>Gentrification Defined:</h3>
            <p>Gentrification is the displacement of existing low income communities by wealthiest families or newcomers to the re-developeded area.</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Continue to Module 2"):
                st.session_state.learn_module = 2
                st.experimental_rerun()
    
    # Module 2
    elif st.session_state.learn_module == 2:
        st.markdown("""
        <div class="module-header">
        <h2>Module 2: WHO IS IMPACTED BY GENTRIFICATION? AND HOW?</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box">
        <h3>Primary Impact Groups:</h3>
        <p>Gentrification primarily impacts low-income residents and racial minorities (such as black and indigenous communities.)</p>
        <p>As the land is redeveloped, property values increase, leading to higher rents and housing costs for low-income residents. Eventually, these individuals are pushed out of their homes, often without any solid safety net or support to help them about displacement.</p>
        <p>Often the puts the displaced people in a cycle of poverty and hardships without any proper help.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("### Impact on Small Businesses")
        
        small_business_impact = st.radio("Do you think small businesses (i.e. a corner store) in low-income communities can also be impacted by gentrification?", ["Select", "Yes", "No"])
        
        if small_business_impact != "Select":
            if small_business_impact == "Yes":
                st.success("Correct")
            else:
                st.error("Incorrect")
                
            st.write("Gentrification also impacts small businesses. Not just low income residents.")
            
            business_explanation = st.text_area("How do you think small businesses are impacted?", height=100)
            
            if st.button("Submit"):
                words = ["rent", "higher", "loss", "customers", "less", "badly", "bad"]
                count = sum(1 for word in words if word in business_explanation.lower())
                
                if count > 0:
                    st.success("You're getting there!")
                else:
                    st.warning("Not perfect! Allow me to help you!")
                
                st.markdown("""
                <div class="info-box">
                <h3>Impact on Small Businesses:</h3>
                <p>Small businesses in gentrifying areas often face rising rents and changing customer demographics (from low income to high income customers. The shop will not be able to cater to the new customer base), which can lead to displacement or forced closures, even if they have strong local ties in the community.</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("Continue to Module 3"):
                    st.session_state.learn_module = 3
                    st.experimental_rerun()
    
    # Module 3
    elif st.session_state.learn_module == 3:
        st.markdown("""
        <div class="module-header">
        <h2>Module 3: SOLUTIONS AND ACTIONS MOVING FORWARD</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="warning-box">
        <p>Many neighborhoods and communities around the world are currently experiencing gentrification. Low income residents lack any influence or power in society, which leads them to only protest against these changes, but their efforts rarely stop developers from moving forward with redevelopment.</p>
        </div>
        """, unsafe_allow_html=True)
        
        user_ideas = st.text_area("Do you have any ideas on combating gentrification?", height=150)
        
        if st.button("Submit"):
            st.success("You have some interesting ideas!")
            
            st.markdown("""
            <div class="success-box">
            <h3>Community Solutions: CO-OP Housing</h3>
            <p>The idea of CO-OP housing becomes more and more popular in areas undergoing gentrification.</p>
            <p>A CO-OP housing is where a group of low income residents can own a property as a joint ownership. It helps keep housing affordable, gives people control in decisions, and protects communities from being pushed out by gentrification.</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Finish Learning Module"):
                st.session_state.page = 'main'
                st.session_state.learn_module = 1
                st.experimental_rerun()

# Play page
elif st.session_state.page == 'play':
    st.title("Play the Gentrification Scenario Game")
    
    st.markdown("""
    <div class="info-box">
    <h3>How to Play:</h3>
    <p>You will be given scenarios about urban development. Your job is to determine the chance of gentrification in each scenario!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # List of scenarios not yet completed
    available_scenarios = [
        scenario for scenario in ["A", "B", "C"] 
        if scenario not in st.session_state.completed_scenarios
    ]
    
    if available_scenarios:
        st.write(f"### Choose from scenarios: {', '.join(available_scenarios)}")
        scenario_choice = st.selectbox("Select scenario:", ["Select"] + available_scenarios)
        
        if scenario_choice != "Select":
            if scenario_choice == "A":
                st.markdown("""
                <div class="scenario-card">
                <h3>Scenario A</h3>
                <p>A historically working-class neighborhood in a large city started opening many new coffee shops, public spaces, and working spaces. Land values have begun to rise, and older apartment buildings are being renovated. A company has plans to move its headquarters into the area, bringing in many new, higher-income employees. What is the chance of Gentrification?</p>
                </div>
                """, unsafe_allow_html=True)
                
                answer = st.radio("Your answer:", ["Select", "A) Low", "B) Medium", "C) High", "D) None of the Above"])
                
                if answer != "Select" and st.button("Submit Answer"):
                    if answer == "C) High":
                        st.success("CORRECT!")
                    else:
                        st.error("WRONG. Correct answer is C) High")
                    
                    st.session_state.completed_scenarios.append("A")
                    st.experimental_rerun()
                    
            elif scenario_choice == "B":
                st.markdown("""
                <div class="scenario-card">
                <h3>Scenario B</h3>
                <p>In a new neighborhood, new commercial districts have arrived. A new Walmart and Ikea has opened up in the area. What is the chance of gentrification in this area?</p>
                </div>
                """, unsafe_allow_html=True)
                
                answer = st.radio("Your answer:", ["Select", "A) Medium", "B) High", "C) Low", "D) None of the Above"])
                
                if answer != "Select" and st.button("Submit Answer"):
                    if answer == "A) Medium":
                        st.success("CORRECT!")
                    else:
                        st.error("WRONG. Correct answer is A) Medium")
                    
                    st.session_state.completed_scenarios.append("B")
                    st.experimental_rerun()
                    
            elif scenario_choice == "C":
                st.markdown("""
                <div class="scenario-card">
                <h3>Scenario C</h3>
                <p>A small suburb in Ontario has spent money on improving neighborhood parks and schools. They have also added more park benches and expanded their park space within the neighborhood.</p>
                </div>
                """, unsafe_allow_html=True)
                
                answer = st.radio("Your answer:", ["Select", "A) Medium", "B) Low", "C) High", "D) None of the Above"])
                
                if answer != "Select" and st.button("Submit Answer"):
                    if answer == "B) Low":
                        st.success("CORRECT!")
                    else:
                        st.error("WRONG. Correct answer is B) Low")
                    
                    st.session_state.completed_scenarios.append("C")
                    st.experimental_rerun()
    else:
        st.markdown("""
        <div class="success-box">
        <h3>Congratulations!</h3>
        <p>You have completed all the scenarios!</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Return to Main Menu"):
            st.session_state.page = 'main'
            st.session_state.completed_scenarios = []
            st.experimental_rerun()

# Donate page
elif st.session_state.page == 'donate':
    st.title("Donate to Support Affordable Housing")
    
    if not st.session_state.donation_confirmed:
        st.markdown("""
        <div class="info-box">
        <h3>Welcome to the donation page!</h3>
        <p>You must be wondering... What do we do with your donations?</p>
        <p>It goes towards helping to fund affordable housing! With your donations, we can ensure that people with the lowest incomes have a place which they can call home.</p>
        <p>Our vision is to ensure that all communities in Canada have affordable housing and their cultures and ways of life are well preserved.</p>
        <p>We have collaborated with Canadian NGOs such as Ottawa Community Land Trust and Team Interact to make our Canadian vision come true in all communities. Step by step we are providing rental properties for low income groups and with your help and donations we can go beyond our vision!</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("### Make a Donation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.session_state.donation_info['name'] = st.text_input("Enter your first and last name:", value=st.session_state.donation_info['name'])
            st.session_state.donation_info['phone'] = st.text_input("Enter your phone number:", value=st.session_state.donation_info['phone'])
            st.session_state.donation_info['email'] = st.text_input("Enter your E-mail:", value=st.session_state.donation_info['email'])
        
        with col2:
            st.session_state.donation_info['bank'] = st.text_input("Enter your bank:", value=st.session_state.donation_info['bank'])
            st.session_state.donation_info['amount'] = st.text_input("Enter the amount you want to donate:", value=st.session_state.donation_info['amount'])
            
        # Check if all fields are filled
        all_filled = all(st.session_state.donation_info.values())
        
        if all_filled:
            st.write("### Confirm Your Information")
            
            for key, value in st.session_state.donation_info.items():
                st.write(f"**{key.title()}:** {value}")
                
            if st.button("Confirm Donation"):
                try:
                    # Validate amount is a number
                    float(st.session_state.donation_info['amount'])
                    loading_animation()
                    st.session_state.donation_confirmed = True
                    st.experimental_rerun()
                except ValueError:
                    st.error("Please enter a valid number for the donation amount")
    else:
        st.markdown(f"""
        <div class="success-box">
        <h2>Thank You For Donating!</h2>
        <p>Name: {st.session_state.donation_info['name']}</p>
        <p>Your Donation Amount: ${st.session_state.donation_info['amount']}</p>
        <p>Your contribution will help provide affordable housing for those in need.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Return to Main Menu"):
            st.session_state.page = 'main'
            st.session_state.donation_confirmed = False
            st.session_state.donation_info = {key: '' for key in st.session_state.donation_info}
            st.experimental_rerun()

# Source page
elif st.session_state.page == 'source':
    st.title("Sources and References")
    
    st.markdown("""
    <div class="info-box">
    <h3>Academic and Media Sources</h3>
    <ul>
        <li>Duncan, Pamela, et al. 'Housing: how 14 years of Tory rule have changed Britain – in charts'. The Guardian, 1 July 2024, https://www.theguardian.com/politics/article/2024/jul/01/housing-how-14-years-of-tory-rule-have-changed-britain-in-charts?utm_source. Accessed 23 April 2025.</li>
        <li>REtripster, et al. What Is 'Gentrification?' YouTube, 16 June 2020, youtu.be/s07D45uHmVY?si=ZcSF7GEybjK4PyEK. Accessed 23 April 23, 2025.</li>
        <li>Wheatle, Alex et al. 'Alex Wheatle on the gentrification of Brixton' YouTube, 6 August 2013, https://youtu.be/D4by4BEPwAw?si=aLZqMWdRJoc5kPBi. Accessed 23, 2025.</li>
        <li>Kane, Laura. 'Vancouver's vision for Downtown Eastside stokes anti-gentrification protests.' Toronto Star, 25 May 2013, https://www.thestar.com/news/canada/vancouver-s-vision-for-downtown-eastside-stokes-anti-gentrification-protests/article_16a77469-5d37-5b4c-b61f-9a9a68b0a95a.html. Accessed 23 April 2025.</li>
        <li>Dorazio, Justin. 'Ways To Combat the Effects of Gentrification and Lack of Affordable Housing' American Progress, 26 September 2022, https://www.americanprogress.org/article/localized-anti-displacement-policies/?utm_source. Accessed 23 April 2025.</li>
        <li>Sutton, Stacey. 'What we don't understand about gentrification' YouTube https://youtu.be/XqogaDX48nI?si=vSh34frFnoAfaa3Y. Accessed 23 April 2025.</li>
        <li>Canada, Housing Federation. 'About Co-op Housing About Co-op Housing.' CHF Canada, https://chfcanada.coop/about-co-op-housing/. Accessed 23 April 2025.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
    <h3>Further Reading</h3>
    <p>For more information on gentrification, affordable housing solutions, and community-based initiatives, check out these additional resources:</p>
    <ul>
        <li>National Low Income Housing Coalition: <a href="https://nlihc.org/">https://nlihc.org/</a></li>
        <li>Urban Displacement Project: <a href="https://www.urbandisplacement.org/">https://www.urbandisplacement.org/</a></li>
        <li>Right to the City Alliance: <a href="https://righttothecity.org/">https://righttothecity.org/</a></li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# Check your area page
elif st.session_state.page == 'check':
    st.title("Check Gentrification Risk in Your Area")
    
    st.markdown("""
    <div class="info-box">
    <h3>Proactive Awareness</h3>
    <p>In this CHECK page, you have the ability to check the chance of gentrification in your area! With this information you can be pro-active rather than re-active!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Locations and their info
    locations = {
        "ELGIN STREET": """
            <div class="location-card">
            <h3>ELGIN STREET</h3>
            <p>Elgin Street is a street in the Downtown core of Ottawa. Currently it faces a lot of urban stress such as low maintenance, some garbage, drugs and smoking. Lot of the land use is mixed (commercial and residential). As a part of the downtown core, it has a <strong style="color: #fd7e14;">medium chance</strong> of getting gentrified and redeveloped.</p>
            </div>
        """,
        "KANATA LAKES": """
            <div class="location-card">
            <h3>KANATA LAKES</h3>
            <p>Kanata Lakes- a cluster of suburban neighbourhoods, parks, greenspace, and golf courses to the west of downtown Ottawa. Kanata Lakes is already a high end neighborhood close to many commercial centers and large tech companies. The chance of major gentrification is <strong style="color: #28a745;">low</strong>.</p>
            </div>
        """,
        "MERIVALE ROAD": """
            <div class="location-card">
            <h3>MERIVALE ROAD</h3>
            <p>Merivale Road, a significant road in Ottawa connecting schools, housing, restaurants, shops and malls all in one road. It includes many transport links. Going further down the road, there is an industrial park as well as a farm. Considering this, Merivale Road will not be going through gentrification anytime soon. However it is a <strong style="color: #fd7e14;">possibility later on</strong>.</p>
            </div>
        """,
        "BEAVERBROOK": """
            <div class="location-card">
            <h3>BEAVERBROOK</h3>
            <p>Beaverbrook is another small cluster of neighborhoods to the right of Kanata Lakes. It is an older religion than Kanata Lakes and has low income and Co-Op housing. Due to this fact, the area may be redeveloped in the future. The chance of redevelopment and gentrification is <strong style="color: #dc3545;">high</strong>.</p>
            </div>
        """,
        "LANSDOWNE": """
            <div class="location-card">
            <h3>LANSDOWNE</h3>
            <p>Lansdowne- located in the very core of Ottawa downtown, it is a very popular area for visitors. Home to Lansdowne Park which is a world-class attraction with modern services combined with heritage sites. The land value is already high. Any gentrification in the future is <strong style="color: #28a745;">very low</strong>.</p>
            </div>
        """
    }
    
    # Create a multi-select for locations
    selected_location = st.selectbox("Select a location to check:", ["Select a location"] + list(locations.keys()))
    
    if selected_location != "Select a location":
        st.markdown(locations[selected_location], unsafe_allow_html=True)
        
        # Map placeholder (in a real app, this would be an actual map)
        st.markdown(f"""
        <div style="background-color: #e9ecef; padding: 10px; border-radius: 5px; text-align: center;">
            <p>Map of {selected_location}</p>
            <img src="https://via.placeholder.com/600x300.png?text=Map+of+{selected_location.replace(' ', '+')}" style="max-width: 100%; border-radius: 5px;">
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("""
    <div class="warning-box">
    <p>*More locations coming soon*</p>
    <p>Want to check an area not listed? Contact us to request an assessment for your neighborhood.</p>
    </div>
    """, unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    # This code is already running within Streamlit
    pass

