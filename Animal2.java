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
class Puppy extends Dog{
	void weep(){
		System.out.println("Puppy weep");
}
}

public class Animal2 {
public static void main(String [] args){
	Puppy d=new Puppy();
	d.sound();
	d.bark();
	d.weep();


}

}