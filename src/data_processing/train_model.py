import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
RAW_DATA_DIR = DATA_DIR / "raw"

# Ensure processed data directory exists
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

def collapse(L):
    return [i.replace(" ", "") for i in L]

def preprocess_tags(tags):
    processed_tags = []
    for tag in tags:
        processed_tags.append(tag.lower().strip())
    return processed_tags

def train_recommender():
    data_path = RAW_DATA_DIR / "projects2.csv"
    if not data_path.exists():
        # Fallback to current directory for projects2.csv to maintain backwards compatibility 
        # just in case it's placed in the root directory.
        data_path = BASE_DIR / "projects2.csv"
        if not data_path.exists():
            print(f"Error: Dataset not found at {data_path}. Please place 'projects2.csv' in the data/raw/ directory.")
            return

    project = pd.read_csv(data_path)
    
    project = project[["project_id", "project_name", "description", "project_type", 
                       "Industry", "location", "environment", "social", "funding_goal(millions_USD)"]]

    project['location'] = collapse(project['location'])
    project['project_type'] = collapse(project['project_type'])
    project['Industry'] = collapse(project['Industry'])
    
    project['tags'] = (project["description"] + " " + project['project_type'] + " " + 
                       project['Industry'] + " " + project["environment"] + " " + 
                       project["social"] + " " + project['location'] + " " + 
                       project['funding_goal(millions_USD)'].astype(str))
    
    new = project.drop(columns=["description", "project_type", "Industry", 
                                "environment", "social", "location", "funding_goal(millions_USD)"])
    
    vectorizer = TfidfVectorizer(max_features=50000, stop_words='english')
    processed_tags = preprocess_tags(new['tags'])
    vector = vectorizer.fit_transform(processed_tags).toarray()
    
    similarity = cosine_similarity(vector)
    
    print("Saving models to:", PROCESSED_DATA_DIR)
    with open(PROCESSED_DATA_DIR / 'project_list.pkl', 'wb') as f:
        pickle.dump(new, f)
    with open(PROCESSED_DATA_DIR / 'similarity.pkl', 'wb') as f:
        pickle.dump(similarity, f)
    with open(PROCESSED_DATA_DIR / 'details.pkl', 'wb') as f:
        pickle.dump(project, f)
    print("Models saved successfully.")

if __name__ == "__main__":
    train_recommender()
