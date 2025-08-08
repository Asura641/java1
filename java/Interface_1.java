interface Printable {
	void print();

	

}
 class Document implements Printable{
	public void print(){
		System.out.println("Hello");
	}
}



class Image extends Document{
		public void print(){
		System.out.println("Hi");
	}

}
public class Interface_1{
public static void main(String [] args){

Image obj = new Image () ;
obj.print();
}


}