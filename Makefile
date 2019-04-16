.PHONY: test test-cov

test:
	PYTHONPATH=. pytest test -s

test-cov:
	PYTHONPATH=. pytest test --cov=traffic_light --cov-report term-missing
