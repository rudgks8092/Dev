### Fork-Exec

리눅스에서 fork 이후 exec를 통하여 자식 프로세스를 제어하는 경우,
exec를 수행하며 복사해간 메모리 중 FD(파일 기술자)를 사용이 가능함

자식 프로세스가 별도로 open하지 않아도, 동일 fd로 열고, 닫음  
![image](https://user-images.githubusercontent.com/85000118/153324328-429e221f-d865-4104-b827-a62669394f04.png)
