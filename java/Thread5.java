class Thread5 implements runnable{
	public void run(){
	System.out.println("Thread running");
}
public static void main(String [] args ){
	Thread5 th =new Thread5 ();
	th.start();
}
}


