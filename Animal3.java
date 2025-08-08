class Main{
	void sound (){
		System.out.println("Animal makes sound");
	}
}
class Dog extends Main{
	void bark(){
		System.out.println("Dog bark");
}
}
class Cat extends Main{
	void meow(){
		System.out.println("Cat meow");
}
}

public class Animal3 {
public static void main(String [] args){
	Dog d= new Dog();
	d.sound();
	d.bark();
	Cat c= new Cat();
	c.sound();
	c.meow();

}

}