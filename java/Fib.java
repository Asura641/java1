import java .util.Scanner;
class Fib {
	public static void main (String [] args){
	Scanner sc = new Scanner (System.in);
	System.out.print("Enter the limit: ");
	int A =sc.nextInt();
	
	int c=0;
	int d=1;
 System.out.println(c) ;
 System.out.println(d) ;

for (int i = 2; i<=A ; i++){
	int e= c+d;
System.out.println(" " +e) ;
c=d;
d=e;
}

	
		

}


}