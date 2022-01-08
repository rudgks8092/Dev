#pragma warning (disable:4996)
#include <stdbool.h>
#include <WinSock2.h>
#include <Windows.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

void initSocket(SOCKET* hServerSock);
// 프로젝트 속성 - 링커 - 입력 - 추가종속성에 
// ws2_32.lib 추가 필수

typedef struct _NODE_ {
	char key[100];
	char value[256];
	struct _NODE_* next;
} NODE;

NODE* HEAD = NULL;
NODE* TAIL = NULL;

SOCKET hServerSock, hClientSock = INVALID_SOCKET;
const char* readData(const char* key);
NODE* checkData(const char* key);
void clearData();
void addData(const char* key, const char* value);

// Console 조작에 대한 CALLBACK 함수
BOOL CtrlHandler(DWORD fdwCtrlType) {
	FILE* fp;
	switch (fdwCtrlType) 
	{ 
	case CTRL_C_EVENT:
	case CTRL_CLOSE_EVENT: 
	case CTRL_LOGOFF_EVENT: 
	case CTRL_SHUTDOWN_EVENT: 
	case CTRL_BREAK_EVENT: 
	default:
		// 모든 종료 단계
		fp = fopen("./data.txt", "w+");
		if (HEAD != NULL)
		{
			NODE* target = HEAD;
			while (1)
			{
				if (target == NULL) break;
				fprintf(fp, "%s:%s\n", target->key, target->value);
				target = target->next;
			}
			
		}
		else { fprintf(fp, ""); }
		clearData();
		fclose(fp);
		closesocket(hServerSock);
		closesocket(hClientSock);
		WSACleanup();
	} 
	return FALSE; 
}
int main()
{
	// Console 조작에 대한 WINAPI Handler 적용
	BOOL fSuccess = SetConsoleCtrlHandler((PHANDLER_ROUTINE)CtrlHandler, TRUE);
	WSADATA wsaData;
	SOCKADDR ClientAddr;
	FILE* fp;
	
	int nClientAddrSize = sizeof(ClientAddr);
	const char TAG_READ[] = "read";
	const char TAG_SAVE[] = "save";
	const char TAG_CLEAR[] = "clear";
	const char TAG_EXIT[] = "exit";
	char key[100] = "";
	char value[256] = "";
	char buf[256] = "";
	char* p = NULL;
	char check[10] = "";
	// Socket 라이브러리 초기화
	if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0)
	{
		// ERROR
		printf("WinSock Init Failed!\n");
		return -1;
	}

	// 저장된 Data들 불러오기
	fp = fopen("./data.txt", "r+");
	if (fp != NULL)
	{
		while (true)
		{
			//result = fscanf(fp, "%[^:]s %s\n", key, value);
			if (fgets(buf, 256, fp) == NULL) break;
			sscanf(buf, "%[^:]%[:]%s\n", key, check,value);
			addData(key, value);
		}
		fclose(fp);
	}

	while (1)
	{
		if (hClientSock == INVALID_SOCKET) {
			initSocket(&hServerSock);
			printf("연결 대기 중\n");
			// 클라이언트 접속 대기
			hClientSock = accept(hServerSock, (SOCKADDR*)&ClientAddr, &nClientAddrSize);
			if (hClientSock == INVALID_SOCKET)
			{
				//ERROR
				printf("Client ACCEPT ERROR!\n");
			}
			else
			{
				closesocket(hServerSock);
				printf("접속 완료\n");
			}
		}
		//send(hClientSock, buf, sizeof(buf), 0);
		recv(hClientSock, buf, sizeof(buf), 0);
		p = strtok(buf, " ");
		if (!strcmp(p, TAG_EXIT)) {
			shutdown(hClientSock, SD_SEND);
			//closesocket(hClientSock);
			hClientSock = INVALID_SOCKET;
		}
		else if (!strcmp(p, TAG_SAVE)) {
			if (*(p + 5) == '\0') goto ERR;
			p = strtok(p+5, ":");
			if (p == NULL) goto ERR;
			strcpy(key, p);
			p = strtok(NULL, " ");
			if (p == NULL) goto ERR;
			strcpy(value, p);
			addData(key, value);
			sprintf(buf, "%s", "SAVE OK");
			send(hClientSock, buf,sizeof(buf) ,0);
		}
		else if (!strcmp(p, TAG_CLEAR)) {
			clearData();
			sprintf(buf, "%s", "CLEAR OK");
			send(hClientSock, buf, sizeof(buf), 0);
		}
		else if (!strcmp(p, TAG_READ)) {
			p = strtok(NULL, " ");
			if (p == NULL) goto ERR;
			strcpy(key, p);
			sprintf(buf, "%s", readData(key));
			send(hClientSock, buf, sizeof(buf), 0);
		}
		else {
		ERR:
			sprintf(buf, "%s", "INVALID_COMMAND");
			send(hClientSock, buf, sizeof(buf), 0);
			
		}
	}
	closesocket(hServerSock);
	closesocket(hClientSock);
	WSACleanup();
	return 0;
}

void initSocket(SOCKET* hServerSock)
{
	
	SOCKADDR_IN serverAddr;
	// 소켓 생성
	*hServerSock = socket(PF_INET, SOCK_STREAM, 0);
	if (*hServerSock == INVALID_SOCKET)
	{
		// 생성 ERROR
		printf("Create Socket Failed!\n");
	}

	// 서버 IP Address 설정
	memset(&serverAddr, 0, sizeof(serverAddr));
	serverAddr.sin_family = AF_INET;
	serverAddr.sin_addr.s_addr = htonl(INADDR_ANY);
	serverAddr.sin_port = htons(12345);

	// 소켓 IP + PORT 연결
	int result = bind(*hServerSock, (SOCKADDR*)&serverAddr, sizeof(serverAddr));
	// ERROR
	if (result == SOCKET_ERROR){ printf("SOCKET BIND ERROR!\n"); }
		
	// ServerSocket Listen
	result = listen(*hServerSock, 0);
	// ERROR
	if (result == SOCKET_ERROR) { printf("Listen ERROR!\n"); }
		
}

void addData(const char* key, const char* value)
{
	NODE* target = NULL;
	if (HEAD == NULL)
	{
		HEAD = (NODE*)malloc(sizeof(NODE));
		TAIL = HEAD;
		HEAD->next = NULL;
		strcpy(HEAD->key, key);
		strcpy(HEAD->value, value);
	}
	else
	{
		target = checkData(key);
		if (target == NULL)
		{
			TAIL->next = (NODE*)malloc(sizeof(NODE));
			TAIL = TAIL->next;
			strcpy(TAIL->key, key);
			strcpy(TAIL->value, value);
			TAIL->next = NULL;
		}
		else
		{
			strcpy(target->value, value);
		}
	}
}
void clearData()
{
	if (HEAD == NULL) return;
	NODE* target = NULL;
	while (HEAD != NULL)
	{
		 target = HEAD;
		 HEAD = HEAD->next;
		 free(target);
	}
	TAIL = NULL;
	HEAD = NULL;
}

const char* readData(const char* key)
{
	if (HEAD == NULL) return "DB is Empty!";
	NODE* target = HEAD;
	
	while (1)
	{
		if (target == NULL) break;
		if (!strcmp(target->key, key)) {
			return target->value;
		}
		target = target->next;
	}
	return "INVALID Key";
}

NODE* checkData(const char* key)
{
	if (HEAD == NULL) return NULL;
	NODE* target = HEAD;
	while (1)
	{
		if (target == NULL) return NULL;
		if (!strcmp(target->key, key)) {
			return target;
		}
		target = target->next;
	}
	return NULL;
}
