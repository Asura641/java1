class MathOperation{
	void multiply(int a, int b){
System.out.println("Result="+(a*b));

}
	void multiply(float a, float b){
System.out.println("Result="+(a*b));
}
	
	void multiply(int a, int b ,int c){
System.out.println("Result="+(a*b*c));
}


public static void main(String [] args ){

MathOperation c = new MathOperation();
c.multiply(1,2);
c.multiply(4,2f);
c.multiply(1,2,3);




}
		
}

