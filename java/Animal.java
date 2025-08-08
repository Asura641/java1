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
public class Animal {
public static void main(String [] args){
	Dog d=new Dog();
	d.sound();
	d.bark();


}

}