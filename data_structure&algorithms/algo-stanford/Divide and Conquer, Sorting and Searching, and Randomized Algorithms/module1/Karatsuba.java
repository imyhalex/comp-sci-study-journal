class Karatsuba { 

    Karatsuba() { }

    static long karatsubaMultiply(long num1, long num2) { 
        if (num1 < 10 || num2 < 10)
            return num1 * num2;
        
        int m = Math.max(Long.toString(num1).length(), Long.toString(num2).length());
        int m2 = m / 2;

        // perfrom split at m2
        long high1 = num1 / (long) Math.pow(10, m2);
        long low1 = num1 % (long) Math.pow(10, m2);
        long high2 = num2 / (long) Math.pow(10, m2);
        long low2 = num2 % (long) Math.pow(10, m2);

        long z2 = karatsubaMultiply(high1, high2);
        long z0 = karatsubaMultiply(low1, low2);
        long z1 = karatsubaMultiply(low1 + high1, low2 + high2) - z2 - z0;
        
        return (z2 * (long) Math.pow(10, 2 * m2)) + (z1 * (long) Math.pow(10, m2)) + z0;
    }

    public static void main(String[] args) {
        long num1 = 1234;
        long num2 = 5678;

        long result = karatsubaMultiply(num1, num2);

        System.out.println("Product of " + num1 + " and " + num2 + " is " + result);
    }
}