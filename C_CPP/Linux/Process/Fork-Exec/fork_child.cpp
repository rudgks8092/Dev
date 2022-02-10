#include <cstdio>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
int main()
{
	dprintf(STDOUT_FILENO, "Child = %d\n", getpid());
	dprintf(3, "CHILD fd3 %d\n", getpid());
	close(3);
	dprintf(STDOUT_FILENO, "CHILD EXIT\n", getpid());

    return 0;
}