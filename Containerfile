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

EXPOSE 5000

WORKDIR /app
COPY . /app
RUN python3 -m pip install -r requirements.txt

CMD ["flask", "--app=app", "run", "--debug", "--host=0.0.0.0"]
