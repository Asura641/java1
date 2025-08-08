abstract class Vehicle{ 
 	 public Vehicle() { 
 	 System.out.println("Car"); 
 	 
 }
 
 
 	 abstract void Move(); 
 }
 class Car extends Vehicle { 
 	 public void Move(){
 	 	 System.out.println("Car crash"); 
 }
 }
 public class Abstract1{
 public static void main(String [] args){
 
 Vehicle obj = new Car() ;
 obj.Move();
 
 }
 }