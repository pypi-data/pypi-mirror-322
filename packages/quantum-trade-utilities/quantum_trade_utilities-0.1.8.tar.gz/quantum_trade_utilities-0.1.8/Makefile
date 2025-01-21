.PHONY: build publish test clean install-dev

clean:
	rm -rf dist/ build/ *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +

install-dev:
	uv pip install -e ".[test]"

test:
	pytest -v

coverage:
	pytest --cov=quantum_trade_utilities tests/

build:
	python -m build

publish:
	python -m twine upload dist/*