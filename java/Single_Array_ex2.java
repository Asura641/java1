import java.util.*;
class Single_Array_ex2{
	public static void main(String [] args){
	Scanner sc =new Scanner(System.in);	
	int i ;
	System.out.println("Enter Array limit: ");
	int n = sc.nextInt();   
        int a[] = new int[n];
	System.out.println("Enter the Array values:");
        for ( i = 0; i < a.length; i++) {
            a[i] = sc.nextInt();   
        }
	int sum=0;
	for( i=0;i<a.length;i++)
	{
	sum=sum+a[i];
	}
	System.out.println("The sum is "+sum);	
}
}