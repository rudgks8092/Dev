using System;
//using namespace;

using static System.Console;
// System.Console의 메서드 자유 사용 ex. WriteLine

// C#은 개체 지향 구조 ( 객체 아님 )
// C# 기본 구조 = namespace.class.method 
// 기본적으로 유니코드 사용 가능

namespace Basic
{
    class Basic
    {
        public static void BasicMethod()
        {
            System.Console.WriteLine("using 없이 사용");
            Console.WriteLine("using System 사용");
            WriteLine("using static");
            Write("줄 바꾸지 않음 \n");
            // cw 치고 Tab, Tab 2번 하면 Console.WriteLine 자동 채우기
            // svm Tab Tab = static void Main() 기본 골격

            // 이스케이프 시퀀스 \n \t 등 C와 비슷



            // Write Line 자리표시자
            // {} 사이의 번호 기준 인자 출력
            Console.WriteLine("{0} {1} {0}", "0번", "1번", "2번");

            // 기본 타입
            int a = 10;
            long b = 20;
            string c = "STRING";
            bool d = true; // System.Boolean
            float e = 1.1f;
            double f = 1.2;
            object g = null;

            Console.WriteLine("{0} {1} {2} {3} {4} {5} {6}", a, b, c, d, e, f, g);
            Console.WriteLine("{0}, {1}", typeof(int), typeof(Basic));
            // 기본 타입 여부 확인
            Console.WriteLine("{0}, {1}", typeof(int).IsPrimitive, typeof(Basic).IsPrimitive);


            // 타입 키워드 앞에 @붙이면 사용 가능하지만, 비추천
            int @int = 0;
            Console.WriteLine(@int);

            // 주석
            /* 주석 */
            // 리터럴 => null은 출력 안됨
            Console.WriteLine("{0}, {1}, {2}, {3} {4}", 10, 23.25f, "Literal", 'L', null);

            int Int_explicit = (int)3.1f;
            Console.WriteLine(Int_explicit);


            // 여러개 동시 선언 및 초기화 = 사용하지 않는 것이 좋음 - 가독성 좋지 않음
            int t1, t2, t3;
            t1 = t2 = t3 = 3;
            Console.WriteLine("{0},{1},{2}", t1, t2, t3);


            // 변수 표기법
            // 헝가리안 - 변수명 앞 적절한 접두사
            int intNum = 10;
            // 파스칼 - 언더스코어(_)로 구분
            int my_num = 20;
            // 카멜 - 낙타 등처럼 중간중간 대문자
            int myNumTest = 30;
            Console.WriteLine("{0} {1} {2}", intNum, my_num, myNumTest);



            // 상수(constant) = 변경불가, 선언 시 초기화
            const int MAX = 100;
            Console.WriteLine(MAX);


            // signed unsigned 부호 존재 여부
            // SIGNED  각각 8, 16 , 32 ,64 비트
            sbyte sB = -10;
            // System.SByte = 20;  닷넷형식 오류남
            short sS = -20;
            // System.Int16;
            int sI = -30;
            // System.Int32;
            long sL = -40;
            // System.Int64;

            //unsinged;
            byte usB = 10;
            // System.Byte
            // 나머지는 위의 것에 u를 붙임
            // ushort uint ulong  || System.UInt16 System.UInt32, System.UInt64
            Console.WriteLine("{0}{1}{2}{3}{4}", sB, sS, sI, sL, usB);

            // float = 32bit System.Single
            // double = 64bit System.Double
            // decimal = 128bit System.Decimal
            // 소수 float,double은 부동소수점 방식 E+28~ 이런식 표현 => 지수표기법
            // decimal은 10진 표현 => 소수 28자리까진 정확도가 높다
            double double_test = 10.20d;
            Console.WriteLine(double_test);
            // d 또는 D 붙여도 됨 , 안붙인 소수면 자동 double처리 (float는 무조건 붙여야 함=f)

            // float 은 f/F , decimal은 m/M


            // C# 7.0부터 언더스코어로 정수 숫자 3자릿수 구분 가능 ( 가독성)
            int test_num = 1_000_000;
            Console.WriteLine(test_num);

            // 최대, 최소값확인
            Console.WriteLine(uint.MaxValue);
            Console.WriteLine(int.MaxValue);
            Console.WriteLine(double.MaxValue);



            // string -> decimal   out 키워드는 추후
            decimal d_test = 0.0M;
            decimal.TryParse("12.34", out d_test);
            Console.WriteLine(d_test);

            // null 대입 가능여부
            int? int_null_1 = null;
            //int int_null_1 = null;  => 에러
            Console.WriteLine(int_null_1);



            // char기본 16bbit 유니코드 ' ' 로 가둠
            // 닷넷은 System.Char
            char cTest = '한';
            Console.WriteLine(cTest);
            System.Char cTest2 = '한';
            Console.WriteLine(cTest2);

            //문자나 문자열 묶어서 출력 $ 이용
            // $"{cTest}, {cTest2}";
            // interactive에서는 그대로 가능 = C#의 인터프리터 느낌
            Console.WriteLine($"{cTest},{cTest2}");


            //문자열
            string name = "테스터";
            Console.WriteLine(name);


            // @붙이면 C++의 로스트링처럼 이스케이프 시퀀스도 포함 가능
            string test_multiline = @"
                        hi \ @ \n
                    ";
            Console.WriteLine(test_multiline);

            // 문자열 포맷팅 3가지 방식
            // string interpolation 문자열 보간법
            string msg = "Hello";
            int int_msg = 123456;
            // $"{msg}";  모두 문자열로 처리됨
            Console.WriteLine($"{msg}, {int_msg} 문자열");

            msg = string.Format("{0} {1}", "Hello", "There");
            Console.WriteLine(msg);
            string msg1 = "Hi";
            string msg2 = "There";
            msg = string.Format($"{msg1}, {msg2}");
            Console.WriteLine(msg);

            // 문자열 + 연산자 제공
            Console.WriteLine("HI " + "THERE");


            // mutable <-> immutable
            const double PI = 3.14d;
            Console.WriteLine($"PI는 {PI}");


            // 닷넷 데이터 형식
            System.Char char_test = 'A';
            Console.WriteLine(char_test);

            // 닷넷 데이터 형식 = Wrapper Type
            // 위 기본 타입을 클래스 또는 구조체로 감싼 형식


            //날짜 형식
            Console.WriteLine(DateTime.Now);
            Console.WriteLine($"{DateTime.Now.Year} {DateTime.Now.Month}");

        }


    }
}
