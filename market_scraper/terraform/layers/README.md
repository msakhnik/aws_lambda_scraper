# Lambda Layers

The folder contains lambda layer that created from ../src/requirements.txt

Steps:

    $ mkdir python
    $ cd python/
    $ pip3 install -r ../../../src/requirements.txt --target ./
    $ ../
    $ zip -r9 lambda-layer.zip .
