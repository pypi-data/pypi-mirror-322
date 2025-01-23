# f2r

Command line tool to create RPMs out of aliBuild output.

## Prerequisites
 - [aliBuild](https://alisw.github.io/alibuild/)
 - [environment Modules](https://modules.readthedocs.io/en/latest/) 4.3 or higher, RPM is available from [this S3 location](http://s3.cern.ch/swift/v1/system-configuration/RPMS/environment-modules-4.6.1-1.el7.cern.x86_64.rpm)
 - Optional: To enable S3 support you need to create a config file under `~/.s3cfg`, see [CERN IT instructions](https://clouddocs.web.cern.ch/object_store/s3cmd.html)
 - gem + fpm: `yum install rubygems -y ; gem install fpm`

## Installation

To just install the tool:
`python3 -m pip install f2r`

OR

Use [flp-release-server](https://gitlab.cern.ch/AliceO2Group/system-configuration/-/tree/dev/ansible/roles/flp-release-server) role from `system-configuration` to fully provision a build server.


## Quickstart
Build packages using `aliBuild`, eg:
```bash
aliBuild build O2Suite --defaults o2-dataflow --always-prefer-system
```
Then, run `alienv` as indicated by `aliBuild` in order to create modulefiles:
```bash
alienv enter O2Suite/latest-o2-dataflow
exit # do not forget to exit
```
And create RPMs providing same package and version as to `alienv`:
```bash
f2r generate --package O2Suite --version latest-o2-dataflow
```
Validate created RPMs (this requires `sudo`):
```
f2r validate
```
Create YUM repo:
```bash
f2r repo
```

and sync it to S3:
```bash
f2r sync
```

## CLI options

Simple run `f2r -h` to see all available options


## Developers documentation

### Software lifecycle
- Make changes and merge MR when all tests pass
- Bump `version` in `setup.py`
- Publish to PyPI
  - `python3 setup.py sdist bdist_wheel`
  - `TWINE_USERNAME=$TWINE_USERNAME TWINE_PASSWORD=$TWINE_PASSWORD python3 -m twine upload --repository pypi dist/*`
- Update build server using `pip`

### Simple description of the logic
Creates tree of dependencies by recursively iterating over "alidist" recipes. It disables certain packages based on selected "defaults".
It retrieves versioning information from "modulefiles" (as "alidist" recipes do not provide that).

It is capable of generating "devel" RPMs. In such case, in addition to runtime dependencies, it also packs build dependencies. (**NOTE**: There is no source of truth for build dependencies versioning, therefore the latest available version is used.)

It picks up system dependencies when aliBuild package is not available. For this reason it uses definitions in `(devel|runtime).slc*.yaml` file translate system dependencies into list of RPM packages.

Then, it uses [fpm](https://fpm.readthedocs.io) tool to generate RPMs.

## Setup virtual environment for development and test (venv)

1. `cd flp-to-rpm`
2. `python3 -m venv env`
3. `source env/bin/activate`
4. `python -m pip install -r requirements.txt`
5. `python3 -m pip install . `
6. You can execute and work. Next time just do `source env/bin/activate` and then you are good to go.
7. If you modify the code, then rerun `python3 -m pip install .`

## Unit Tests

```
cd flp-to-rpm
source env/bin/activate  
cd tests

# Run a test: 
python -m unittest testModule.TestModule.test_versions

# Run all tests:
python3 -m unittest discover`
```