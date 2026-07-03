.PHONY: load validate test check clean

load:
	python -m src.etl.load_all

validate:
	python -m src.etl.validator

test:
	pytest -v

check:
	python -m src.etl.check_db

clean:
	rm -f output/*.csv