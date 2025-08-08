import java.util.Scanner ;

class BuitInPackages{
public static void main(String[] args){
	Scanner sc = new Scanner(System.in);
	
	System.out.print("Enter Yor name : ");
        String Name = sc.nextLine();
	
	System.out.println("Hello," + Name + "!");
	sc.close();
}


}