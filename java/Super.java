class Animal {
String color =" Brown"; 

}
class Dog extends Animal {
String color =" Black"; 
void printColor(){
System.out.println("Dog color :" +color);
System.out.println("Animal color :" +super .color);


}

}
public class Super {
public static void main(String [] args){
	Dog d= new Dog();
	d.printColor();
}
}