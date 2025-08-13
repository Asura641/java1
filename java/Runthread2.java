public class Runthread2 implements Runnable {
    public void run() {
        System.out.println("Thread is under Running ... ");
        for (int i = 1; i <= 10; i++) {
            System.out.println("i = " + i);
        }
    }

    public static void main(String args[]) {
       Runthread2 OBJ = new Runthread2();
        Thread thread = new Thread(OBJ);

        System.out.println("Thread about to start ... ");
        thread.start();
    }
}
