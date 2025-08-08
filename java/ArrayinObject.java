public class ArrayinObject {
	String name;
    	int age;

       public ArrayinObject(String name, int age) {
        this.name = name;
        this.age = age;
    }

       public void display() {
        System.out.println("Name: " + name + ", Age: " + age);
    }
    public static void main(String[] args) {
               ArrayinObject[] students = new ArrayinObject[3];

        
        students[0] = new ArrayinObject("Dracula", 18);
        students[1] = new ArrayinObject("Asura", 19);
        students[2] = new ArrayinObject("Kratos", 17);

        
        for (int i = 0; i < students.length; i++) {
            students[i].display();
        }
    }
}
