abstract class BankAccount{
	double balance = 10000;
	void CalculateInterest();
}
class Savings_Acccount extends BankAccount {
	public void CalculateInterest(){
	double interest= balance *0.05;
		System.out.println("Savings Account" + interest );
	
}

}
class Current_Acccount extends BankAccount {
	public void CalculateInterest(){
	double interest= balance *0.03;
		System.out.println("Current Account" + interest );
	
}
public class Abstract_test{ 
public static void main(String [] args){

BankAccount obj = new Savings_Acccount () ;
obj.CalculateInterest();

BankAccount obj1 = new Current_Acccount () ;
obj1.CalculateInterest();
}
}