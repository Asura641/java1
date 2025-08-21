class MyTask implements Runnable {
    private String taskName;

    MyTask(String name) {
        this.taskName = name;
    }

    public void run() {
        for (int i = 1; i <= 5; i++) {
            System.out.println(taskName + " - Count: " + i);
            try {
                Thread.sleep(500);
            } catch (InterruptedException e) {
                e.printStackTrace();

                System.out.println(taskName + " finished.");
            }
        }
    }

    public class MultiThreadRunnableDemo {
        public static void main(String[] args) {
            MyTask task1 = new MyTask("Task 1");
            MyTask task2 = new MyTask("Task 2");

            Thread t1 = new Thread(task1);
            Thread t2 = new Thread(task2);

            t1.start();
            t2.start();
        }
    }
}