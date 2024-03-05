# CRUD

A simple, extendable CRUD interface that abstracts the backend storage system.

Supports:

- RAM storage
- Local filesystem storage
- Amazon S3 storage
- Google Cloud Storage (planned)

## Quickstart

Clone the repository and set the current working directory to the root of the repository:

```shell
git clone https://github.com/FreddyWordingham/CRUD.git
cd CRUD
```

Install the required dependencies, and the package itself:

```shell
poetry env use python3.10
poetry install
```

Copy the example environment file and fill in the required details:

```shell
cp .env.example .env
open .env
```

You can then run the example scripts to see the CRUD interface in action!
