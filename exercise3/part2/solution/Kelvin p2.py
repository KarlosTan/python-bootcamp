init_coins = 10
no_stocked = 10

#Process:
#Basically same as exercise 2, but variables are now attached to the class.
#1. Print Menu
#2. Ask to select items multiple times. On first attempt can quit or perform maintenance
#3. Check if order is above limit, otherwise go to payment
#4. Ask for coin input. These are counted and added to the coin pool. Items are reduced from the stock pool
#5. Return change if necessary
#6. Repeat

class VendingMachine:
    def __init__(self):
        self.itemlist = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']
        self.itemcost = [0.75, 1.20, 1.20, 1.00, 1.50, 0.95, 1.10, 0.50, 1.20]
        self.stock = [no_stocked]*len(self.itemlist)
        self.denomination = [1, 0.5, 0.2, 0.1, 0.05]
        self.coins = [init_coins]*len(self.denomination)
        self.sold = [0]*len(self.stock)     #Total number sold
        self.balance = 0
        self.income = 0
        self.order = []                     #Current order. Flows into sales
        self.sales = []                     #Sales of current order. Flows into sold after order complete
        self.total = 0                      #Total cost of current order
        self.owe = 0                        #Amount owed in current order
        self.cont = True                    #Should the transaction continue. Turns to False if asked to quit
        self.reset = False                  #Should the vending machine reset. True when run maintenance
        
    def set_properties(self, item, cost, denom):
        self.itemlist = item
        self.itemcost = cost
        self.denomination = denom
        
    def ShowMenu(self):
        print('Vending Machine')
        print('+-------------+-------------+-------------+')
        print('|    Water    |     Coke    |  Diet Coke  |')
        print('|    $0.75    |    $1.20    |    $1.20    |')
        print('|     A1      |     A2      |     A3      |')
        print('+-------------+-------------+-------------+')
        print('|  Iced Tea   |  Chocolate  |    Candy    |')
        print('|    $1.00    |    $1.50    |    $0.95    |')
        print('|     B1      |     B2      |     B3      |')
        print('+-------------+-------------+-------------+')
        print('|    Chips    |     Gum     |Turk. Delight|')
        print('|    $1.10    |    $0.50    |    $1.20    |')
        print('|     C1      |     C2      |     C3      |')
        print('+-------------+-------------+-------------+')
        print('|        +----------------------+         |')
        print('|        |                      |         |')
        print('|        +----------------------+         |')
        print('+-----------------------------------------+')   
               
    def SalesSummary(self):
        for i in range(len(self.stock)):
            self.sold[i] = no_stocked - self.stock[i]                   #Calculate missing stock
            print('Sold', self.sold[i], 'units of', self.itemlist[i])
            self.stock[i] = no_stocked                                  #Reset stock levels in same loop
        for i in range(len(self.denomination)):
            self.balance += self.coins[i] * self.denomination[i]        #Calculate money in the machine
            self.coins[i] = init_coins                                  #Reset number of coins
        print('There is a balance of', self.balance)

        for i in range(len(self.itemcost)):
            self.income += self.sold[i] * self.itemcost[i]              #Calculate total income
        print('Total income of $', self.income)
        input('Press the enter key to continue: ')
        self.reset = True
        self.ShowMenu()
    
    def Payment(self):
        self.sales = []
        for item in self.itemlist:
            self.sales.append(self.order.count(item))                   #Count number of times each item appears in list typos not counted
        for i in range(len(self.sales)):
            self.total += round(self.sales[i]*self.itemcost[i], 2)      #Total cost of selection

    def MakeSelection(self):
        if len(self.order) == 0:                                        #Displays only on first run to quit or maintenance
            selection = input('Please select a product by typing its code or enter q to quit: ')
            if selection != 'q':                                        #Stop if quit
                if selection == '99':                                   #Maintenance password
                    code = input('*') #Super secret pin code
                    if code == 'password':
                        self.SalesSummary()
                    else:
                        self.MakeSelection()  
                else:
                    self.order.append(selection)
                    self.MakeSelection()
            else:
                self.cont = False
        else:
            print('Your current order is: ', self.order)                #Display current order and ask for additional orders
            additional = input('Type another code to add to your order or enter n to proceed to payment: ')
            if additional != 'n':                                       #Output order for payment
                self.order.append(additional)                           #Run order process again
                self.MakeSelection()

    def ReturnChange(self):
        for i in range(len(self.coins)):
            num = 0
            num = min(self.coins[i], round(self.owe, 2)//self.denomination[i])              #Returns as many high denominations as possible. Limited by number of coins left
            if num > 0:
                print('Change owed:', round(self.owe,2))                                    #Python has strange rounding errors
                print('*The machine spits out', num, self.denomination[i], 'piece(s)')
                self.coins[i] -= num
            self.owe -= num*self.denomination[i]
        print('Thanks for using the vending machine.')
        self.order = []
        self.total = 0

    def DisplayErrorMessage(self):
        for i in range(len(self.sales)):
            if self.sales[i] > self.stock[i]:                           #Check if sufficient stock
                print('Insufficient stock on product', self.sales[i], 'please reduce amount by', self.sales[i]-self.stock[i], 'units.')
                print('Order resetting...')
                self.order = []                                         #Clears current order to try again
                self.MakeSelection()
        print('Your total is $', self.total)                            #If successful, count amount owed
        amount = 0
        while True:
            try:
                coin = float(input('Insert (by typing) each coin: '))
                ind = self.denomination.index(coin)                     #Determine if correct denomination entered
            except ValueError:
                print('Invalid coin')
            else:
                self.coins[ind] += 1                                    #Add inserted coin to the coin pool
                amount += coin                                          #Sum the total money inserted
                self.owe = round(self.total - amount, 2)
                if self.owe > 0:                                        #Stop asking for money once there is enough money to pay
                    print('Amount owing:', self.owe)
                else:
                    for i in range(len(self.sales)):
                        self.stock[i] -= self.sales[i]                  #Reduce stock by the number of items purchased
                        print('Processing order...')
                    self.owe = -self.owe
                    break
    
class MachineList(VendingMachine):
    def __init__(self, city, address, manage):
        super().__init__()
        self.id = city
        self.address = address
        self.manage = manage

A = MachineList('Syd', 'First Ave', 'Adam')
B = MachineList('Bri', 'Second Ave', 'Bob')
C = MachineList('Mel', 'Third Ave', 'Chris')

def main():
    Choose = input('Select a city A, B or C: ')
    a = globals()[Choose]                       #Turn selection into the correct vending machine chosen
    a.MakeSelection()
    if a.reset:
        a.reset = False
        main()
    if a.cont:
        a.Payment()
        a.DisplayErrorMessage()
        a.ReturnChange()
        main()

if __name__ == '__main__':
    main()