# Simple Calculater, addition, subtraction, multiplication and division

def addition(a:float,b:float):
    #Adds a and b together.
    try:
        c = a+b
        return(c)
    except Exception as Error:
        return(print(Error))

def subtraction(a:float,b:float):
    #subtracts b from a.
    try:
        c = a-b
        return(c)
    except Exception as Error:
        return(print(Error))
    
def multiplication(a:float,b:float):
    #Multiply a and b.
    try:
        c = a*b
        return(c)
    except Exception as Error:
        return(print(Error))
    
def division(a:float,b:float):
    #divide a by b.
    try:    # Error handling if divition by 0
        c = a/b
        return(c)
    except Exception as Error:
        return(print(Error))
