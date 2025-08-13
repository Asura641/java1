public class Runthread1 implements Runnable {
    public void run() {
        System.out.println("thread is running ... ");
    }

    public static void main(String args[]) {
        Runthread1 m1 = new Runthread1();
        Thread t1 = new Thread(m1);
        t1.start();
    }
}
