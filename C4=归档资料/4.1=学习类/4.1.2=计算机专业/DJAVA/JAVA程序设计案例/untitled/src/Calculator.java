
public class Calculator {
    public static void main(String[] args) {
        // 定义两个整型变量a和b
        int a = 10;
        int b = 3;

        // 计算商（整数部分）
        int quotient = a / b;
        // 计算余数
        int remainder = a % b;

        // 将结果输出到控制台
        System.out.println("a 除以 b 的商是：" + quotient); // 输出商
        System.out.println("a 除以 b 的余数是：" + remainder); // 输出余数
    }
}
