FROM python:3.12-bullseye as builder

RUN pip install poetry==1.7.1

# poetry 가상환경 생성 활성화 -> 기존 환경과 최대한 분리
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN touch README.md

# 코드 복사 전 의존성 미리 설치, 캐싱
RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --no-root

FROM python:3.12-slim-bullseye as runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

# builder에서 구성한 가상환경(의존성 설치됨)과 코드만 복사 -> 수정 빈도 순으로 복사 순서 내림차순 정렬
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY config.py main.py ./
COPY util ./util
COPY core ./core

# poetry가 아닌 uvicorn으로 앱 실행
ENTRYPOINT ["uvicorn", "main:app"]
