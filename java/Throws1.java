import java .io.*;


class Throws1{
	static void readFile () throws IOExeption {
		FileReader fr = new FileReader("file.txt");
		


}
	public static void main(String [] args  ){

	try {
		readFile();
			
	}catch(IOException e){
		System.out.println("File not found or error reading file");
	}


}
}
