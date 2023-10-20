build-flake8:
	docker build -t gpt_kw_team-flake8:latest -f Dockerfile.flake8 .

flake8: build-flake8
	docker run -ti --rm -v $(shell pwd):/app:ro gpt_kw_team-flake8 */**.py
