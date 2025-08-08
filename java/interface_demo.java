// interface
interface A {
	void sound (); // abstract method 
}
// class implementing the interface
class B implements A {
	public void sound (){
		System.out.println("Dog barks");
}
} 
// Main class 
public class interface_demo {
	public static void main(String [] args ){
	B obj = new B ();
	obj.sound(); // output : Dog barks
	
	}

}