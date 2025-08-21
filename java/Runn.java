class Runn implements Runnable {

	public void run() {
		for (int i = 0; i <= 4; i++) {
			System.out.println("Thread B" + " :" + i);
			{
			}
		}
	}
}