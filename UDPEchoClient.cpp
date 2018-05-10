#define _WINSOCK_DEPRECATED_NO_WARNINGS
#define _CRT_SECURE_NO_WARNINGS
#include <winSock2.h>
#include <stdio.h>

#define PORT 9000
#define MAXBUF 4096

int main()
{
	SOCKET clientSocket;
	SOCKADDR_IN serv_Addr;
	SOCKADDR_IN recv_Addr;
	char buf[MAXBUF + 1];
	int ret;
	int size;
	WSADATA wsadata;
	
	if (WSAStartup(MAKEWORD(2, 2), &wsadata))
	{
		return 0;
	}

	clientSocket = socket(AF_INET, SOCK_DGRAM, 0);
	if (clientSocket == INVALID_SOCKET)
	{
		printf("Socket Create : 실패(%d)\n", WSAGetLastError());
		return 0;
	}
	ZeroMemory(&serv_Addr, sizeof(serv_Addr));
	serv_Addr.sin_family = AF_INET;
	serv_Addr.sin_port = htons(PORT);
	serv_Addr.sin_addr.S_un.S_addr = inet_addr("127.17.209.103");
	
	while (1) 
	{
		printf("전달할 데이터 : ");
		scanf("%s", buf);
		ret = sendto(clientSocket, buf,strlen(buf),0,(struct sockaddr*)&serv_Addr, sizeof(serv_Addr));
		if (ret == SOCKET_ERROR)
			{
			printf("sendto error : %d\n", WSAGetLastError());
			closesocket(clientSocket);
			return 0;
			}

			printf("sendto ====> %s\n",buf);

			size = sizeof(recv_Addr);
			ret = recvfrom(clientSocket, buf, sizeof(buf), 0, (struct sockaddr*)&recv_Addr, &size);
		if (ret == SOCKET_ERROR)
		{
			printf("sendto error : %d\n", WSAGetLastError());
			closesocket(clientSocket);
			return 0;
		}
		buf[ret] = 0;
		printf("recvfrom ====> %s\n", buf);

	}
	closesocket(clientSocket);
	WSACleanup();
	return 1;
}