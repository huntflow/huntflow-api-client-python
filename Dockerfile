FROM python:3.10.9-slim

WORKDIR /app

COPY . .
RUN pip install --upgrade pip
RUN pip install PyGithub pyproject_parser

CMD ["python", "auto_release.py", "--github_token", "2", "--current_branch", "v3"]

