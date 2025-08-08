class Student{
	String name;
   Student(String name){
	this.name=name; //this.name ->instance variable 
			//name	    ->constructor parameater 
}
 void display(){
	System.out.println("Student name:" +name);

}	

}
public class Main {
	public static void main(String[] args){
	Student s = new Student("Asura666");
	s.display();
}

}