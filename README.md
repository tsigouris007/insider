# A rewritten insider Dockerfile

This clones and builds https://github.com/insidersec/insider

## Why?

Because the default docker image does not give any output files to the user.

## How?

### Build

```bash
docker build . -t insider:3.0.0 # or whatever you wanna call it
```

### Run

It is preferable to mount the `/data` folder as shown with your current project's folder in order to receive a proper `report.insider.json` file as an output.

```bash
docker run --rm -v $(pwd):/data insider:3.0.0 -tech <android|java|ios|javascript|csharp> -target /data/<your_folder>
```

This will copy the two report files to your mounted folder. \
Runs as root. Felt cute might fix it later.
