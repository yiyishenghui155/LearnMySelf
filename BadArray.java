public class BadArray {
    private static int[] store = new int[4];

    public static void putData(int pos, int num) {
        if (pos < 0) {
            return;
        }
        store[pos] = num;
    }

    public static void main(String[] args) {
        putData(5, 100);
    }
}