# Docker image for cSMTiser

## Usage

### 1. Clone cSMTiser repository:
```console
$ cd ~
$ git clone https://github.com/clarinsi/csmtiser.git
```

### 2. Copy and adjust config. Use values of variables `working_dir`, `moses_scripts`, `kenlm`, `moses`, `mgiza` as they are in `docker/config.docker.yml`:
```console
$ cp ~/csmtiser/docker/config.docker.yml ~/csmtiser/docker/config.yml
$ # adjust ~/csmtiser/docker/config.yml, e.g. num_cores variable
```

### 3. Run docker image `greegorey/csmtiser`, mounting your `~/csmtiser` directory into container:
```console
$ docker run -v ~/csmtiser:/csmtiser greegorey/csmtiser python preprocess.py
```

Proceed further with the main tutorial, just add `docker run -v ~/csmtiser:/csmtiser greegorey/csmtiser` every time before you run `python <COMMAND>`.
