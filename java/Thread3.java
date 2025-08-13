class Thread3 extends Thread {
    public void run() {
        System.out.println("Thread is under Running ... ");
        for (int i = 1; i <= 10; i++) {
            System.out.println("i = " + i);
        }
    }

    public static void main(String[] args) {
        Thread3 t1 = new Thread3();
        t1.start();
    }
}
