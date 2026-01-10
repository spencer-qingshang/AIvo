public class ArrayMaxFinder {
    public static void main(String[] args) {
        // 定义一个包含至少5个整数的一维数组
        int[] numbers = {15, 7, 23, 10, 42, 18, 5};

        // 假设第一个元素是最大值
        int max = numbers[0];

        // 遍历数组，从第二个元素开始比较
        for (int i = 1; i < numbers.length; i++) {
            if (numbers[i] > max) {
                max = numbers[i]; // 更新最大值
            }
        }

        // 输出最大值
        System.out.println("数组中的最大值是：" + max);
    }
}
