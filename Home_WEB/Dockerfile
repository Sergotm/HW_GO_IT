# TODO FROM Задає базовий образ для наступних інструкцій
FROM python:3.12

# TODO ENV Встановлює змінну середовища
ENV APP_HOME /app

# TODO
WORKDIR $APP_HOME

# TODO
COPY pyproject.toml $APP_HOME/pyproject.toml
#COPY poetry.lock $APP_HOME/poetry.lock

# TODO
RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install --only main

# TODO
COPY . .

# TODO
EXPOSE 5000

# TODO
CMD ["python", "work.py"]
