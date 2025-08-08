abstract class Animal{
	abstract void sound();//abstract method
	void eat (){
		System.out.println("This animal eats food");
}
}
class Dog extends Animal{
	void sound (){
		System.out.println("Dog barks");
}
}
public class Abs{
	public static void main (String [] args){	
	Dog d = new Dog () ;
	d.sound(); // Dog barks
	d.eat(); //This animal eats food
}
}