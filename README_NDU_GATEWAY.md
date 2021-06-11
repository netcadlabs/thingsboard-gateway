# NDU IoT Gateway  

The NDU **IoT Gateway** is an open-source solution that allows you to integrate devices connected to legacy and third-party systems with NDU. 

This project is forked from [Thingsboard IoT Gateway](https://github.com/thingsboard/thingsboard-gateway)

## Building & Publishing Module

To build ndu version of the gateway module, run the following script.

```
 make_pypi_dist-ndu_gateway.ps1
```
 
Publish ndu-gateway module (use netcadlabs pypi credentials)

```
 python -m twine upload dist/*
```
 
## Installing ndu-gateway module

To install from source code, run the following script.

```
 pip install ./dist/ndu_gateway-<VERSION>.whl
```

Install using pip

```
 pip install ndu-gateway
```



## Running

``` python -c "from ndu_gateway.tb_gateway import daemon; daemon()" ```

or 

``` ndu-gateway -c custom_config_path_.yml ```

## Licenses

This project is released under [Apache 2.0 License](./LICENSE).
