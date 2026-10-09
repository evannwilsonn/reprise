.PHONY: setup extract simulate test load build dashboard serve all
all: extract simulate test load build dashboard   ## everything, on DuckDB (~2 minutes)
setup:      ## install dependencies
	pip install -r requirements.txt
extract:    ## download the Mooncake traces and check them against the published request counts
	python ingest/extract.py
simulate:   ## replay every trace x policy x cluster scenario (126 simulations)
	python sim/simulate.py
test:       ## unit tests for the tier cache
	python -m pytest -q sim/tests
load:       ## land traces and simulator output in DuckDB (hash-checked)
	python ingest/load_raw.py
build:      ## seed, run and test every dbt model
	dbt build --profiles-dir .
dashboard:  ## export the reporting marts for the dashboard
	python dashboard/export_data.py
serve:      ## open the dashboard at http://localhost:8000
	cd dashboard && python -m http.server 8000
