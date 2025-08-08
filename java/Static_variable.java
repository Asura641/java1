class Static_variable {
	int id ;
	String name ;
	static String  college ="ABC College"; // shared by all 
	Static_variable(int i, String n){
	id = i;
	name =n;
}
	void display(){
	System.out.println(id+ " " +name+" "+college);

}


	public static void main(String[] args){
		Static_variable s1 = new Static_variable(1,"ASURA");
		Static_variable s2 = new Static_variable(2,"Kartos");
s1.display();
s2.display();

}
}
