print("How many pencils would you like to use:")
pencils = int(input())

players = ["John", "Jack"]
print(f"Who will be the first ({', '.join(players)}):")
player = input()

print("|" * pencils)
print(f"{player} is going first!")
