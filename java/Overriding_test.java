class Employee {
	void work(){
	System.out.println("employee Work");
}
}
class Developer extends Employee{
		void work(){
		
		System.out.println("Developer");
	}
}
class Manager extends Employee{
		void work(){
		
		System.out.println("Manager");
	}
}
public class Overriding_test{
public static void main(String [] args){
 Developer ob1 = new Developer ();
ob1.work();
Manager ob2 = new Manager ();
ob2.work();	

}
}