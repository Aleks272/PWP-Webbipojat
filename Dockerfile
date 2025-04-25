FROM python:3.13.3-alpine3.21
# adapted from course material:
# https://lovelace.oulu.fi/ohjelmoitava-web/ohjelmoitava-web/exercise-3-api-documentation-and-hypermedia/#creating-images-from-dockerfiles
WORKDIR /opt/watchlists
COPY . .
RUN pip install -r requirements.txt
CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0", "project_watchlist:create_app()"]