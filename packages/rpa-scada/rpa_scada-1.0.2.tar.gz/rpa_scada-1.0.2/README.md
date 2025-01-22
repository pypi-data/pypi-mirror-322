# RPA
Scraper para obtener los datos desde el acceso web del SCADA sin la necesidad de un navegador

## Build
para construir el paquete:
```
python setup.py sdist bdist_wheel
```

para subir el paquete a pypi:
```
python -m twine upload dist/*
```

## instalacion
para instalar el paquete local
```
pip install PATH_MODULE/dist/mipaquete-0.1.tar.gz
```
