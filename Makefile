
install:
	pip install --upgrade build

build:
	python -m build

deploy:
	twine upload --repository testpypi dist/*
