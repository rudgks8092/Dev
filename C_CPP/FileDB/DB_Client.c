#pragma warning(disable:4996)
#include <stdbool.h>
#include <WinSock2.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
// 프로젝트 속성 - 링커 - 입력 - 추가종속성에 
// ws2_32.lib 추가 필수
WSADATA wsaData;
SOCKET hSocket;

// Console 조작에 대한 CALLBACK 함수
BOOL CtrlHandler(DWORD fdwCtrlType) {
    
    switch (fdwCtrlType)
    {
    case CTRL_C_EVENT:
    case CTRL_CLOSE_EVENT:
    case CTRL_LOGOFF_EVENT:
    case CTRL_SHUTDOWN_EVENT:
    case CTRL_BREAK_EVENT:
    default:
        send(hSocket, "exit", 5, 0);
        closesocket(hSocket); //소켓 라이브러리 해제
        WSACleanup();
    }
    return FALSE;
}

int main()
{
    // Console 조작에 대한 WINAPI Handler 적용
    BOOL fSuccess = SetConsoleCtrlHandler((PHANDLER_ROUTINE)CtrlHandler, TRUE);
    SOCKADDR_IN servAddr;
    bool bFlag = false;
    char message[256];
    int strLen;
    //소켓 라이브러리 초기화
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) 
    {
        // ERROR
    }
    // 소켓 생성
    hSocket = socket(PF_INET, SOCK_STREAM, 0); 
    if (hSocket == INVALID_SOCKET)
    {
        // ERROR
    }

    memset(&servAddr, 0, sizeof(servAddr));
    servAddr.sin_family = AF_INET;
    servAddr.sin_addr.s_addr = inet_addr("127.0.0.1");
    servAddr.sin_port = htons(12345);
    
    char buf[256] = "";
    char* p = NULL;
    // Connect + Receive 
    while (1)
    {
        printf("SHELL >> ");
        scanf(" %[^\n]s", buf);
        if (bFlag)
        {
            send(hSocket, buf, sizeof(buf), 0);
            strLen = recv(hSocket, message, sizeof(message), 0);
            if (strLen == 0)
            {
                printf("종료\n");
                break;
            }
            printf("%s\n", message);
        }

        if (!bFlag) {

            p = strtok(buf, " ");
            if (!strcmp(p, "connect")) {
                p = strtok(NULL, " ");
                servAddr.sin_addr.s_addr = inet_addr(p);
                if (connect(hSocket, (SOCKADDR*)&servAddr, sizeof(servAddr)) == SOCKET_ERROR)
                {
                    // ERROR
                    printf("CONNET ERROR!\n");
                    return 0;
                }
                else {
                    bFlag = true;
                }
            }
        }
    }
    return 0;
}
