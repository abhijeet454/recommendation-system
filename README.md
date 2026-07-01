# Sustainable Project Recommendation Engine

A content-based recommendation system that suggests projects based on descriptions, industries, environmental impacts, and other factors. Built with Python, Scikit-Learn, and Streamlit.

## Project Structure

This project follows a clean architecture layout:

```text
Sustainable-Project-Recommendation-Engine/
├── data/
│   ├── processed/          # Serialized models and processed data (.pkl)
│   └── raw/                # Raw datasets (e.g., projects2.csv)
├── notebooks/              # Jupyter notebooks for exploration
├── src/
│   ├── app/                # Streamlit web application
│   │   └── main.py
│   ├── data_processing/    # Scripts for processing data and training
│   │   └── train_model.py
│   └── models/             # Core recommendation logic
│       └── recommender.py
├── requirements.txt        # Python dependencies
└── README.md
```

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd Sustainable-Project-Recommendation-Engine
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit application:**
   ```bash
   streamlit run src/app/main.py
   ```

## Model Training

To retrain the model on new data, ensure that `projects2.csv` is placed in the `data/raw/` directory (or root directory), and run the training script:

```bash
python src/data_processing/train_model.py
```
This will generate updated `.pkl` files in `data/processed/`.
