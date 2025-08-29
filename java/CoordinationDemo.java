class Mythreads extends Thread {
	public void run() {
		for (int i = 1; i <= 3; i++) {
			System.out.println(getName() + "-" + i);
			try {
				Thread.sleep(500);
			} catch (InterruptedException e) {
			}
		}
	}
}

public class CoordinationDemo {

	public static void main(String[] args) {
		Mythreads t1 = new Mythreads();
		Mythreads t2 = new Mythreads();

		t1.start();
		try {
			t1.join();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}

		t2.start();
	}
}
