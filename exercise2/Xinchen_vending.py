import decimal
decimal.getcontext().prec = 4

class VendingMachine:
    
    def __init__(self):
        # New items can be added here.
        # Value list stands for price and amountn respectively.
        self.item_price = {
            'Water': [0.75, 10, 1],
            'Coke': [1.20, 10, 2],
            'Diet Coke': [1.20, 10, 3],
            'Iced Tea': [1.00, 10, 4],
            'Swiss Chocolate': [1.50, 10, 5],
            'Candy': [0.95, 10, 6],
            'Chips': [1.10, 10, 7],
            'Bubble Gum': [0.50, 10, 8],
            'Turkish Delight': [1.20, 10, 9],
            'End of Transaction': ['', '', 10],           
        }
        
        # Coin denomination can be modified here.
        self.coins = [100, 50, 20, 10, 5]
        
        # Each denomination has 5 coins initially.
        self.num_coins = [5, 5, 5, 5, 5]
        
        
    def show_menu(self):
        # value[0] stands for price.
        # value[1] stands for amount.
        # value[2] stands for No.
        for item, value in self.item_price.items():
            if item == "End of Transaction":
                # do not print "$"
                print(f"{value[2]}. {item}".ljust(25))
            else:
                # ljust(25) is used to align left and total length is 25.
                print(f"{value[2]}. {item}".ljust(25) + f"${value[0]}")
            
    def make_selection(self):
        # The sum price of all of the items selected.
        price_sum = decimal.Decimal(0)
        # User deposit coins here.    
        message = "Please deposit your coins: "
        current_balance = decimal.Decimal(input(message))        
        # While loop is used to let the user select items
        # For loop is used to loop items in the item_price dictionary.
        while(True):
            message = "Please make your selection: "
            selection = int(input(message))
            # Value[0] stands for the price of the item.
            # Value[1] stands for the amount of the item.
            # Value[2] stands for the item No.
            for item, value in self.item_price.items():
                # Selection = 10 means the end of Transaction on the menu.
                # Then stops the selection part and return change amount
                if selection == 10:
                    return current_balance - price_sum
                # Maintenance part.
                elif selection == 99:
                    # Program will sum the balance and restore the items
                    # only when the for loop reaches the last choice 
                    # "End of Transaction".
                    # Otherwise, it will print the result and restore every time
                    # during the for loop.
                    if item == "End of Transaction":
                        # Print the coins left.
                        for a in range(0, 5):
                            num_coins_given = 5 - self.num_coins[a]
                            message = f"{self.coins[a]} cents coin has been given "
                            temp = "piece" if num_coins_given <= 1 else "pieces"
                            message += f"{num_coins_given} {temp}." 
                            print(message)
                        # Restore the items.   
                        for value in self.item_price.values():
                                value[1] = 10
                        break
                    else:
                        # Since "Water" is the No.1 item, print 
                        # "Items sold: " at the beginning.
                        if item == "Water":
                            print("Items sold: ")
                        # Print the item name and sold amount
                        print(f"{item}".ljust(25) + f"{10 - value[1]}")
                        # Since "Turkish Delight" is the last item, print
                        # the total income here for once.
                        if item == "Turkish Delight":
                            print(f"Total income: ${price_sum}.") 
                # Once selection equals to value[2], which is the item No.,
                # the selection and the No. matches.
                # Then price will be added to the sum and this item's
                # amount will be decreased by 1.
                # Then break the for loop and continue the selection in the menu.
                elif selection == value[2]:
                    # When the item amount is 0, machine will tell
                    # the user that this item is out of sold.
                    if value[1] == 0:
                        print(f"{item} is out of sold!")
                    else:
                        price_sum += decimal.Decimal(value[0])
                        # If the current balance can't cover the prices of items,
                        # ask users to top up new coins.
                        if price_sum > current_balance:
                            message = f"Please top up ${price_sum - current_balance}"
                            message += " amount of coins for your new selection: "
                            current_balance += decimal.Decimal(input(message))   
                        # Amount of the item will be decreased by 1
                        # after new coins deposited or current balance
                        # is enough to cover the prices 
                        value[1] -= 1
                    # Break the for loop to continue the while loop
                    break
                # The program runs to this position implying that
                # current value[2] does not equal to the selection.
                # Then just continue the for loop, till the value[2]
                # matches the selection.
                elif value[2] < 10: 
                    continue
                # Program will print an error message if the 
                # selection is beyond the item number range.
                else:
                    print("Wrong selection!")
                    break
                
    def return_change(self):
        # Change amount got from make_selection().
        change_amount = decimal.Decimal(100) * self.make_selection()
        # self.coins = [100, 50, 20, 10, 5]
        # self.num_coins = [5, 5, 5, 5, 5]
        for i in range(0, 5):
            # Get the number of each coin denomination.
            coin_num = change_amount // decimal.Decimal(self.coins[i])
            # Number needed is larger than the balance.
            if coin_num > self.num_coins[i]:
                # Reaches the smallest denomination -- "$5".
                # And number of coins required is still larger.
                if i == 4:
                    message = "Sorry, the machine balance is not enough"
                    message += " to cover your change. And the transaction"
                    message += " is cancelled."
                    print(message)
                # Not reaches the "$5" yet and continues.
                else: 
                    continue
            elif self.num_coins[i] != 0:
                if i == 0:
                    print("Here are your changes: ")
                self.num_coins[i] - coin_num
                change_amount -= self.coins[i] * coin_num
                print(f"${self.coins[i]}".ljust(10) + f"{coin_num}")

def main():    
    vd = VendingMachine()
    vd.show_menu()
    vd.return_change()

if __name__ == '__main__':
    main()