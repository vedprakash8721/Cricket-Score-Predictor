import streamlit as st
import pickle
import pandas as pd
import numpy as np
import plotly.graph_objects as go

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

pipe = pickle.load(open("App/pipe.pkl", "rb"))

# ----------------- Page Config -----------------
st.set_page_config(
    page_title="IPL Win Predictor",
    page_icon="🏏",
    layout="wide"
)

# ----------------- Dark Background -----------------
st.markdown("""
    <style>
    .stApp {
        background-color: #0f111a;
        color: #f5f5f5;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #f5f5f5;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏏 IPL Win Probability Predictor")
st.markdown("Predict dynamic win chances for batting and bowling teams")

# ----------------- Input Sliders -----------------
st.sidebar.header("Match Setup")
batting_team = st.sidebar.selectbox("Batting Team", teams)
bowling_team = st.sidebar.selectbox("Bowling Team", teams)
venue = st.sidebar.selectbox("Venue", cities)
target = st.sidebar.slider("Target Score", 0, 300, 150)
current_score = st.sidebar.slider("Current Score", 0, target, 50)
overs = st.sidebar.slider("Overs Completed", 0, 20, 10)
wickets_out = st.sidebar.slider("Wickets Lost", 0, 10, 2)

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
    win = result[0][1]*100
    lose = result[0][0]*100

    # --------- Circular Progress Display ---------
    col1, col2 = st.columns(2)
    col1.markdown(f"<h2 style='text-align:center; color:#00ff7f'>{batting_team}<br>{win:.1f}%</h2>", unsafe_allow_html=True)
    col2.markdown(f"<h2 style='text-align:center; color:#ff4d4d'>{bowling_team}<br>{lose:.1f}%</h2>", unsafe_allow_html=True)

    # --------- Over-by-over simulated data for plot ---------
    overs_array = np.arange(1, overs+1)
    win_prob = np.clip(np.linspace(50, win, overs), 0, 100)
    lose_prob = np.clip(100 - win_prob, 0, 100)
    runs_per_over = np.random.randint(4, 20, size=overs)
    wickets_per_over = np.random.randint(0,2, size=overs)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=overs_array, y=win_prob, mode='lines+markers',
                             name='Win Probability', line=dict(color='#00ff7f', width=3),
                             hovertemplate="Over %{x}: Win %{y:.1f}%"))
    fig.add_trace(go.Scatter(x=overs_array, y=lose_prob, mode='lines+markers',
                             name='Lose Probability', line=dict(color='#ff4d4d', width=3),
                             hovertemplate="Over %{x}: Lose %{y:.1f}%"))
    fig.add_trace(go.Bar(x=overs_array, y=runs_per_over, name='Runs per Over', marker_color='#1f77b4', opacity=0.6,
                         hovertemplate="Over %{x}: Runs %{y}"))
    fig.add_trace(go.Bar(x=overs_array, y=wickets_per_over, name='Wickets per Over', marker_color='#ffd700', opacity=0.6,
                         hovertemplate="Over %{x}: Wickets %{y}"))

    fig.update_layout(barmode='overlay', xaxis_title='Overs', yaxis_title='Value',
                      template='plotly_dark', width=900, height=500,
                      legend=dict(font=dict(color="#f5f5f5")))
    st.plotly_chart(fig, use_container_width=True)

    # --------- Collapsible Match Summary ---------
    with st.expander("Match Summary"):
        st.markdown(f"<span style='color:#f5f5f5'>Target: {target} | Current Score: {current_score} | Overs: {overs} | Wickets Lost: {wickets_out}</span>", unsafe_allow_html=True)
        st.markdown(f"<span style='color:#f5f5f5'>Runs left: {runs_left} | Balls left: {balls_left} | Wickets left: {wickets_left}</span>", unsafe_allow_html=True)
        st.markdown(f"<span style='color:#f5f5f5'>Current Run Rate: {round(current_rr,2)} | Required Run Rate: {round(required_rr,2)}</span>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color: grey;'>Developed by Abhishek Kushwaha | IPL Win Predictor Project</p>", unsafe_allow_html=True)
