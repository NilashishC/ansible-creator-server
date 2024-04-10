FROM quay.io/fedora/fedora-minimal:39

USER root

RUN microdnf -y makecache && microdnf -y update && microdnf install -y \
tar \
echo \
python3-devel \
which \
gcc \
git-core \
python3-markupsafe \
python3-bcrypt \
python3-cffi \
python3-pip \
python3-pyyaml \
python3-ruamel-yaml \
python3-wheel \
    && microdnf clean all

COPY ./requirements.txt /tmp/requirements.txt
RUN python3 -m pip install -r /tmp/requirements.txt

EXPOSE 5000

WORKDIR /app
COPY ./main.py /app/main.py

ENV FLASK_APP=main.py

CMD ["flask", "run", "--host=0.0.0.0"]