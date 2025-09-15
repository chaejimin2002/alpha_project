FROM python:3.12-slim

# 타임존(알파카는 서버시간 UTC, 표시는 선택)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Poetry 설치
RUN pip install poetry

# Poetry 설정
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VENV_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

# Poetry 파일들 복사 및 의존성 설치
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev && rm -rf $POETRY_CACHE_DIR

# 앱 코드 복사
COPY . .

# Poetry 가상환경에서 실행
CMD ["poetry", "run", "python", "app/bot.py"]