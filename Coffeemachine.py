class CoffeeMachine:
    class State:
        MAIN = "MAIN"
        BUY = "BUY"
        FILL_WATER = "FILL_WATER"
        FILL_MILK = "FILL_MILK"
        FILL_BEANS = "FILL_BEANS"
        FILL_CUPS = "FILL_CUPS"
        EXIT = "EXIT"

    def __init__(self):
        self.state = self.State.MAIN
        self.supplies = {
            "water": 400,
            "milk": 540,
            "coffee beans": 120,
            "disposable cups": 9,
            "money": 550,
        }

    def process_input(self, input_str):
        if self.state == self.State.MAIN:
            return self._handle_main(input_str)
        elif self.state == self.State.BUY:
            return self._handle_buy(input_str)
        elif self.state == self.State.FILL_WATER:
            return self._handle_fill_water(input_str)
        elif self.state == self.State.FILL_MILK:
            return self._handle_fill_milk(input_str)
        elif self.state == self.State.FILL_BEANS:
            return self._handle_fill_beans(input_str)
        elif self.state == self.State.FILL_CUPS:
            return self._handle_fill_cups(input_str)
        return ""

    def _handle_main(self, cmd):
        if cmd == "buy":
            self.state = self.State.BUY
            return ""
        elif cmd == "fill":
            self.state = self.State.FILL_WATER
            return ""
        elif cmd == "take":
            taken = self.supplies["money"]
            self.supplies["money"] = 0
            return f"I gave you ${taken}"
        elif cmd == "remaining":
            return self._status()
        elif cmd == "exit":
            self.state = self.State.EXIT
            return ""
        else:
            return "Invalid input"

    def _handle_buy(self, choice):
        if choice == "back":
            self.state = self.State.MAIN
            return ""

        recipes = {
            "1": {"water": 250, "milk": 0, "coffee beans": 16, "disposable cups":1, "money": -4},  # espresso
            "2": {"water": 350, "milk": 75, "coffee beans": 20, "disposable cups":1, "money": -7},  # latte
            "3": {"water": 200, "milk": 100, "coffee beans": 12, "disposable cups":1, "money": -6},  # cappuccino
        }
        if choice not in recipes:
            return "Invalid choice"

        check = self._check_resources(recipes[choice])
        if check == "I have enough resources, making you a coffee!":
            for item in recipes[choice]:
                self.supplies[item] -= recipes[choice][item]
        return check

    def _handle_fill_water(self, val):
        self.supplies["water"] += int(val)
        self.state = self.State.FILL_MILK
        return ""

    def _handle_fill_milk(self, val):
        self.supplies["milk"] += int(val)
        self.state = self.State.FILL_BEANS
        return ""

    def _handle_fill_beans(self, val):
        self.supplies["coffee beans"] += int(val)
        self.state = self.State.FILL_CUPS
        return ""

    def _handle_fill_cups(self, val):
        self.supplies["disposable cups"] += int(val)
        self.state = self.State.MAIN
        return ""

    def _check_resources(self, recipe):
        for item in recipe:
            if self.supplies[item] < recipe[item]:
                self.state = self.State.MAIN
                return f"Sorry, not enough {item}!"
        self.state = self.State.MAIN
        return "I have enough resources, making you a coffee!"

    def _status(self):
        return (f"""The coffee machine has:\n{self.supplies["water"]} ml of water\n
            {self.supplies["milk"]} ml of milk\n
            {self.supplies["coffee beans"]} g of coffee beans\n
            {self.supplies["disposable cups"]} disposable cups\n
            {self.supplies["money"]} of money\n""")

if __name__ == "__main__":
    machine = CoffeeMachine()

    while machine.state != machine.State.EXIT:
        if machine.state == machine.State.MAIN:
            print("Write action (buy, fill, take, remaining)")
        elif machine.state == machine.State.BUY:
            print("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:")
        elif machine.state == machine.State.FILL_WATER:
            print("Write how many ml of water you want to add:")
        elif machine.state == machine.State.FILL_MILK:
            print("Write how many ml of milk you want to add:")
        elif machine.state == machine.State.FILL_BEANS:
            print("Write how many beans you want to add:")
        elif machine.state == machine.State.FILL_CUPS:
            print("Write how many cups you want to add:")

        user_line = input().lower().strip()
        output = machine.process_input(user_line)
        if output:
            print(output)
