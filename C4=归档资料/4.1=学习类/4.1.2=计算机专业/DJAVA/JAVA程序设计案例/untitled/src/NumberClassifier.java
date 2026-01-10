import java.util.Scanner;

public class NumberClassifier {
    Scanner sc = new Scanner(System.in);
    int i = sc.nextInt();
    if (i > 0) {
        System.out.println("正数");
    } else if (i < 0) {
        System.out.println("负数");
    } else
    {
        System.out.println("0");
    }
}
