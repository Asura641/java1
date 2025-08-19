class Thread5 implements Runnable{
	public void run(){
	System.out.println("Thread running");
}
public static void main(String [] args ){
	Thread5 th =new Thread5 ();
	Thread t =new Thread (th);
	t.start();
}
}


