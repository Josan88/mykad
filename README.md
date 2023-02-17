# MyKad Reader
This code reads the MyKad identification card using a smart card reader. It selects the JPN (Jabatan Pendaftaran Negara, National Registration Department) application and reads data from various files, including the user's photograph.

## Prerequisites
To use this code, you will need the following:
- A smart card reader
- The smartcard package for Python (which can be installed via pip)
- A MyKad identification card

## Usage
This program sends apdu commands to mykad to obtain data from mykad. [Different apdu command](http://forum.lowyat.net/index.php?showtopic=355950&view=findpost&p=11151482) is needed to read different jpn files. The info read is then stored in json files.

## Steps
1. Extract the zip file.
2. Insert a MyKad into the smart card reader.
3. Run mykad.exe in /dist/.

![image](https://user-images.githubusercontent.com/124897328/219552775-2b01736c-c44c-4110-b2b6-85a730048fcf.png)
4. The program is started in the background (mykad.exe).
5. The script will automatically detect the insertion of the card, select the JPN application, and read data from various files, including the user's photograph.
6. After reading, data is stored in 2 json file. 
7. The user's photograph will be saved as a JPEG file named "photo.jpg" in the current directory.
8. View data in index.php.
9. If user want to read another myKAD, remove the inserted card and insert another myKAD.



## Future suggestion and improvement
Extract biometric template from MyKAD and use it for biometric verification (Decryption is needed).

[Guidelines for Securing MyKAD Enhanced Biometric Access (EBA) Ecosystem](https://www.cybersecurity.my/data/content_files/56/2079.pdf)
