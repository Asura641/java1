class Mytask implements Runnable {
	public void run(){
	for(int i=1; i<=5; i++){
		System.out.println("Task running : "+ i);
		try{	Thread.sleep(500);} catch (InterruptedException e) {}
		}
	}
}

public class RunnableDemo {

	public static void main(String[] args ){
		Runnable r= new Mytask();
		Thread t = new Thread (r);
		t.start();
	}

}