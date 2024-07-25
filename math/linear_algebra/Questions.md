
- psi(x, y) = (x + y^2, y + x^2 + 2xy^2 + y^4). Is psi a bijective map?  (https://www.math.iitb.ac.in/~ars/MA106/slides-I.pdf)
    - yes. Solve for a bijective mapping directly
        - say psi(x, y) = (a, b)
        - then, a = x + y^2 and b = y + (x+y^2)^2 = y + a^2 => y = b - a^2
        - x = a - y^2 = a - (b - a^2)^2
        - this mapping is bijective because: 
            - surjective: for any (a, b), we can find x and y
            - injective: for any (a, b), x and y that map to (a, b) are unique. y has to be b - a^2 and x has to be a - (b - a^2)^2. No other x and y will map to (a, b)
    - this is very scary. What if finding a bijective mapping is difficult?


