FROM quay.io/fedora/fedora-minimal:39

USER root

RUN microdnf -y makecache && microdnf -y update && microdnf install -y \
tar \
echo \
which \
gcc \
python3-devel \
python3-pip \
    && microdnf clean all

COPY ./requirements.txt /tmp/requirements.txt
RUN python3 -m pip install -r /tmp/requirements.txt

EXPOSE 5000

WORKDIR /app
COPY ./main.py /app/main.py

CMD ["python", "main.py"]
