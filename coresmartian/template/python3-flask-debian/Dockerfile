FROM ghcr.io/openfaas/of-watchdog:0.9.6 as watchdog
FROM python:3.8-slim-buster

COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
RUN chmod +x /usr/bin/fwatchdog

ARG ADDITIONAL_PACKAGE
# Alternatively use ADD https:// (which will not be cached by Docker builder)

RUN apt-get -qy update && apt-get -qy install gcc python3-dev libpq-dev software-properties-common libssl-dev vim make ${ADDITIONAL_PACKAGE}
RUN add-apt-repository ppa:ethereum/ethereum
# Add non root user
RUN addgroup --system app && adduser app --system --ingroup app
RUN chown app /home/app

USER app

ENV PATH=$PATH:/home/app/.local/bin

WORKDIR /home/app/

COPY index.py           .
COPY requirements.txt   .

USER root
RUN pip install -r requirements.txt

# Build the function directory and install any user-specified components
USER app

RUN mkdir -p function && mkdir -p .mythril
RUN touch ./function/__init__.py
WORKDIR /home/app/function/
COPY function/requirements.txt	.
RUN pip install --user -r requirements.txt
#install function code
USER root

COPY function/   .
RUN chown -R app:app ../

ARG TEST_COMMAND=tox
ARG TEST_ENABLED=true
RUN [ "$TEST_ENABLED" = "false" ] && echo "skipping tests" || eval "$TEST_COMMAND"

WORKDIR /home/app/

#configure WSGI server and healthcheck
USER app

ENV fprocess="python index.py"

ENV cgi_headers="true"
ENV mode="http"
ENV upstream_url="http://127.0.0.1:5000"

HEALTHCHECK --interval=5s CMD [ -e /tmp/.lock ] || exit 1
RUN solc-select install 0.5.16
RUN solc-select install 0.6.11
RUN solc-select install 0.7.6
RUN solc-select install 0.8.16
RUN solc-select use 0.8.16
CMD ["fwatchdog"]
