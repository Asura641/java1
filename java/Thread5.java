class Thread5 implements Thread{
	public void run(){
	System.out.println("Thread running");
}
public static void main(String [] args ){
	Thread5 th =new Thread5 ();
	th.run();
}
}


