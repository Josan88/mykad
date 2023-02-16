# MyKAD
This program uses [pyscard](https://pyscard.sourceforge.io/) for adding smart cards support to Python.

##Installation
pip install pyscard

## Usage
This program sends apdu commands to mykad to obtain data from mykad. [Different apdu command](http://forum.lowyat.net/index.php?showtopic=355950&view=findpost&p=11151482) is needed to read different jpn files. The info read is then stored in json files.

## Steps
1. Run mykad.exe.
2. Insert myKAD into a smartcard reader.
3. Wait for the program to read.
![image](https://user-images.githubusercontent.com/124897328/219326018-d3dce885-7af8-46cb-afe7-f0e479830735.png)
4. After reading, data is stored in 2 json file and 1 jpg.
5. View data in index.php.
6. If user want to read another myKAD, remove the inserted card and insert another myKAD.



## Future suggestion and improvement
Extract biometric template from MyKAD and use it for biometric verification (Decryption is needed).

[Guidelines for Securing MyKAD Enhanced Biometric Access (EBA) Ecosystem](https://www.cybersecurity.my/data/content_files/56/2079.pdf)
