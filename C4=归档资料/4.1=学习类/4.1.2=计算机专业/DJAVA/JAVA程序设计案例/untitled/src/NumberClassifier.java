import java.util.Scanner;

public class NumberClassifier {
    public static void main(String[] args) { // 将执行逻辑放入main方法
        Scanner sc = new Scanner(System.in);
        System.out.println("请输入一个整数："); // 提示用户输入
        int i = sc.nextInt();

        if (i > 0) {
            System.out.println("这是一个正数");
        } else if (i < 0) {
            System.out.println("这是一个负数");
        } else {
            System.out.println("这是零");
        }
        sc.close(); // 关闭Scanner，释放资源
    }
}