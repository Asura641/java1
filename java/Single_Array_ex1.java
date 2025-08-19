import java.util.*;
class Single_Array_ex1{
	public static void main(String [] args){
	Scanner sc =new Scanner(System.in);	
	int a[] = new int [10];	
	int i ;
	System.out.println("Enter 10 numbers: ");
	for(i=0 ; i < 10; i++){

	a[i]=sc.nextInt();

}
	System.out.println("List of even number");
	for(i=0;i<10;i++){
	if(a[i]%2==0)
	{
	System.out.println(a[i]+"");
	}

}
}
}