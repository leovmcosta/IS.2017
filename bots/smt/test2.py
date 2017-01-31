import kb, sys
from kb import KB, Boolean, Integer, Constant

# Define our integer symbols
x = Integer('x')
y = Integer('y')
z = Integer('z')

# sum = x + y
# print(sum)
#
a = x + y + z > 1
# print(constraint)

b = 1 < x + y + z
# print(constraint)

c = x - (z + y) < x - (y - z)
# print(constraint)

q = 15
d = q * x  == x - (y - q * z)
# print(constraint)

# Create a new knowledge base
kb = KB()

# Add clauses
kb.add_clause(a)
kb.add_clause(b)
kb.add_clause(c)
kb.add_clause(d)

# Print all models of the knowledge base
for model in kb.models():
    print(model)

# Print out whether the KB is satisfiable (if there are no models, it is not satisfiable)
print(kb.satisfiable())
