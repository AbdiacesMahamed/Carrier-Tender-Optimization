# Streamlit Deployment Instructions

## Repository Structure

Your repository should have this structure:

```
your-repo-name/
├── dashboard.py                 # Main Streamlit app
├── requirements.txt            # Dependencies
├── README.md                  # Project description
├── components/                # Application modules
│   ├── __init__.py
│   ├── data_loader.py
│   ├── data_processor.py
│   ├── metrics.py
│   ├── optimization.py
│   └── ... (other modules)
└── .streamlit/                # Streamlit config (optional)
    └── config.toml
```

## Streamlit Cloud Deployment Settings

When deploying on Streamlit Community Cloud:

1. **Repository**: Select your GitHub repository
2. **Branch**: main (or your default branch)
3. **Main file path**: `dashboard.py`
4. **Python version**: 3.9+ (leave default)
5. **Advanced settings**: Leave blank (auto-detects requirements.txt)

## Important Notes

- Do NOT specify a requirements file path manually
- Streamlit will automatically find `requirements.txt` in the root
- Make sure all imports use relative paths (e.g., `from components.data_loader import ...`)
- Ensure your dashboard.py is in the repository root

## If you get "Optimization/requirements.txt" error:

This means either:

1. Your repo structure has an extra "Optimization" folder
2. There's a hardcoded path reference somewhere
3. The deployment settings have the wrong path

Fix by ensuring dashboard.py and requirements.txt are in the repository root.
