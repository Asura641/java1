public class ArraywithinClass {
	String name;
	int[] marks;

	public ArraywithinClass(String studentName,int[] studentMarks) {
        
	this.name = studentName;
	this.marks = studentMarks; 
    }
	public void displayMarks() {
	System.out.println("Name: " + name);
        System.out.println("Student Marks:");
        for (int mark : marks) { 
            System.out.println(mark);
        }
    }
	
    public static void main(String[] args) {
	String name = "Abhishek"; 
	int[] marks = new int[]{85, 90, 78}; 
        ArraywithinClass s1 = new ArraywithinClass(name,marks);       
        
	s1.displayMarks();                
    }
}
