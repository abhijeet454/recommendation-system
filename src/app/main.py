import sys
from pathlib import Path
import streamlit as st

# Setup page configuration
st.set_page_config(
    page_title="EcoInvest | Sustainable Projects",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add the project root to sys.path to allow importing from src
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))

from src.models.recommender import Recommender

@st.cache_resource
def get_recommender():
    return Recommender()

def main():
    # --- Custom CSS ---
    st.markdown("""
        <style>
        .stButton>button {
            width: 100%;
            border-radius: 5px;
            height: 3em;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # --- Sidebar ---
    with st.sidebar:
        st.title("🌱 EcoInvest")
        st.markdown("""
        **Discover your next sustainable investment.**
        
        This engine recommends high-impact projects based on your preferences and previous selections. 
        It analyzes industry, environmental impact, and social benefits.
        """)
        st.markdown("---")
        st.caption("Powered by Advanced Machine Learning")
        st.caption("© 2026 EcoInvest Inc.")
        
    # --- Main Content ---
    st.title('Sustainable Project Recommendation Engine')
    st.markdown("Find the perfect eco-friendly projects to fund and make a positive impact on the world.")
    st.markdown("---")
    
    try:
        with st.spinner("Loading Recommendation Engine..."):
            recommender = get_recommender()
    except FileNotFoundError:
        st.error("⚠️ Model files not found. Please ensure that models are trained and present in data/processed/")
        return

    project_list = recommender.get_project_list()
    
    # Layout for selection
    col1, col2 = st.columns([3, 1])
    with col1:
        selected_project = st.selectbox(
            "🔍 Search or select a project you are interested in:",
            project_list,
            index=0
        )
    
    with col2:
        st.write("") # Spacing
        st.write("")
        show_btn = st.button('🚀 Get Recommendations', type="primary")

    if show_btn:
        st.markdown("---")
        
        # Display selected project details
        selected_project_data = recommender.get_project_details(selected_project)
        
        if not selected_project_data.empty:
            st.subheader("📌 Selected Project Overview")
            # We can create a nice metrics layout for the selected project
            s_col1, s_col2, s_col3 = st.columns(3)
            with s_col1:
                industry = selected_project_data['Industry'].values[0] if 'Industry' in selected_project_data.columns else "N/A"
                st.metric(label="Industry", value=industry)
            with s_col2:
                p_type = selected_project_data['project_type'].values[0] if 'project_type' in selected_project_data.columns else "N/A"
                st.metric(label="Type", value=p_type)
            with s_col3:
                budget = "N/A"
                if 'funding_goal(millions_USD)' in selected_project_data.columns:
                    budget = f"${selected_project_data['funding_goal(millions_USD)'].values[0]}M"
                st.metric(label="Funding Goal", value=budget)
            
            with st.expander("View Full Details", expanded=False):
                for col in selected_project_data.columns:
                    if col not in ['funding_goal(millions_USD)', 'tags', 'project_name']:
                        val = selected_project_data[col].values[0]
                        st.markdown(f"**{col.replace('_', ' ').title()}:** {val}")
                        
        st.markdown("---")
        
        # Fetch recommendations
        with st.spinner("Finding similar projects..."):
            recommended_projects, warning = recommender.recommend(selected_project)
        
        if warning:
            st.warning(warning)
            
        if recommended_projects:
            st.subheader("🌟 Top Recommended Investments")
            st.markdown("Based on your selection, here are other projects you might be interested in:")
            
            # Use columns to create a grid (e.g., 3 columns)
            cols = st.columns(3)
            
            for index, project in enumerate(recommended_projects):
                # Distribute projects across columns
                col_idx = index % 3
                with cols[col_idx]:
                    st.markdown(f"#### {project['name']}")
                    st.image(project['poster'], use_column_width=True)
                    
                    st.markdown(f"**{project['industry']}** | **{project['type']}**")
                    
                    desc = project['description']
                    if len(desc) > 150:
                        desc = desc[:147] + "..."
                    st.markdown(f"*{desc}*")
                    
                    st.caption(f"📍 **Location:** {project['location']}")
                    st.caption(f"🌍 **Environment:** {project['environment']}")
                    st.caption(f"🤝 **Social:** {project['social']}")
                    st.caption(f"💰 **Budget:** ${project['budget']}M")
                    st.markdown("---")
        elif not warning:
            st.info("No similar recommendations found at this time.")

if __name__ == "__main__":
    main()
