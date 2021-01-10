# Rubix Lora Raw

## Running in development

- Use [`poetry`](https://github.com/python-poetry/poetry) to manage dependencies
- Simple script to install

    ```bash
    ./setup.sh
    ```

- Join `venv`

    ```bash
    poetry shell
    ```

- Build local binary

    ```bash
    poetry run pyinstaller run.py -n rubix-lora --clean --onefile \
            --add-data VERSION:. \
            --add-data config:config \
            --hidden-import=src.utils.color_formatter
    ```

  The output is: `dist/rubix-lora`

## Docker build

### Build

```bash
./docker.sh
```

The output image is: `rubix-lora:dev`

### Run

```bash
docker volume create rubix-lora-data
docker run --rm -it -p 1919:1919 -v rubix-lora-data:/data --name rubix-lora rubix-lora:dev
```

## Deploy on Production

- Download release artifact
- Review help and start

```bash
$ rubix-lora -h
Usage: rubix-lora [OPTIONS]

Options:
  -p, --port INTEGER              Port  [default: 1919]
  -d, --data-dir PATH             Application data dir
  --prod                          Production mode
  -s, --setting-file TEXT         Rubix-Lora: setting ini file
  -l, --logging-conf TEXT         Rubix-Lora: logging config file
  --workers INTEGER               Gunicorn: The number of worker processes for handling requests.
  -c, --gunicorn-config TEXT      Gunicorn: config file(gunicorn.conf.py)
  --log-level [FATAL|ERROR|WARN|INFO|DEBUG]
                                  Logging level
  -h, --help                      Show this message and exit.
```
