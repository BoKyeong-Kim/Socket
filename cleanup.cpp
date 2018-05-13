#include <winsock2.h>
#include <tchar.h> 

int main (int argc, char* argv[])
{
	//윈속초기화
	WSADATA wsa;
	if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0)
	return -1;
	MessageBox(NULL, "윈속초기화 성공","성공", MB_OK);

	//윈속 종료
	WSACleanup();
	return 0;
}