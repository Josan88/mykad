# MyKAD
This program uses [pyscard](https://pyscard.sourceforge.io/) for adding smart cards support to Python.
# Usage
This program sends apdu commands to mykad to obtain data from mykad. Different apdu command is needed to read different jpn files. The info read is then stored in json files.

More info on: http://forum.lowyat.net/index.php?showtopic=355950&view=findpost&p=11151482

The info can be read at *index.php*.

# Future suggestion and improvement
Extract biometric template from MyKAD and use it for biometric verification (Decryption is needed).

Guidelines for Securing MyKAD Enhanced Biometric Access (EBA) Ecosystem: https://www.cybersecurity.my/data/content_files/56/2079.pdf
