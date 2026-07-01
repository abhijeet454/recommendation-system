import sys
from pathlib import Path
import streamlit as st

# Add the project root to sys.path to allow importing from src
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))

from src.models.recommender import Recommender

@st.cache_resource
def get_recommender():
    return Recommender()

def main():
    st.header('Sustainable Project Recommendation Engine')
    
    try:
        recommender = get_recommender()
    except FileNotFoundError:
        st.error("Model files not found. Please ensure that models are trained and present in data/processed/")
        return

    project_list = recommender.get_project_list()
    selected_project = st.selectbox(
        "Type or select project from the dropdown",
        project_list
    )

    if st.button('Show Details'):
        recommended_projects, warning = recommender.recommend(selected_project)
        
        if warning:
            st.warning(warning)

        # Display details of selected project
        selected_project_data = recommender.get_project_details(selected_project)
        if not selected_project_data.empty:
            st.subheader("Selected Project Details:")
            for col in selected_project_data.columns:
                if col not in ['funding_goal(millions_USD)', 'tags']:
                    st.write(f"**{col}:** {selected_project_data[col].values[0]}")
        
        if recommended_projects:
            st.subheader("More Recommended Investments")
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
        elif not warning:
            st.error("No recommendations found.")

if __name__ == "__main__":
    main()
