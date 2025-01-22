# It is a program that allows you to find GCD - LCM.

# It has no interface.

# By putting this file in the library section of Python, you can meet your EBOB-EKOK needs in your other projects.

# It has other features besides GCD - LCM.
# If you examine the codes, you will see other features!

def findPrimesUntil(num): # Returns the prime numbers up to the number you enter (including itself)
        
        # Example:
        
        # findPrimesUntil(11) = [2, 3, 5, 7, 11]
        
	prime_numbers = []
	for i in range(2, num + 1):  
		is_prime = True
		for x in range(2, i + 1):
			if i // x == i / x and not i == x:
				is_prime = False
				break
		if is_prime:
			prime_numbers.append(i)	
	return prime_numbers

def getIntegerMultipliers(num): # Returns the integer factors of the number you enter.
        
        # Example:

        # getIntegerMultipliers(12) = get

        multipliers = []
        for i in range(1, num + 1):
                if num % i == 0:
                        multipliers.append(i)            
        return multipliers

def isPrime(num): # Returns whether the number you enter is prime or not.
        
        # Example:
        
        # isPrime(5) = True
        # isPrime(6) = False
        
        return num in findPrimesUntil(num)

def getPrimeMultipliers(num): # Returns the prime factors of the number you enter.

        # Example:

        # getPrimeMultipliers(360) = [[2, 3], [3, 2], [5, 1]]
        
        prime_multipliers = []
        
        for i in findPrimesUntil(num):
                base = 1
                power = 0
                dividing = num
                while dividing % i == 0:
                        base = i
                        power += 1
                        dividing /= i
                        if dividing % i != 0:
                                prime_multipliers.append([base, power])
        
        return prime_multipliers

def gcd(e, *b): # Gives the GCD of the numbers you enter.

        # Example:
        
        # gcd(12, 18) = 6
        # gcd(12, 15, 18) = 3
        
        answer = e
        
        for i in b:
                eb = 1
                ea = getPrimeMultipliers(answer)
                ba = getPrimeMultipliers(i)
                least = ea if len(ea) < len(ba) else ba
                greatest = ba if len(ba) > len(ea) else ea
                for x in least:
                        for y in greatest:
                                if x[0] == y[0]:
                                        if x[1] < y[1]:
                                                eb *= x[0] ** x[1]     
                                        elif y[1] < x[1]:
                                                eb *= y[0] ** y[1]    
                                        else:
                                                eb *= x[0] ** x[1]
                answer = eb

        return answer

def lcm(e, *k): # Returns the LCM of the numbers you enter.
        
        # Example:

        # lcm(12, 18) = 36
        # lcm(12, 15, 18) = 180
        
        answer = e
        
        for i in k: 
                ek = 1
                ea = getPrimeMultipliers(answer)
                ka = getPrimeMultipliers(i)
                least = ea if len(ea) < len(ka) else ka
                greatest = ka if len(ka) > len(ea) else ea
                used_multipliers = []
                for x in least:
                        for y in greatest:
                                if x[0] == y[0]:
                                        if x[1] > y[1]:
                                            ek *= x[0] ** x[1]
                                        elif y[1] > x[1]:
                                            ek *= y[0] ** y[1]
                                        else:
                                            ek *= y[0] ** y[1]
                                        used_multipliers.append(x)
                                        used_multipliers.append(y)
                for x in used_multipliers:
                        if x in greatest:
                                greatest.remove(x)
                        if x in least:
                                least.remove(x)
                remaining_multipliers = greatest + least
                for x in remaining_multipliers:
                        ek *= x[0] ** x[1]
                answer = ek
        
        return answer

def isPrimeAmong(8, 10, 15): # It tells you whether the numbers you enter are relatively prime or not.
        
        # Example:

        # isPrimeAmong(5, 6) = True
        # isPrimeAmong(6, 9, 12) = False
        
        return gcd(x, *y) == 1

def getMostPrime(x, *y): # Gives a simplified version of the numbers you enter.
        
        # Example:
        
        # getMostPrime(20, 25) = [4, 5]
        
        answer = x // gcd(x, *y)
        primes = [answer]
        
        for i in y:
                answer = i // gcd(x, *y)
                primes.append(answer)
        
        return asallar
        
