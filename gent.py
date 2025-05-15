import streamlit as st
import time
import base64
from typing import Dict, List, Optional
import json
from pathlib import Path
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
THEME = {
    'light': {
        'primary': '#1E3A8A',
        'secondary': '#3B82F6',
        'background': '#F0F9FF',
        'text': '#1F2937',
        'success': '#047857',
        'error': '#DC2626',
        'warning': '#F59E0B'
    },
    'dark': {
        'primary': '#60A5FA',
        'secondary': '#93C5FD',
        'background': '#1F2937',
        'text': '#F9FAFB',
        'success': '#34D399',
        'error': '#EF4444',
        'warning': '#FBBF24'
    }
}

# Set page configuration with improved metadata
st.set_page_config(
    page_title="Gentrification Awareness App",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/gentrification-app',
        'Report a bug': 'https://github.com/yourusername/gentrification-app/issues',
        'About': '''
        # Gentrification Awareness App
        This app helps educate about gentrification, its impacts, and potential solutions.
        Built with Streamlit and ❤️ for community awareness.
        '''
    }
)

# Fixed CSS with proper structure and no duplicates
st.markdown("""
<style>
    /* Base styles with dark mode support */
    :root {
        --primary-color: #1E3A8A;
        --secondary-color: #3B82F6;
        --background-color: #F0F9FF;
        --text-color: #1F2937;
        --success-color: #047857;
        --error-color: #DC2626;
        --warning-color: #F59E0B;
    }

    @media (prefers-color-scheme: dark) {
        :root {
            --primary-color: #60A5FA;
            --secondary-color: #93C5FD;
            --background-color: #1F2937;
            --text-color: #F9FAFB;
            --success-color: #34D399;
            --error-color: #EF4444;
            --warning-color: #FBBF24;
        }
    }

    /* Typography and base styles */
    * {
        font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        line-height: 1.5;
    }

    /* Headers */
    .main-header {
        font-size: clamp(2rem, 5vw, 2.625rem);
        font-weight: 800;
        color: var(--primary-color);
        text-align: center;
        margin-bottom: 1.5rem;
        padding: 1.5rem;
        background-color: var(--background-color);
        border-radius: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .module-header {
        font-size: 1.75rem;
        font-weight: 700;
        color: var(--primary-color);
        margin: 1.25rem 0 1rem;
        padding: 0.75rem;
        background-color: var(--background-color);
        border-radius: 0.5rem;
    }

    .sub-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--primary-color);
        margin: 1rem 0 0.75rem;
    }

    /* Cards */
    .card {
        padding: 1.5rem;
        border-radius: 1rem;
        background-color: var(--background-color);
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }

    .scenario-card {
        padding: 1.5rem;
        border-radius: 1rem;
        background-color: var(--background-color);
        margin-bottom: 1.5rem;
        border-left: 0.5rem solid var(--secondary-color);
    }

    .donate-card {
        padding: 1.5rem;
        border-radius: 1rem;
        background-color: var(--background-color);
        margin-bottom: 1.5rem;
        border-left: 0.5rem solid var(--success-color);
    }

    .location-card {
        padding: 1.25rem;
        border-radius: 0.75rem;
        background-color: var(--background-color);
        margin-bottom: 1.25rem;
        border-left: 0.5rem solid var(--secondary-color);
    }

    /* Interactive elements */
    .button-primary {
        background-color: var(--primary-color);
        color: white;
        border-radius: 0.5rem;
        padding: 0.75rem 1rem;
        font-weight: 600;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .button-primary:hover {
        background-color: var(--secondary-color);
        transform: translateY(-1px);
    }

    .button-success {
        background-color: var(--success-color);
        color: white;
        border-radius: 0.5rem;
        padding: 0.75rem 1rem;
        font-weight: 600;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .button-warning {
        background-color: var(--warning-color);
        color: white;
        border-radius: 0.5rem;
        padding: 0.75rem 1rem;
        font-weight: 600;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    /* Progress and status indicators */
    .progress-container {
        width: 100%;
        background-color: var(--background-color);
        border-radius: 1rem;
        margin: 1.5rem 0;
        overflow: hidden;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .progress-bar {
        height: 0.75rem;
        border-radius: 1rem;
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        transition: width 0.5s ease-in-out;
    }

    /* Status messages */
    .correct-answer {
        color: var(--success-color);
        font-weight: 600;
    }

    .wrong-answer {
        color: var(--error-color);
        font-weight: 600;
    }

    .highlight-text {
        background-color: var(--warning-color);
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        color: var(--text-color);
    }

    /* Form elements */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 0.5rem;
        border: 2px solid var(--background-color);
        padding: 0.75rem;
        transition: border-color 0.3s ease;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary-color);
        outline: none;
    }

    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .main-header {
            font-size: 1.75rem;
            padding: 1rem;
        }
        
        .module-header {
            font-size: 1.5rem;
        }
        
        .card {
            padding: 1rem;
        }
        
        .button-primary,
        .button-success,
        .button-warning {
            padding: 0.5rem 0.75rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session states
if 'page' not in st.session_state:
    st.session_state.page = 'HOME'
if 'completed_scenarios' not in st.session_state:
    st.session_state.completed_scenarios = []
if 'donation_info' not in st.session_state:
    st.session_state.donation_info = {'name': '', 'phone': '', 'email': '', 'bank': '', 'amount': ''}
if 'confirm_donation' not in st.session_state:
    st.session_state.confirm_donation = False
if 'donation_successful' not in st.session_state:
    st.session_state.donation_successful = False
if 'learn_progress' not in st.session_state:
    st.session_state.learn_progress = 0
if 'current_module' not in st.session_state:
    st.session_state.current_module = 1
if 'scenario_result' not in st.session_state:
    st.session_state.scenario_result = None

# Fixed navigation function with proper error handling
def navigate_to(page: str) -> None:
    """Navigate to a different page with proper state management"""
    try:
        if page not in ['HOME', 'LEARN', 'PLAY', 'DONATE', 'CHECK', 'SOURCE', 'CLOSE']:
            raise ValueError(f"Invalid page: {page}")
        
        st.session_state.page = page
        
        # Reset relevant session states
        if page == 'PLAY':
            st.session_state.completed_scenarios = []
            st.session_state.current_scenario = None
            st.session_state.scenario_result = None
        elif page == 'DONATE':
            reset_donation()
        elif page == 'LEARN':
            st.session_state.learn_progress = 0
            st.session_state.current_module = 1
        
        logger.info(f"Navigated to {page}")
        st.rerun()
    except Exception as e:
        logger.error(f"Navigation error: {str(e)}")
        st.error("An error occurred during navigation. Please try again.")

def reset_donation():
    st.session_state.donation_info = {'name': '', 'phone': '', 'email': '', 'bank': '', 'amount': ''}
    st.session_state.confirm_donation = False
    st.session_state.donation_successful = False

def next_module():
    if st.session_state.current_module < 3:
        st.session_state.current_module += 1
        st.session_state.learn_progress = (st.session_state.current_module - 1) * 33.33
    else:
        st.session_state.learn_progress = 100

# Fixed scenario answer checking
def check_scenario_answer(scenario: str, answer: str) -> bool:
    """Check if the answer is correct for a given scenario"""
    try:
        if not scenario or not answer:
            raise ValueError("Scenario and answer must be provided")
        
        correct_answers = {
            "A": "C",
            "B": "A",
            "C": "B"
        }
        
        return correct_answers.get(scenario) == answer
    except Exception as e:
        logger.error(f"Error checking scenario answer: {str(e)}")
        return False

# Fixed sidebar navigation
def render_sidebar():
    """Render the sidebar with proper navigation"""
    with st.sidebar:
        # Logo with proper alt text
        st.image(
            "https://via.placeholder.com/150x150.png?text=Gentrification+App",
            width=150,
            caption="Gentrification Awareness App Logo"
        )
        
        st.markdown("### Navigation")
        
        # Navigation items with proper keys and tooltips
        nav_items = [
            ("🏠 Home", "home_nav", "HOME", "Return to the main page"),
            ("📚 Learn", "learn_nav", "LEARN", "Start learning about gentrification"),
            ("🎮 Play", "play_nav", "PLAY", "Test your knowledge with scenarios"),
            ("💰 Donate", "donate_nav", "DONATE", "Support affordable housing initiatives"),
            ("🔍 Check Your Area", "check_nav", "CHECK", "Check gentrification risk in your area"),
            ("📋 Sources", "source_nav", "SOURCE", "View sources and references"),
            ("❌ Close App", "close_nav", "CLOSE", "Exit the application")
        ]
        
        for label, key, page, tooltip in nav_items:
            if st.button(
                label,
                key=key,
                help=tooltip,
                use_container_width=True
            ):
                navigate_to(page)
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        This app is designed to educate about gentrification, its impacts, and potential solutions.
        Built with ❤️ for community awareness.
        """)

# Sidebar Navigation
with st.sidebar:
    st.image("https://via.placeholder.com/150x150.png?text=Gentrification+App", width=150)
    st.markdown("### Navigation")
    
    if st.button("🏠 Home", key="home_nav"):
        navigate_to('HOME')
    
    if st.button("📚 Learn", key="learn_nav"):
        navigate_to('LEARN')
    
    if st.button("🎮 Play", key="play_nav"):
        navigate_to('PLAY')
    
    if st.button("💰 Donate", key="donate_nav"):
        navigate_to('DONATE')
    
    if st.button("🔍 Check Your Area", key="check_nav"):
        navigate_to('CHECK')
    
    if st.button("📋 Sources", key="source_nav"):
        navigate_to('SOURCE')
    
    if st.button("❌ Close App", key="close_nav"):
        navigate_to('CLOSE')
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("This app is designed to educate about gentrification, its impacts, and potential solutions.")

# Main content area
def render_home():
    st.markdown('<div class="main-header">Welcome to the Gentrification Awareness App</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("""
        ### What is this app about?
        
        This interactive application helps you understand the concept of **gentrification**, its impact on communities, 
        and what can be done about it. Through educational modules, interactive scenarios, and resources, you'll learn about:
        
        - The process and effects of gentrification
        - Who is impacted and how
        - Solutions and possible actions
        - How to assess gentrification risk in different areas
        
        Use the sidebar navigation to explore the different sections of the app.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Quick Access")
        
        if st.button("Learn About Gentrification", key="home_learn"):
            navigate_to('LEARN')
        
        if st.button("Test Your Knowledge", key="home_play"):
            navigate_to('PLAY')
        
        if st.button("Support Affordable Housing", key="home_donate"):
            navigate_to('DONATE')
        
        if st.button("Check Gentrification Risk", key="home_check"):
            navigate_to('CHECK')
        st.markdown('</div>', unsafe_allow_html=True)

def render_learn():
    st.markdown('<div class="main-header">Learning About Gentrification</div>', unsafe_allow_html=True)
    
    # Progress bar
    st.markdown('<div class="progress-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="progress-bar" style="width:{st.session_state.learn_progress}%;"></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Module 1
    if st.session_state.current_module == 1:
        st.markdown('<div class="module-header">Module 1: WHAT IS GENTRIFICATION?</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        user_explanation = st.text_area("Try explaining gentrification in your own words:", height=100)
        
        if st.button("Submit"):
            words = ["process", "wealthy", "displacement", "displaced", "displace", "move out"]
            count = sum(1 for word in words if word in user_explanation.lower())
            
            if count > 0:
                st.success("You are on the right track!")
            else:
                st.warning("Not perfect! Allow me to help you!")
            
            st.markdown("""
            **Gentrification** is the displacement of existing low income communities by wealthiest families 
            or newcomers to the re-developeded area.
            """)
            
            if st.button("Continue to Module 2"):
                next_module()
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Module 2
    elif st.session_state.current_module == 2:
        st.markdown('<div class="module-header">Module 2: WHO IS IMPACTED BY GENTRIFICATION? AND HOW?</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("""
        Gentrification primarily impacts low-income residents and racial minorities (such as black and indigenous communities).

        As the land is redeveloped, property values increase, leading to higher rents and housing costs for low-income residents. 
        Eventually, these individuals are pushed out of their homes, often without any solid safety net or support to help them 
        about displacement.

        Often the puts the displaced people in a cycle of poverty and hardships without any proper help.
        """)
        
        small_business_impact = st.radio(
            "Do you think small businesses (i.e. a corner store) in low-income communities can also be impacted by gentrification?",
            ["Select an answer", "Yes", "No"]
        )
        
        if small_business_impact != "Select an answer":
            if small_business_impact == "Yes":
                st.success("Correct! Gentrification also impacts small businesses. Not just low income residents.")
            else:
                st.error("Incorrect! Gentrification also impacts small businesses. Not just low income residents.")
            
            business_explanation = st.text_area("How do you think small businesses are impacted?", height=100)
            
            if st.button("Submit"):
                words = ["rent", "higher", "loss", "customers", "less", "badly", "bad"]
                count = sum(1 for word in words if word in business_explanation.lower())
                
                if count > 0:
                    st.success("You're getting there!")
                else:
                    st.warning("Not perfect! Allow me to help you!")
                
                st.markdown("""
                Small businesses in gentrifying areas often face rising rents and changing customer demographics 
                (from low income to high income customers. The shop will not be able to cater to the new customer base), 
                which can lead to displacement or forced closures, even if they have strong local ties in the community.
                """)
                
                if st.button("Continue to Module 3"):
                    next_module()
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Module 3
    elif st.session_state.current_module == 3:
        st.markdown('<div class="module-header">Module 3: SOLUTIONS AND ACTIONS MOVING FORWARD</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("""
        Many neighborhoods and communities around the world are currently experiencing gentrification. 
        Low income residents lack any influence or power in society, which leads them to only protest against these changes, 
        but their efforts rarely stop developers from moving forward with redevelopment.
        """)
        
        user_ideas = st.text_area("Do you have any ideas on combating gentrification?", height=100)
        
        if st.button("Submit"):
            st.success("You have some interesting ideas!")
            
            st.markdown("""
            ### CO-OP Housing as a Solution

            The idea of CO-OP housing becomes more and more popular in areas undergoing gentrification.

            A CO-OP housing is where a group of low income residents can own a property as a joint ownership. 
            It helps keep housing affordable, gives people control in decisions, and protects communities from 
            being pushed out by gentrification.
            """)
            
            if st.button("Complete Learning Module"):
                st.session_state.learn_progress = 100
                st.success("You've completed all learning modules! Return to the Home page or explore other sections.")
                
                # Button to go back to main page
                if st.button("Return to Home"):
                    navigate_to('HOME')
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def render_play():
    st.markdown('<div class="main-header">Test Your Knowledge</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("""
    ### Scenario Challenge
    
    You will be given scenarios related to community development.
    Your job is to assess the chance of GENTRIFICATION in each scenario!
    
    Complete all three scenarios to test your understanding.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Available scenarios
    available_scenarios = ["A", "B", "C"]
    completed_scenarios = st.session_state.completed_scenarios
    remaining_scenarios = [s for s in available_scenarios if s not in completed_scenarios]
    
    if not remaining_scenarios:
        st.success("🎉 Congratulations! You've completed all scenarios!")
        if st.button("Play Again"):
            st.session_state.completed_scenarios = []
            st.rerun()
        if st.button("Return to Home"):
            navigate_to('HOME')
            st.rerun()
        return
    
    # Scenario selection
    if 'current_scenario' not in st.session_state:
        st.session_state.current_scenario = None
    
    if st.session_state.current_scenario is None:
        st.markdown("### Choose a Scenario")
        cols = st.columns(len(remaining_scenarios))
        for i, scenario in enumerate(remaining_scenarios):
            with cols[i]:
                if st.button(f"Scenario {scenario}", key=f"scenario_{scenario}"):
                    st.session_state.current_scenario = scenario
                    st.session_state.scenario_result = None
                    st.rerun()
    else:
        # Display the current scenario
        st.markdown('<div class="scenario-card">', unsafe_allow_html=True)
        
        if st.session_state.current_scenario == "A":
            st.markdown("### Scenario A")
            st.markdown("""
            A historically working-class neighborhood in a large city started opening many new coffee shops, 
            public spaces, and working spaces. Land values have begun to rise, and older apartment buildings 
            are being renovated. A company has plans to move its headquarters into the area, bringing in many 
            new, higher-income employees. 
            
            **What is the chance of Gentrification?**
            """)
            options = ["A) Low", "B) Medium", "C) High", "D) None of the Above"]
            correct_answer = "C) High"
            
        elif st.session_state.current_scenario == "B":
            st.markdown("### Scenario B")
            st.markdown("""
            In a new neighborhood, new commercial districts have arrived. A new Walmart and 
            Ikea has opened up in the area. 
            
            **What is the chance of gentrification in this area?**
            """)
            options = ["A) Medium", "B) High", "C) Low", "D) None of the Above"]
            correct_answer = "A) Medium"
            
        else:  # Scenario C
            st.markdown("### Scenario C")
            st.markdown("""
            A small suburb in Ontario has spent money on improving neighborhood parks and schools. 
            They have also added more park benches and expanded their park space within the neighborhood.
            
            **What is the chance of Gentrification?**
            """)
            options = ["A) Medium", "B) Low", "C) High", "D) None of the Above"]
            correct_answer = "B) Low"
        
        # Answer selection
        user_answer = st.radio("Select your answer:", options, key=f"answer_{st.session_state.current_scenario}")
        
        if st.button("Submit Answer"):
            if user_answer == correct_answer:
                st.session_state.scenario_result = "correct"
            else:
                st.session_state.scenario_result = "incorrect"
            st.rerun()
        
        # Show result if available
        if st.session_state.scenario_result == "correct":
            st.success("CORRECT! 🎉")
            st.session_state.completed_scenarios.append(st.session_state.current_scenario)
            if st.button("Continue"):
                st.session_state.current_scenario = None
                st.session_state.scenario_result = None
                st.rerun()
        elif st.session_state.scenario_result == "incorrect":
            st.error(f"WRONG. The correct answer is {correct_answer}")
            st.session_state.completed_scenarios.append(st.session_state.current_scenario)
            if st.button("Continue"):
                st.session_state.current_scenario = None
                st.session_state.scenario_result = None
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Option to go back to scenario selection
        if st.button("Back to Scenario Selection"):
            st.session_state.current_scenario = None
            st.session_state.scenario_result = None
            st.rerun()

def render_donate():
    st.markdown('<div class="main-header">Support Affordable Housing</div>', unsafe_allow_html=True)
    
    if st.session_state.donation_successful:
        st.markdown('<div class="donate-card">', unsafe_allow_html=True)
        st.success(f"Thank You, {st.session_state.donation_info['name']}! Your donation of ${st.session_state.donation_info['amount']} has been processed.")
        st.markdown("Your contribution will help fund affordable housing initiatives and support communities at risk of displacement.")
        
        if st.button("Make Another Donation"):
            reset_donation()
            st.rerun()
        
        if st.button("Return to Home"):
            navigate_to('HOME')
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # Information about donations
    if not st.session_state.confirm_donation:
        st.markdown('<div class="donate-card">', unsafe_allow_html=True)
        st.markdown("### What We Do With Your Donations")
        st.markdown("""
        Your donations go towards helping to fund affordable housing! With your support, we can ensure 
        that people with the lowest incomes have a place which they can call home.

        Our vision is to ensure that all communities in Canada have affordable housing and their cultures 
        and ways of life are well preserved.

        We have collaborated with Canadian NGOs such as Ottawa Community Land Trust and Team Interact to 
        make our Canadian vision come true in all communities. Step by step we are providing rental properties 
        for low income groups and with your help and donations we can go beyond our vision!
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Donation form
        st.markdown('<div class="donate-card">', unsafe_allow_html=True)
        st.markdown("### Make a Donation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.session_state.donation_info['name'] = st.text_input("Full Name", st.session_state.donation_info['name'])
            st.session_state.donation_info['email'] = st.text_input("Email Address", st.session_state.donation_info['email'])
            st.session_state.donation_info['bank'] = st.text_input("Bank Name", st.session_state.donation_info['bank'])
        
        with col2:
            st.session_state.donation_info['phone'] = st.text_input("Phone Number", st.session_state.donation_info['phone'])
            st.session_state.donation_info['amount'] = st.text_input("Donation Amount ($)", st.session_state.donation_info['amount'])
        
        # Validate form
        all_fields_filled = all(st.session_state.donation_info.values())
        amount_is_number = st.session_state.donation_info['amount'].isdigit() if st.session_state.donation_info['amount'] else False
        
        if st.button("Review Donation", disabled=not (all_fields_filled and amount_is_number)):
            if not amount_is_number:
                st.error("Donation amount must be a number")
            else:
                st.session_state.confirm_donation = True
                st.rerun()
        
        if not all_fields_filled:
            st.info("Please fill in all fields to proceed")
        st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        # Confirmation page
        st.markdown('<div class="donate-card">', unsafe_allow_html=True)
        st.markdown("### Review Your Donation")
        
        st.markdown("<div style='padding: 20px; background-color: #f8fafc; border-radius: 10px;'>", unsafe_allow_html=True)
        st.markdown(f"**Name:** {st.session_state.donation_info['name']}")
        st.markdown(f"**Phone Number:** {st.session_state.donation_info['phone']}")
        st.markdown(f"**Email:** {st.session_state.donation_info['email']}")
        st.markdown(f"**Bank:** {st.session_state.donation_info['bank']}")
        st.markdown(f"**Donation Amount:** ${st.session_state.donation_info['amount']}")
        st.markdown("</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Confirm Donation"):
                st.session_state.donation_successful = True
                st.rerun()
        
        with col2:
            if st.button("Edit Information"):
                st.session_state.confirm_donation = False
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def render_check():
    st.markdown('<div class="main-header">Check Gentrification Risk in Your Area</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("""
    ### Gentrification Risk Assessment
    
    In this section, you can check the chance of gentrification in various areas in Ottawa.
    With this information, you can be pro-active rather than re-active!
    
    Select a location below to learn about its gentrification risk profile.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Available locations
    locations = {
        "ELGIN STREET": {
            "description": "Elgin Street is a street in the Downtown core of Ottawa. Currently it faces a lot of urban stress such as low maintenance, some garbage, drugs and smoking. Lot of the land use is mixed (commercial and residential). As a part of the downtown core, it has a medium chance of getting gentrified and redeveloped.",
            "risk": "Medium"
        },
        "KANATA LAKES": {
            "description": "Kanata Lakes- a cluster of suburban neighbourhoods, parks, greenspace, and golf courses to the west of downtown Ottawa. Kanata Lakes is already a high end neighborhood close to many commercial centers and large tech companies. The chance of major gentrification is low.",
            "risk": "Low"
        },
        "MERIVALE ROAD": {
            "description": "Merivale Road, a significant road in Ottawa connecting schools, housing, restaurants, shops and malls all in one road. It includes many transport links. Going further down the road, there is an industrial park as well as a farm. Considering this, Merivale Road will not be going through gentrification anytime soon. However it is a possibility later on.",
            "risk": "Low-Medium"
        },
        "BEAVERBROOK": {
            "description": "Beaverbrook is another small cluster of neighborhoods to the right of Kanata Lakes. It is an older religion than Kanata Lakes and has low income and Co-Op housing. Due to this fact, the area may be redeveloped in the future. The chance of redevelopment and gentrification is high.",
            "risk": "High"
        },
        "LANSDOWNE": {
            "description": "Lansdowne- located in the very core of Ottawa downtown, it is a very popular area for visitors. Home to Lansdowne Park which is a world-class attraction with modern services combined with heritage sites. The land value is already high. Any gentrification in the future is very low.",
            "risk": "Very Low"
        }
    }
    
    # Create tabs for locations
    tabs = st.tabs(list(locations.keys()))
    
    for i, (location_name, location_data) in enumerate(locations.items()):
        with tabs[i]:
            risk_color = {
                "Very Low": "#10B981",  # Green
                "Low": "#34D399",  # Light Green
                "Low-Medium": "#FBBF24",  # Yellow
                "Medium": "#F59E0B",  # Orange
                "High": "#DC2626"  # Red
            }
            
            st.markdown(f"""
            <div style='padding: 20px; background-color: #f8fafc; border-radius: 10px; border-left: 5px solid {risk_color.get(location_data["risk"], "#6B7280")}'>
                <h3 style='margin-top: 0;'>{location_name}</h3>
                <p>{location_data["description"]}</p>
                <p><strong>Gentrification Risk: <span style='color: {risk_color.get(location_data["risk"], "#6B7280")}'>{location_data["risk"]}</span></strong></p>
            </div>
            """, unsafe_allow_html=True)
    
    # Coming soon section
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### More Locations Coming Soon")
    st.markdown("""
    We're continuously expanding our database to include more locations and more detailed 
    risk assessments. Check back later for updates!
    
    If you'd like to suggest a location for us to analyze, please use the Contact Us feature.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

def render_source():
    st.markdown('<div class="main-header">Sources & References</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Academic & Media Sources")
    
    sources = [
        "Duncan, Pamela, et al. 'Housing: how 14 years of Tory rule have changed Britain – in charts'. The Guardian, 1 July 2024, https://www.theguardian.com/politics/article/2024/jul/01/housing-how-14-years-of-tory-rule-have-changed-britain-in-charts?utm_source. Accessed 23 April 2025.",
        "REtripster, et al. What Is 'Gentrification?' YouTube, 16 June 2020, youtu.be/s07D45uHmVY?si=ZcSF7GEybjK4PyEK. Accessed 23 April 23, 2025.",
        "Wheatle, Alex et al. 'Alex Wheatle on the gentrification of Brixton'YouTube, 6 August 2013,https://youtu.be/D4by4BEPwAw?si=aLZqMWdRJoc5kPBi. Accessed 23, 2025.",
        "Kane, Laura. 'Vancouver's vision for Downtown Eastside stokes anti-gentrification protests.' Toronto Star, 25 May 2013, https://www.thestar.com/news/canada/vancouver-s-vision-for-downtown-eastside-stokes-anti-gentrification-protests/article_16a77469-5d37-5b4c-b61f-9a9a68b0a95a.html. Accessed 23 April 2025.",
        "Dorazio, Justin. 'Ways To Combat the Effects of Gentrification and Lack of Affordable Housing' American Progress, 26 September 2022, https://www.americanprogress.org/article/localized-anti-displacement-policies/?utm_source. Accessed 23 April 2025",
        "Sutton, Stacey. 'What we don't understand about gentrification' YouTube https://youtu.be/XqogaDX48nI?si=vSh34frFnoAfaa3Y. Accessed 23 April 2025",
        "Canada, Housing Federation. 'About Co-op Housing About Co-op Housing.' CHF Canada, https://chfcanada.coop/about-co-op-housing/. Accessed 23 April 2025."
    ]
    
    for i, source in enumerate(sources):
        st.markdown(f'<div class="source-item">{i+1}. {source}</div>', unsafe_allow_html=True)
    
    # Additional resources section
    st.markdown("### Additional Resources")
    st.markdown("""
    Looking for more information on gentrification and affordable housing solutions? 
    Check out these additional resources:
    
    - Local community organizations working on housing justice
    - Government policies and initiatives related to affordable housing
    - Academic research on the socioeconomic impacts of gentrification
    - Community-led solutions and success stories
    """)
    st.markdown('</div>', unsafe_allow_html=True)

def render_close():
    st.markdown('<div class="main-header">Thank You for Using the Gentrification Awareness App</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("""
    ### We hope you found this app informative and educational!
    
    Thanks for taking the time to learn about gentrification and its impacts on communities.
    
    Remember, awareness is the first step toward creating positive change in our communities.
    
    Would you like to:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Return to Home Page"):
            navigate_to('HOME')
            st.rerun()
    
    with col2:
        if st.button("Exit Application"):
            st.markdown("Closing application... Thank you for using the Gentrification Awareness App!")
            st.balloons()
    st.markdown('</div>', unsafe_allow_html=True)

# Main page selector
if st.session_state.page == 'HOME':
    render_home()
elif st.session_state.page == 'LEARN':
    render_learn()
elif st.session_state.page == 'PLAY':
    render_play()
elif st.session_state.page == 'DONATE':
    render_donate()
elif st.session_state.page == 'CHECK':
    render_check()
elif st.session_state.page == 'SOURCE':
    render_source()
elif st.session_state.page == 'CLOSE':
    render_close()
