import pickle
import streamlit as st

def fetch_poster(project_id):
    # Replace with logic to fetch poster based on project_id (if available)
    full_path = "https://t4.ftcdn.net/jpg/05/55/33/01/240_F_555330189_cKKtlJA502lcdqXveULFTcL5Rgg5F0JA.jpg"
    return full_path

def extract_budget(budget_str):
    # Convert the budget to string
    budget_str = str(budget_str)
    # Extract numeric part from the string
    numeric_budget = ''.join(filter(str.isdigit, budget_str))
    return numeric_budget

def recommend(project):
    index = projects[projects['project_name'] == project].index
    if len(index) == 0:
        st.error("Selected project not found.")
        return [], []

    index = index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_projects = []
    for i in distances[1:6]:
        # fetch the project details
        project_id = projects.iloc[i[0]].project_id
        project_data = details[details['project_id'] == project_id]
        funding_goal_column = 'funding_goal(millions_USD)'
        if funding_goal_column not in project_data.columns:
            st.warning(f"Column '{funding_goal_column}' not found in project data. Available columns: {', '.join(project_data.columns)}")
            continue
        project_details = {
            'name': project_data['project_name'].values[0],
            'poster': fetch_poster(project_id),
            'description': project_data['description'].values[0],
            'type': project_data['project_type'].values[0],
            'industry': project_data['Industry'].values[0],
            'environment': project_data['environment'].values[0],
            'social': project_data['social'].values[0],
            'location': project_data['location'].values[0],
            'budget': extract_budget(project_data[funding_goal_column].values[0])
        }
        recommended_projects.append(project_details)

    return recommended_projects

st.header('Project Recommender System')
projects = pickle.load(open('project_list.pkl', 'rb'))
details = pickle.load(open('details.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

project_list = projects['project_name'].values
selected_project = st.selectbox(
    "Type or select project from the dropdown",
    project_list
)


if st.button('Show Details'):
    recommended_projects = recommend(selected_project)

    # Display details of selected project
    selected_project_data = details[details['project_name'] == selected_project]
    st.subheader("Selected Project Details:")
    for col in selected_project_data.columns:
        if col != 'funding_goal(millions_USD)' and col != 'tags':
            st.write(f"**{col}:** {selected_project_data[col].values[0]}")
    st.subheader("More Recommended Investements")
    # Display recommendations
    for project in recommended_projects:
        st.subheader(project['name'])
        st.image(project['poster'])
        st.write(f"**Description:** {project['description']}")
        st.write(f"**Project Type:** {project['type']}")
        st.write(f"**Industry:** {project['industry']}")
        st.write(f"**Environment:** {project['environment']}")
        st.write(f"**Social:** {project['social']}")
        st.write(f"**Location:** {project['location']}")
        st.write(f"**Project Budget (Millions):** {project['budget']}")
