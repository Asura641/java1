class Calculator{
	void add (int a ,int b){
		System.out.println("Sum="+(a+b));
	}

	 void add (double a ,double b){
		System.out.println("Sum="+(a+b));
}

 	void add (int a ,int b, int c){
		System.out.println("Sum="+(a+b+c));}
}

public class Kanakku {
public static void main(String [] args){
	Calculator c= new Calculator();
	c.add(5,10);
	c.add(4.5,3.2);
	c.add(1,2,3);
}

}