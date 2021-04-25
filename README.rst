pl-pfdcm_tagextract
================================

.. image:: https://img.shields.io/docker/v/fnndsc/pl-pfdcm_tagextract?sort=semver
    :target: https://hub.docker.com/r/fnndsc/pl-pfdcm_tagextract

.. image:: https://img.shields.io/github/license/fnndsc/pl-pfdcm_tagextract
    :target: https://github.com/FNNDSC/pl-pfdcm_tagextract/blob/master/LICENSE


.. contents:: Table of Contents


Abstract
--------

An app to ...


Description
-----------

``pfdcm_tagextract`` is a ChRIS-based application that...


Usage
-----

.. code::

    python pfdcm_tagextract.py
        [-h|--help]
        [--json] [--man] [--meta]
        [--savejson <DIR>]
        [-v|--verbosity <level>]
        [--version]
        <inputDir> <outputDir>


Arguments
~~~~~~~~~

.. code::

    [-h] [--help]
    If specified, show help message and exit.
    
    [--json]
    If specified, show json representation of app and exit.
    
    [--man]
    If specified, print (this) man page and exit.

    [--meta]
    If specified, print plugin meta data and exit.
    
    [--savejson <DIR>] 
    If specified, save json representation file to DIR and exit. 
    
    [-v <level>] [--verbosity <level>]
    Verbosity level for app. Not used currently.
    
    [--version]
    If specified, print version number and exit. 


Getting inline help is:

.. code:: bash

    docker run --rm fnndsc/pl-pfdcm_tagextract pfdcm_tagextract --man

Run
~~~

You need to specify input and output directories using the `-v` flag to `docker run`.


.. code:: bash

    docker run --rm -u $(id -u)                             \
        -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
        fnndsc/pl-pfdcm_tagextract pfdcm_tagextract                        \
        /incoming /outgoing


Development
-----------

Build the Docker container:

.. code:: bash

    docker build -t local/pl-pfdcm_tagextract .

Run unit tests:

.. code:: bash

    docker run --rm local/pl-pfdcm_tagextract nosetests

Examples
--------

Put some examples here!


.. image:: https://raw.githubusercontent.com/FNNDSC/cookiecutter-chrisapp/master/doc/assets/badge/light.png
    :target: https://chrisstore.co
