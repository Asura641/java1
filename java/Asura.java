class Mythread extends Thread {
    public void run() {
        try {
            for (int i = 1; i <= 5; i++) {
                System.out.println("Working" + i);
                Thread.sleep(1000);
            }

        } catch (InterruptedException e) {
            System.out.println("Thread was Interupted !");
        }
    }

}

public class Asura {
    public static void main(String args[]) {
        Mythread t1 = new Mythread();
        t1.start();
        try {
            Thread.sleep(2000);
            t1.interrupt();
        } catch (InterruptedException e) {
        }
        t1.interrupt();

    }
}
