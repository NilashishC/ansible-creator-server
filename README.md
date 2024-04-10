# A RESTful service for ansible-creator

## Usage

Pull the container image for this service:

```bash
docker pull ghcr.io/nilashishc/ansible-creator-svc:latest
```

Start the container:

```bash
docker run -d -p 5000:5000 ghcr.io/nilashishc/ansible-creator-svc:latest
```

Send request to the service to return a scaffolded collection as a tarball:

```bash
curl localhost:5000/init --request GET --data '{"collection": "testns.testorg"}' --header "Content-Type: application/json" --output testns-testorg.tar
```

Untar to get collection contents:

```bash
tar -xvf testns-testorg.tar
```
