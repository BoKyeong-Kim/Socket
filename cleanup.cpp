#include <winsock2.h>
#include <tchar.h> 

int main (int argc, char* argv[])
{
	//�����ʱ�ȭ
	WSADATA wsa;
	if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0)
	return -1;
	MessageBox(NULL, "�����ʱ�ȭ ����","����", MB_OK);

	//���� ����
	WSACleanup();
	return 0;
}