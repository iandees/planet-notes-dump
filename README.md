planet-notes-dump
=================

A utility to dump OpenStreetMap notes from the database into an XML file for bulk use.

Installation
------------

On Ubuntu 12.04 LTS:

    # Install virtualenvwrapper
    sudo apt-get install virtualenvwrapper
    source ~/.bashrc

    # Make a virtualenv for planet-notes-dump
    mkvirtualenv --no-site-packages planet-notes-dump

    # Install prerequisites for planet-notes-dump
    sudo apt-get install build-essential python-dev libxml2-dev libxslt-dev
    pip install -r requirements.txt

Running
-------

    # Use your virtualenv
    workon planet-notes-dump

    # Execute the initial dump
    python dump.py --database openstreetmap --username foo notes_dump.xml

