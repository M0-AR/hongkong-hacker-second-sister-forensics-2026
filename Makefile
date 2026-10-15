.PHONY: all exp01 exp02 exp03 exp04 test clean
all: exp01 exp02 exp03 exp04 test
exp01:
	python3 experiments/01_tradecraft_verification.py
exp02:
	python3 experiments/02_cyberbullying_benchmark.py
exp03:
	python3 experiments/03_hidden_patterns.py
exp04:
	python3 experiments/04_live_anchor.py
test:
	pytest -q
clean:
	rm -rf results/*.json __pycache__ .pytest_cache
