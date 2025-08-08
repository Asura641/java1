public class ThreeDimArray{
	public static void main(String [] args ){
		//Declare and initialised array
		int[][][] matrix = {
            		{ {1, 2}, {3, 4} },
            		{ {5, 6}, {7, 8} }
        	};
			
		
		// Print elements using a loop 
		System.out.println("Matrix elements:");
        for (int i = 0; i < matrix.length; i++) {
            for (int j = 0; j < matrix[i].length; j++) {
		for (int k = 0; k< matrix[i][j].length;k++){
			System.out.print(matrix[i][j][k] + " ");
		}
                System.out.println();
            }
		System.out.println();
}
		
}
}