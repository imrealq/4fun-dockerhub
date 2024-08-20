FROM gitpod/workspace-full

RUN pyenv install -f 3.10.12

RUN pip install --upgrade pip
