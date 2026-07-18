.PHONY: load validate dashboard test check clean install freeze

install:
	pip install -r requirements.txt

load:
	python -m src.etl.load_all

validate:
	python -m src.etl.validator

dashboard:
	streamlit run src/dashboard/app.py

test:
	pytest -v

check:
	python -m src.etl.check_db

freeze:
	pip freeze > requirements.txt

clean:
	rm -f output/*.csv
	rm -f reports/*.xlsx