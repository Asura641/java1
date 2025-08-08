class Animal{
	void sound (){
		System.out.println("Animal makes sound");
	}
}
class Dog extends Animal{
	void sound(){
		System.out.println("Dog bark");
}
}
class Cat extends Animal{
	void sound(){
		System.out.println("Cat meow");
}
}

public class Mrugam {
public static void main(String [] args){
	Cat c= new Cat();
	c.sound();
	

}

}