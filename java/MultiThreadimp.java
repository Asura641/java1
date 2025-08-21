class RunnableWorker implements Runnable {
	public void run() {
		for (int i = 0; i <= 4; i++) {
			System.out.println("Thread A " + " : " + i);
		}
	}

}



public class MultiThreadimp {
	public static void main(String[] args) {
		RunnableWorker r = new RunnableWorker();
		Runn l = new Runn();
		Thread t1 = new Thread(r);
		Thread t2 = new Thread(l);
		t1.start();
		t2.start();

	}
}