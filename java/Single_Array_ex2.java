import java.util.*;
class Single_Array_ex2{
	public static void main(String [] args){
	Scanner sc =new Scanner(System.in);	
	int i ;
	System.out.println("Enter Array limit: ");
	i=sc.nextInt();
	int a[]=new int[i];
	System.out.println("Enter the Array value:");
	a[0]=sc.nextInt();
	a[1]=sc.nextInt();
	a[2]=sc.nextInt();
	a[3]=sc.nextInt();
	a[4]=sc.nextInt();
	int sum=0;
	for(int i=0;i<a.length;i++)
	{
	sum=sum+i;
	}
	System.out.println("The sum is "+sum);	
}
}