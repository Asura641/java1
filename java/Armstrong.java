class Armstrong {
    public static void main(String[] args) {
        int n =407 ;
	int sum =0 ; 
	int temp =n;

        for (; n > 0; n /= 10) {
            int r = n % 10;
            sum += r * r * r;
        }

        System.out.println(sum == temp );
    }
}
