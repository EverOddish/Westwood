# Westwood

Westwood is an open source project that stores Pokemon data in a human-readable format that is easy to extend and use.

## Format

XML was chosen as the primary data storage format. XML is human-readable, easy to understand for non-programmers, widely supported by many different programming languages, and is verifiable for correctness through the use of XML Schema Definition (XSD) files. Human-readability should be prioritized over implementation wherever possible.

## Usage

Westwood contains Python scripts to verify the correctness of all XML data, and to convert the XML data to a format that lends itself to generating a relational database. The scripts generate Comma-Separated Value (CSV) files that resemble the format of relational database tables, containing properly-generated index numbers that describe the relationships between concepts. This intermediary CSV format allows the data set to be database-independent and alleviates the burden of specifying implementation-specific information (such as index numbers) from any contributors.

## Name Origin

The name "Westwood" comes from Professor Westwood, a Pokedex programmer. https://bulbapedia.bulbagarden.net/wiki/Professor_Westwood_V
