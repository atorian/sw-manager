
# Install all the libs locally
install:
	pipenv install --three --dev

serve:
	@echo "not implemented yet"
	#@pipenv run python ./serve.py

clean:
	mkdir -p ./build/
	rm -rf ./build/*

run:
	python ./src/optimize.py

test:
	PYTHONPATH=src pytest

.PHONY: build
