class Thread2 extends Thread {
    public void run() {
        int a = 10;
        int b = 20;
        System.out.println(a + b);
    }

    public static void main(String args[]) {
        Thread2 t1 = new Thread2();
        t1.start();
    }
}
