class karatsuba:
    def __init__(self):
        pass 

    def karatsuba_multiply(num1, num2):
        if num1 < 10 or num2 < 10:
            return num1 * num2
        
        m = max(len(str(abs(num1))), len(str(abs(num2))))
        m2 = m // 2

        high1 = num1 // pow(10, m2)
        low1 = num1 % pow(10, m2)
        high2 = num2 // pow(10, m2)
        low2 = num2 % pow(10, m2)

        z2 = karatsuba.karatsuba_multiply(high1, high2)
        z0 = karatsuba.karatsuba_multiply(low1, low2)
        z1 = karatsuba.karatsuba_multiply(low1 + high1, low2 + high2) - z2 - z0

        return (z2 * pow(10, 2 * m2)) + (z1 * pow(10, m2)) + z0
    
if __name__ == "__main__":
    # Test the implementation with the same numbers as the Java version
    num1 = 3141592653589793238462643383279502884197169399375105820974944592
    num2 = 2718281828459045235360287471352662497757247093699959574966967627
    
    # Calculate the result using our Karatsuba multiplication
    result = karatsuba.karatsuba_multiply(num1, num2)
    
    # Print the result
    print(f"Product of {num1} and {num2} is {result}")

