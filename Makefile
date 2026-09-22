install:
	pip install -r requirements.txt
test:
	pytest -q
eval:
	python -m evals.run_evals
mcp:
	python -m mcp_server.server
demo:
	streamlit run app.py
