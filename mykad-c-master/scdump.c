#include <stdio.h>
#include <winscard.h>
#include <scarderr.h>

#ifndef SCARD_E_NO_READERS_AVAILABLE
#define SCARD_E_NO_READERS_AVAILABLE ((DWORD)0x8010002E)
#endif

void TrimString(char *out, char *in, int count);
void DateString(char *out, unsigned char *in);
void PostcodeString(char *out, unsigned char *in);

const unsigned char CmdSelectAppJPN[] = 
	{0x00, 0xA4, 0x04, 0x00, 0x0A, 0x0A0, 0x00, 0x00, 0x00, 0x74, 0x4A, 0x50, 0x4E, 0x00, 0x10};
const unsigned char CmdAppResponse[] =
	{0x00, 0xC0, 0x00, 0x00, 0x05};
const unsigned char CmdSetLength[] =
	{0xC8, 0x32, 0x00, 0x00, 0x05, 0x08, 0x00, 0x00};		//append with ss ss
const unsigned char CmdSelectFile[] =
	{0xCC, 0x00, 0x00, 0x00, 0x08}; //append with pp pp qq qq rr rr ss ss
										//pppp = file id, qqqq = file group
										//rrrr = offset, ssss = length
const unsigned char CmdGetData[] =
	{0xCC, 0x06, 0x00, 0x00};		//append with ss
const int fileLengths[] = {0, 459, 4011, 1227, 171, 43, 43, 0};

SCARD_IO_REQUEST pciT0 = {1, 8};

int main(void)
{
	SCARDCONTEXT hSC;
	SCARDHANDLE	hCard;
	char RxBuffer[256];
	char TxBuffer[64];
	char ReaderName[64];
	int retval, dCount, i, dProtocol, dLength, FileNum;
	int split_offset, split_length;
	FILE *outfile, *out2file;

	retval = SCardEstablishContext(SCARD_SCOPE_USER, 0, 0, &hSC);
	if (retval == SCARD_E_NO_SERVICE) {
		printf("Smart card service not started\n");
		goto _Quit;
	}
	else if (retval != 0) {
		printf("SCardEstablishContext Error: %x\n", retval);
		goto _Quit;
	}

	printf("Ready to read, press Enter");
	getchar();

	dCount = 256;
	retval = SCardListReaders(hSC, 0, RxBuffer, &dCount);
	if (retval == SCARD_E_NO_READERS_AVAILABLE) {
		printf("SCardListReaders: No readers available\n");
		goto _ReleaseContext;
	}
	else if (retval != 0) {
		printf("SCardListReaders: Error %x\n", retval);
		goto _ReleaseContext;
	}
	for (i=0; (ReaderName[i] = RxBuffer[i]) && i<64; i++);
	if (!i) {
		printf("SCardListReaders: No readers available\n");
		goto _ReleaseContext;
	}
	puts(ReaderName);
	retval = SCardConnect(hSC, ReaderName, SCARD_SHARE_SHARED, SCARD_PROTOCOL_T0, &hCard, &dProtocol);
	if (retval == SCARD_W_REMOVED_CARD || retval == SCARD_E_NO_SMARTCARD) {
		printf("Smart card removed\n");
		goto _ReleaseContext;
	}
	else if (retval != 0) {
		printf("SCardConnect: Error %x\n", retval);
		goto _ReleaseContext;
	}
	printf("Selecting JPN application\n");
	dLength = 256;
	retval = SCardTransmit(hCard, &pciT0, CmdSelectAppJPN, 15, &pciT0, RxBuffer, &dLength);
	if (retval) {
		printf("SCardTransmit (Select App): Error %x\n", retval);
		goto _ReleaseContext;
	}
	else if (RxBuffer[0] != 0x61 || RxBuffer[1] != 0x05) {
		printf("Not MyKad\n");
		goto _ReleaseContext;
	}
	dLength = 256;
	retval = SCardTransmit(hCard, &pciT0, CmdAppResponse, 5, &pciT0, RxBuffer, &dLength);
	if (retval) {
		printf("SCardTransmit (App Response): Error %x\n", retval);
		goto _ReleaseContext;
	}

	for (FileNum = 1; fileLengths[FileNum]; FileNum++) {
		printf("Reading JPN file %d ", FileNum);
		sprintf(RxBuffer, "jpn%d", FileNum);
		outfile = fopen(RxBuffer, "wb+");
		if (FileNum == 2)
			out2file = fopen("photo.jpg", "wb+");
		for (split_offset=0, split_length=252; split_offset<fileLengths[FileNum]; split_offset+=split_length) {
			printf(".");
			if (split_offset+split_length > fileLengths[FileNum])
				split_length = fileLengths[FileNum] - split_offset;
			dLength = 256;
			for (i=0; i<8; TxBuffer[i++] = CmdSetLength[i]);
			*(short *) (TxBuffer+i) = split_length;	i += 2;
			retval = SCardTransmit(hCard, &pciT0, TxBuffer, i, &pciT0, RxBuffer, &dLength);

			dLength = 256;
			for (i=0; i<5; TxBuffer[i++] = CmdSelectFile[i]);
			*(short *) (TxBuffer+i) = FileNum;	i += 2;
			*(short *) (TxBuffer+i) = 1;	i += 2;
			*(short *) (TxBuffer+i) = split_offset;	i += 2;
			*(short *) (TxBuffer+i) = split_length;	i += 2;
			retval = SCardTransmit(hCard, &pciT0, TxBuffer, i, &pciT0, RxBuffer, &dLength);

			dLength = 256;
			for (i=0; i<4; TxBuffer[i++] = CmdGetData[i]);
			TxBuffer[i++] = (unsigned char) split_length;
			retval = SCardTransmit(hCard, &pciT0, TxBuffer, i, &pciT0, RxBuffer, &dLength);
			fwrite(RxBuffer, 1, dLength-2, outfile);
			if (FileNum == 2) {
				if (split_offset == 0)
					fwrite(RxBuffer+3, 1, dLength-5, out2file);
				else
					fwrite(RxBuffer, 1, dLength-2, out2file);
			}
			/* extra display stuffs */
			if (FileNum==1 && split_offset==0) {
				TrimString(TxBuffer, RxBuffer+0x03, 0x28);
				printf("\nName:           %s\n", TxBuffer);
			}
			else if (FileNum==1 && split_offset==252) {
				TrimString(TxBuffer, RxBuffer+0x111-252, 0x0D);
				printf("\nIC:             %s\n", TxBuffer);
				printf("Sex:            ");
				if (RxBuffer[0x11E-252] == 'P')
					printf("Female\n");
				else if (RxBuffer[0x11E-252] == 'L')
					printf("Male\n");
				else
					printf("%c\n", RxBuffer[0x11E-252]);
				TrimString(TxBuffer, RxBuffer+0x11F-252, 0x08);
				printf("Old IC:         %s\n", TxBuffer);
				DateString(TxBuffer, RxBuffer+0x127-252);
				printf("DOB:            %s\n", TxBuffer);
				TrimString(TxBuffer, RxBuffer+0x12B-252, 0x19);
				printf("State of birth: %s\n", TxBuffer);
				DateString(TxBuffer, RxBuffer+0x144-252);
				printf("Validity Date:  %s\n", TxBuffer);
				TrimString(TxBuffer, RxBuffer+0x148-252, 0x12);
				printf("Nationality:    %s\n", TxBuffer);
				TrimString(TxBuffer, RxBuffer+0x15A-252, 0x19);
				printf("Ethnic/Race:    %s\n", TxBuffer);
				TrimString(TxBuffer, RxBuffer+0x173-252, 0x0B);
				printf("Religion:       %s\n", TxBuffer);
			}
			else if (FileNum==4 && split_offset==0) {
				printf("\nAddress:\n");
				TrimString(TxBuffer, RxBuffer+0x03, 0x1E);
				puts(TxBuffer);
				TrimString(TxBuffer, RxBuffer+0x21, 0x1E);
				puts(TxBuffer);
				TrimString(TxBuffer, RxBuffer+0x3F, 0x1E);
				puts(TxBuffer);
				PostcodeString(TxBuffer, RxBuffer+0x5D);
				printf("%s\t", TxBuffer);
				TrimString(TxBuffer, RxBuffer+0x60, 0x19);
				puts(TxBuffer);
				TrimString(TxBuffer, RxBuffer+0x79, 0x1E);
				puts(TxBuffer);
			}
			/* End displaying stuffs */
		}
		printf("\n");
		fclose(outfile);
		if (FileNum == 2)
			fclose(out2file);
	}
_ReleaseContext:
	SCardReleaseContext(hSC);
_Quit:
	printf("press Enter to end program");
	getchar();

	return 0;
}

void TrimString(char *out, char *in, int count)
{
	int i, j;
	for (i=count-1; i>=0 && in[i] == 0x20; i--);
	for (j=0; j<i+1; out[j++]=in[j]);
	out[j] = 0;
}

void DateString(char *out, unsigned char *in)
{
	sprintf(out, "%02x", in[0]);
	sprintf(out+2, "%02x-", in[1]);
	sprintf(out+5, "%02x-", in[2]);
	sprintf(out+8, "%02x", in[3]);
	out[10] = 0;
}

void PostcodeString(char *out, unsigned char *in)
{
	sprintf(out, "%02x", in[0]);
	sprintf(out+2, "%02x", in[1]);
	sprintf(out+4, "%02x", in[2]);
	out[5] = 0;
}
