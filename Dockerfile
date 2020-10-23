FROM python:3.8

RUN mkdir -p /srv/pansen
COPY . /srv/pansen/
WORKDIR /srv/pansen
RUN make bootstrap build

# Ensure we can call our own scripts without any prefix
ENV PATH=/srv/pansen/.venv/bin:$PATH

EXPOSE 8000
ENTRYPOINT [ "pansen_castlabs" ]

