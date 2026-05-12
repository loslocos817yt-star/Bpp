import math
import random

def procesar(expresion):
    """
    Cerebro matemático de B++
    Soporta: +, -, *, /, **, sqrt, rand
    """
    try:
      
        expresion = expresion.strip()

      
        if expresion.startswith("sqrt:"):
            num = float(expresion.split(":")[1])
            return str(math.sqrt(num))
            
        
        if expresion.startswith("rand:"):
            rango = expresion.split(":")[1]
            min_val, max_val = map(int, rango.split("-"))
            return str(random.randint(min_val, max_val))
            
        
        resultado = eval(expresion, {"__builtins__": None}, {})
        return str(resultado)
        
    except Exception as e:
        return f"Error Matemático: {e}"
      
