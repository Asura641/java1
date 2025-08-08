public class MultiDimArray {
    public static void main(String[] args) {
        // Declare and initialize the 2D array (matrix)
        int[][] matrix = {{1, 2}, {3, 4}};

        // Print matrix elements
        System.out.println("Matrix elements:");

        // Loop through rows
        for (int i = 0; i < matrix.length; i++) {
            // Loop through columns
            for (int j = 0; j < matrix[i].length; j++) {
                System.out.print(matrix[i][j] + " "); // Print element and a space
            }
            System.out.println(); // Move to the next line after printing each row
        }
    }
}