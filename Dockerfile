FROM python:3.5-alpine

RUN pip install --upgrade google-api-python-client requests
COPY cluster.py /cluster.py

# Expose volume for adding credentials
VOLUME ["/root/.config"]

# Expose directory to write output to, and to potentially read certs from
VOLUME ["/etc/sysconfig/", "/etc/certs"]
ENTRYPOINT python /cluster.py
