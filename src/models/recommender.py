import pickle
from pathlib import Path

# Define paths relative to this file
BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"

class Recommender:
    def __init__(self):
        self.projects = pickle.load(open(PROCESSED_DATA_DIR / 'project_list.pkl', 'rb'))
        self.details = pickle.load(open(PROCESSED_DATA_DIR / 'details.pkl', 'rb'))
        self.similarity = pickle.load(open(PROCESSED_DATA_DIR / 'similarity.pkl', 'rb'))

    def get_project_list(self):
        return self.projects['project_name'].values

    def get_project_details(self, project_name):
        return self.details[self.details['project_name'] == project_name]

    def fetch_poster(self, project_id):
        # Replace with logic to fetch poster based on project_id (if available)
        full_path = "https://t4.ftcdn.net/jpg/05/55/33/01/240_F_555330189_cKKtlJA502lcdqXveULFTcL5Rgg5F0JA.jpg"
        return full_path

    def extract_budget(self, budget_str):
        # Convert the budget to string
        budget_str = str(budget_str)
        # Extract numeric part from the string
        numeric_budget = ''.join(filter(str.isdigit, budget_str))
        return numeric_budget

    def recommend(self, project_name):
        index = self.projects[self.projects['project_name'] == project_name].index
        if len(index) == 0:
            return [], "Selected project not found."

        index = index[0]
        distances = sorted(list(enumerate(self.similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_projects = []
        warning_msg = None
        
        for i in distances[1:6]:
            project_id = self.projects.iloc[i[0]].project_id
            project_data = self.details[self.details['project_id'] == project_id]
            funding_goal_column = 'funding_goal(millions_USD)'
            
            if funding_goal_column not in project_data.columns:
                warning_msg = f"Column '{funding_goal_column}' not found in project data. Available columns: {', '.join(project_data.columns)}"
                continue
            
            project_details = {
                'name': project_data['project_name'].values[0],
                'poster': self.fetch_poster(project_id),
                'description': project_data['description'].values[0],
                'type': project_data['project_type'].values[0],
                'industry': project_data['Industry'].values[0],
                'environment': project_data['environment'].values[0],
                'social': project_data['social'].values[0],
                'location': project_data['location'].values[0],
                'budget': self.extract_budget(project_data[funding_goal_column].values[0])
            }
            recommended_projects.append(project_details)

        return recommended_projects, warning_msg
