import java.util.Scanner ;



public class Pattern {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

	
	System.out.print("Enter element : ");
        int rows = sc.nextInt();
	
	 sc.nextLine();
          
	  

        
        System.out.println("Pattern:");

        for (int i = 1; i <= rows; i++) {
            for (int j = 1; j <= i; j++) {
                System.out.print("*");
            }
            System.out.println();  
        }
    }
}