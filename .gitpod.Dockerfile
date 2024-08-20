FROM gitpod/workspace-full

RUN pyenv install 3.10.12 \
    && pip install --upgrade pip