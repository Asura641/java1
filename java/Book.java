class Book {
	String title;
	Book(String title){
		this.title=title;
	}

public static void main(String [] args ){

	Book[] book = new Book[5];
	book[0] = new Book("Dune");
	book[1] = new Book("The Game of Thrones");
	book[2] = new Book("Harry Potter");
	book[3] = new Book("THE WITCHER");
	book[4] = new Book("THE LORD OF THE RINGS");
	for (Book b : book){
		System.out.println(b.title);
		}

	}
}	