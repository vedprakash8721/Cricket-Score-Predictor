import streamlit as st
import pickle
import pandas as pd
import os

# ----------------- Data -----------------
teams = ['Sunrisers Hyderabad','Mumbai Indians','Royal Challengers Bangalore',
         'Kolkata Knight Riders','Kings XI Punjab','Chennai Super Kings',
         'Rajasthan Royals','Delhi Capitals']

cities = ['Hyderabad','Bangalore','Mumbai','Indore','Kolkata','Delhi',
          'Chandigarh','Jaipur','Chennai','Cape Town','Port Elizabeth',
          'Durban','Centurion','East London','Johannesburg','Kimberley',
          'Bloemfontein','Ahmedabad','Cuttack','Nagpur','Dharamsala',
          'Visakhapatnam','Pune','Raipur','Ranchi','Abu Dhabi',
          'Sharjah','Mohali','Bengaluru']

# ----------------- Load Model -----------------

# Get the directory of the current file (app.py)
BASE_DIR = os.path.dirname(__file__)
pipe_path = os.path.join(BASE_DIR, 'pipe.pkl')

# Load the pickle model
pipe = pickle.load(open(pipe_path, 'rb'))



# ----------------- Page Config -----------------
st.set_page_config(
    page_title="IPL Win Predictor",
    page_icon="🏏",
    layout="wide"
)

st.title("🏏 IPL Win Probability Predictor")
st.markdown("Predict the chance of winning for batting and bowling teams dynamically!")

# ----------------- Inputs in Sidebar -----------------
st.sidebar.header("Match Details")
batting_team = st.sidebar.selectbox("Select Batting Team", teams)
bowling_team = st.sidebar.selectbox("Select Bowling Team", teams)
venue = st.sidebar.selectbox("Select Venue", cities)
target = st.sidebar.number_input("Target Score", min_value=0, value=150)
current_score = st.sidebar.number_input("Current Score", min_value=0, value=50)
overs = st.sidebar.number_input("Overs Completed", min_value=0, max_value=20, value=10)
wickets_out = st.sidebar.number_input("Wickets Lost", min_value=0, max_value=10, value=2)

# ----------------- Prediction -----------------
if st.sidebar.button("Predict Win Probability"):
    runs_left = target - current_score
    balls_left = 120 - (overs * 6)
    wickets_left = 10 - wickets_out
    current_rr = current_score / overs if overs > 0 else 0
    required_rr = (runs_left * 6) / balls_left if balls_left > 0 else 0

    input_df = pd.DataFrame({
        'batting_team':[batting_team],
        'bowling_team':[bowling_team],
        'city':[venue],
        'runs_left':[runs_left],
        'balls_left':[balls_left],
        'wickets_left':[wickets_left],
        'total_runs_x':[target],
        'current_score':[current_score],
        'current_rr':[current_rr],
        'required_rr':[required_rr]
    })

    result = pipe.predict_proba(input_df)
    loss = result[0][0]*100
    win = result[0][1]*100

    # ----------------- Display Results Side by Side -----------------
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"<h3 style='color:green'>{batting_team}: {round(win,1)}%</h3>", unsafe_allow_html=True)
        st.progress(int(win))
    with col2:
        st.markdown(f"<h3 style='color:red'>{bowling_team}: {round(loss,1)}%</h3>", unsafe_allow_html=True)
        st.progress(int(loss))

    st.markdown("---")
    st.markdown("**Match Summary:**")
    st.write(f"Target: {target} | Current Score: {current_score} | Overs: {overs} | Wickets Lost: {wickets_out}")
    st.write(f"Runs left: {runs_left} | Balls left: {balls_left} | Wickets left: {wickets_left}")
    st.write(f"Current Run Rate: {round(current_rr,2)} | Required Run Rate: {round(required_rr,2)}")

# ----------------- Footer -----------------
st.markdown("""
<div style='text-align: center; color: grey; margin-top: 60px;'>
Developed by Abhishek Kushwaha | IPL Win Predictor Project
</div>
""", unsafe_allow_html=True)
