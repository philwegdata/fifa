import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load the preprocessed CSV file with average overall scores
average_data = pd.read_csv('average_overall_by_club.csv')

# Load the precomputed top 5 players CSV file based on club names
top_5_data = pd.read_csv('top_5_players_by_club_and_version.csv')

# Get the unique club names for selection
club_names = average_data['club_name'].unique()

# Allow the user to select one or more clubs
selected_club_names = st.multiselect('Select Clubs to Compare:', club_names)

# ... (Previous parts of the Streamlit and Plotly code)

# Customize appearance
fig = go.Figure()

# Add traces for each selected club
for idx, club in enumerate(selected_club_names):
    club_data = average_data[average_data['club_name'] == club]
    fig.add_trace(go.Scatter(x=club_data['fifa_version'], y=club_data['overall'],
                             mode='lines+markers',
                             name=club,
                             hoverinfo='x+y+text',
                             hovertemplate=
                             "FIFA Version: %{x}<br>" +
                             "Average Overall: %{y}",
                             marker=dict(size=10)))

# Customize appearance
fig.update_layout(
    title='Comparison of Average "Overall" Rating by FIFA Version',
    hovermode="closest",
    xaxis_title="FIFA Version",
    yaxis_title="Average Overall Rating",
    font=dict(
        family="Courier New, monospace",
        size=14,
        color="RebeccaPurple"
    )
)

# Display the Plotly plot in Streamlit
st.plotly_chart(fig)


st.write("Expand to check the best players by year:")
# ... (Previous Streamlit code for plotting)

# Display collapsible tables for top 5 players of each selected club for each FIFA version
for club in selected_club_names:
    with st.expander(f"Top 5 players for {club} by FIFA version", expanded=False):
        club_data = top_5_data[top_5_data['club_name'] == club]

        for version in club_data['fifa_version'].unique():
            st.write(f"#### FIFA Version: {version}")
            version_data = club_data[club_data['fifa_version'] == version]

            # Create a header row with adjusted column widths
            cols = st.columns([1, 1.5, 1, 1])
            cols[0].write("Face")
            cols[1].write("Short Name")
            cols[2].write("Positions")
            cols[3].write("Overall")


            # Populate rows with player data and their faces
            for _, row in version_data.iterrows():
                cols = st.columns([1, 1.5, 1, 1])
                cols[0].image(row['player_face_url'], caption='', width=60)
                cols[1].write(row['short_name'])
                cols[2].write(row['player_positions'])
                cols[3].write(row['overall'])
