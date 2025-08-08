public class MultiDimArray{
	public static void main(String [] args ){
		//Declare and initialised array
		int[][] matrix = {{1, 2}, {3, 4}};
			
		
		// Print elements using a loop 
		System.out.println("Matrix elements:");
        for (int i = 0; i < matrix.length; i++) {
            for (int j = 0; j < matrix[i].length; j++) {
                System.out.print(matrix[i][j] + " ");
            }
		System.out.println();
}
		
}
}