# A RESTful service for ansible-creator

## Usage

Pull the container image for this service:

```bash
podman pull ghcr.io/nilashishc/ansible-creator-svc:latest
```

Start the container:

```bash
podman run --name=ansible-creator-svc -d -p 5000:5000 ghcr.io/nilashishc/ansible-creator-svc:latest
```

### Scaffolding a collection

```bash
curl localhost:5000/init --request GET --data '{"collection": "testns.testorg"}' --header "Content-Type: application/json" --output testns-testorg.tar
```

### Scaffolding an Ansible playbook project

```bash
curl localhost:5000/init --request GET --data '{"scm_org": "ansible", "scm_project": "devops", "project": "ansible-project"}' --header "Content-Type: application/json" --output ansible-devops-project.tar
```

Untar to get collection contents:

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
