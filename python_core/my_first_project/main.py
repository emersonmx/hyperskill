bubblegum = 202
toffee = 118
ice_cream = 2250
milk_chocolate = 1680
doughnut = 1075
pancake = 80
income = bubblegum + toffee + ice_cream + milk_chocolate + doughnut + pancake

print("Earned amount:")
print("Bubblegum: $" + str(bubblegum))
print("Toffee: $" + str(toffee))
print("Ice cream: $" + str(ice_cream))
print("Milk chocolate: $" + str(milk_chocolate))
print("Doughnut: $" + str(doughnut))
print("Pancake: $" + str(pancake))
print("Income: $" + str(income))

staff_expenses = int(input("Staff expenses:\n"))
other_expenses = int(input("Other expenses:\n"))

print("Net income: $" + str(income - staff_expenses - other_expenses))
