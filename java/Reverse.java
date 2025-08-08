import java.util.Scanner ;

public class Reverse {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

	
	System.out.print("Enter element : ");
        int n = sc.nextInt();
	
	 sc.nextLine();


        int reversed = 0;

        for (; n != 0; n /= 10) {
            int digit = n % 10;
            reversed = reversed * 10 + digit;
        }

        System.out.println("Reversed number: " + reversed);
    }
}