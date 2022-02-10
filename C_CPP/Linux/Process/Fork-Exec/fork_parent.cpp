#include <cstdio>
#include <iostream>

#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <string>
using namespace std;

#define APPLY_FD_CLOEXEC
int main()
{
	

	pid_t pid_child;
	int fd = open("Text.txt", O_WRONLY | O_CREAT | O_APPEND, 0644);
	if (fd == -1) {
		perror("FAIL:OPEN");
		exit(EXIT_FAILURE);
	}
	dprintf(fd, "Parent[%d]:Open log file(fd=%d)\n", getpid(), fd);
	/*
		dprintf(fd, format, ...);
		���н����� High-Level, Low-Level ����ó���� ����
		����� (fpintf, fscanf) :ȿ������, ����ӵ�������, ���� ���
		������(read, write) : ȿ��������, ����ӵ�����, ���� ��� ���ؼ� CPU ���� ����
		write�� �̿��� ���, �������� �ȵ� - sprintf + write ����
		�̸� ���� ������ ���� �����
		dprintf
	*/
#ifdef APPLY_FD_CLOEXEC
	int ret_fcntl;
	if ((ret_fcntl = fcntl(fd, F_SETFD, FD_CLOEXEC)) == -1) {
		perror("FAIL : fcntl(F_SETFD, FD_CLOEXEC)");
		exit(EXIT_FAILURE);
	}
#endif
	// fork-exec
	char *argv_exec[] = { "forkexec_childE", (char*)NULL };
	switch ((pid_child = fork()))
	{
	case 0:
		//Child
		execv(argv_exec[0], argv_exec);
		break;
	case -1:
		//Error
		perror("FAIL : FORK");
		break;
	default:
		//Parent
		wait();
		break;
	}
	printf("Parent[%d]:Exit\n", getpid());
    return 0;
}