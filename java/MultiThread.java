class A extends Thread {
	public void run(){
		for (int i =1 ; i <=5; i++){
		
		System.out.println("\tFrom Thread A : i="+i);
	}
		System.out.println("Exit from A");
}

}
class B extends Thread{
	public void run(){
	for (int i =1;i<=5;i++){
	System.out.println("\t From Thread B:i= " +i);
	}
	System.out.println("Exit from B");
}

}
class C extends Thread{
	public void run(){
	for (int i =1;i<=5;i++){
	System.out.println("\t From Thread C:i= " +i);
	}
	System.out.println("Exit from C ");
}

}
class MultiThread{
	public static void main(String [] args){

	A a=new A();
	a.start();
	B b=new B();
	b.start();
	C c=new C();
	c.start();
}
}