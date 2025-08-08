import java.util.Scanner;

class fact{
public static void main(String [] args){
	Scanner sc = new Scanner(System.in);
        
        System.out.print("Enter the value: ");
        int a = sc.nextInt();


	int mul = 1;
		
	for (int i = 1; i <= a; i++) {
		mul=mul*i;
}
System.out.println("factorial: " +mul);


}

}