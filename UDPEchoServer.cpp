#include <WinSock2.h>
#include <stdio.h>

#define PORT 9000
#define MAXBUF 256

int main()
{
	SOCKADDR_IN serv_Addr;
	SOCKADDR_IN client_Addr;
	SOCKET serv_Socket;
	WSADATA wsadata;

	int ret;
	char buf[MAXBUF];
	int len;

	if (WSAStartup(MAKEWORD(2, 2), &wsadata))
	{
		return 0;
	}

	serv_Socket = socket(AF_INET, SOCK_DGRAM, 0);
	if (serv_Socket == INVALID_SOCKET)
	{
		printf("Socket Create : 실패(%d)\n", WSAGetLastError());
		return 0;
	}
	ZeroMemory(&serv_Addr, sizeof(serv_Addr));
	serv_Addr.sin_family = AF_INET;
	serv_Addr.sin_addr.S_un.S_addr = htonl(INADDR_ANY);
	serv_Addr.sin_port = htons(PORT);

	ret = bind(serv_Socket, (SOCKADDR*)&serv_Addr, sizeof(serv_Addr));
	if (ret == SOCKET_ERROR)
	{
		printf("Socket Bind : 실패(%d)\n", WSAGetLastError());
		closesocket(serv_Socket);
		return 0;
	}
	int size = sizeof(client_Addr);

	for (;;) {
		printf("클라이언트로부터 데이터를 기다린다\n");
		ret = recvfrom(serv_Socket, buf, sizeof(buf), 0, (SOCKADDR*)&client_Addr, &size);
		if (ret == SOCKET_ERROR)
		{
			printf("recvfrom : 실패(%d)\n", WSAGetLastError());
			break;
		}
		buf[ret] = 0;
		printf("read ====> %s\n", buf);

		ret = sendto(serv_Socket,buf,ret,0, (SOCKADDR*)&client_Addr, size);
		if (ret == SOCKET_ERROR)
		{
			printf("sendto : 실패(%d)\n", WSAGetLastError());
			break;
		}
	}
	closesocket(serv_Socket);
	WSACleanup();
	return 1;
}