package Calculator;

import java.util.Scanner;

public class Calculator {
    public void start() {
        Scanner sc = new Scanner(System.in);

        System.out.print("Enter first number: ");
        double num1 = sc.nextDouble();

        System.out.print("Enter second number: ");
        double num2 = sc.nextDouble();

        
        double result = 0;

        double  i= num1+num2;
	double  j= num1-num2;
	double  k= num1*num2;
	
        System.out.println("Result: " + i);
	System.out.println("Result: " + j);
	System.out.println("Result: " + k);

        sc.close();
    }
}
