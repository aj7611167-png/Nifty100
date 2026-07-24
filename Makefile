.PHONY: install load validate api dashboard test check freeze clean lint

# Install project dependencies
install:
	pip install -r requirements.txt

# Load all datasets into SQLite
load:
	python -m src.etl.load_all

# Run data validation
validate:
	python -m src.etl.validator

# Check database integrity
check:
	python -m src.etl.check_db

# Start the FastAPI server
api:
	uvicorn src.api.main:app --reload

# Launch the Streamlit dashboard
dashboard:
	streamlit run src/dashboard/app.py

# Run all tests
test:
	pytest -v

# Optional: Run linting (if flake8 is installed)
lint:
	flake8 src tests

# Update requirements.txt
freeze:
	pip freeze > requirements.txt

# Remove generated output files
clean:
	rm -f output/*.csv
	rm -f output/*.json
	rm -f reports/*.xlsx
	rm -f reports/*.html
	rm -f reports/*.pdf
	rm -f reports/*.png
	rm -rf .pytest_cache
	rm -rf __pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete