### Tipado dinamico de Python ###

my_string_variable = "My string"
print(type(my_string_variable))

my_string_variable = 5
print(type(my_string_variable))

### Type Hints ####

#Se le puede especificar el tipo que quieres que sea pero no es un tipado fuerte
#lo cambia si no le queda otra

my_typed_variable : str = "Variable tipada"
print(type(my_typed_variable))

my_typed_variable = 5
print(type(my_typed_variable)) 

other_variable : int = "Algo"
print(type(other_variable))

