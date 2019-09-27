# Westwood

Westwood is an open source project that stores high-quality Pokemon game data in a human-readable format that is easy to extend and use.

## Data Format

XML has been chosen as the primary data storage format. XML is human-readable, easy to understand for non-programmers, widely supported by many different programming languages, and is verifiable for correctness through the use of XML Schema Definition (XSD) files. Human-readability should be prioritized over implementation wherever possible. It is intended that the data set be easily extensible for new official Pokemon games, and popular fan-made content (such as ROM hacks).

## Usage

Westwood contains Python scripts to verify the correctness of all XML data, and to convert the XML data to a format that lends itself to generating a relational database.

Westwood data can be converted to any data format, if support is added. To start with, Westwood will only support conversion to Django models, which can then be populated with Django data migrations. If other formats are required (such as JSON or CSV), support can be added at a later date. Westwood is intended to be easily extensible and adaptable.

Python 3 is required. To install all Python requirements:

    pip install -r requirements.txt

To validate the XML data, run the following command:

    python3 validate.py

To auto-generate Django models inside the django-westwood app, run the following command:

    python3 convert_to_django.py

This will read every XSD file and generate Python classes that describe each model. Then, a database will be generated using the models, and populated from the XML data by running a Django data migration.

## Contributing

If you notice any errors in the data or would like to contribute, there are several ways you can help:

 * Open an issue on GitHub
 * Fix the issue and open a pull request on GitHub
 * Contact @EverOddish on Twitter <https://twitter.com/EverOddish>

## Name Origin

The name "Westwood" comes from Professor Westwood, a Pokedex programmer. https://bulbapedia.bulbagarden.net/wiki/Professor_Westwood_V

## Disclaimer

All Pokemon data is owned by The Pokemon Company International. This project should not be used for commercial purposes.
