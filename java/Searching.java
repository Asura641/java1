class Searching{
	public static void main(String [] args){
	
	int [] A  ={1,2,5,4,6};
	int key = 6;
		 for (int i = 0; i < A.length; i++) {
			if (A[i] == key) 
			{
			 System.out.println("Found at index " + i); 	
			return; 	
			}
            System.out.println(A[i]);
        }
    }
}