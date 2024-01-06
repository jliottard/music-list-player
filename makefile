install:
	python3 -m venv .venv
	source .venv/bin/activate
	python3 -m pip install --upgrade pip
	pip install -r requirements.txt
run:
	.venv/bin/python main.py
close:
	deactivate