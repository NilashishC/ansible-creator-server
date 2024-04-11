# A RESTful service for ansible-creator

## Usage

```bash
podman run --name=ansible-creator-svc -d -p 5000:5000 ghcr.io/nilashishc/ansible-creator-service:latest
```

### Scaffolding an Ansible collection

```bash
curl 'localhost:5000/init?collection=testns.testorg' --request GET --output testns-testorg.tar
```

### Scaffolding an Ansible playbook project

```bash
curl 'localhost:5000/init?project=ansible-project&scm_org=ansible&scm_project=devops' --request GET --output ansible-devops-project.tar
```

Untar to get scaffolded contents:

```bash
tar -xvf </path/to/tar>
```

## Debugging

Log into the running container inspect the logs:

```bash
podman exec -it ansible-creator-svc /bin/bash
cat ansible-creator-svc-<utc timestamp>.log
cat ansible-creator.log
```
