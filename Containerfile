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
# OpenShift will by default run containers as a non root user where group is root.
# Make sure things are writeable by the root group.
RUN chmod -R 775 /app && chmod -R g+rwx /app && chgrp -R root /app

COPY . /app
RUN python3 -m pip install -r requirements.txt


CMD ["flask", "--app=app", "run", "--debug", "--host=0.0.0.0"]
