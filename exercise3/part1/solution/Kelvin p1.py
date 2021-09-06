Digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

from math import log

def base(value, old, new):
    sum10 = 0
    for i in range(len(value)):
        temp10 = Digits.index(value[i])
        if temp10 > old:                                                #Check that entered number and base is valid
            print('Entered value is not expressable in base', old)
            sum10 = 'error'
            break
        sum10 += temp10*old**(len(value)-i-1)                           #Each digit is multiplied by the appropriate base power and added

    if sum10 != 'error':
        print('The value in base 10 is', sum10)

        length = int(log(sum10, new))                                   #Determine how many digits the new number should have
        remainder = sum10
        newvalue = ''
        for i in range(length, -1, -1):
            tempnew = Digits[remainder//(new**i)]
            newvalue += tempnew
            remainder %= new**i
        print('The new value in base', new, 'is:', newvalue)
            


    
def main(): 
    value = input('Type a value to convert: ')
    old = int(input('What is the original base of the value? '))
    new = int(input('What is the new base you want to express the value? '))
    base(value, old, new)

if __name__ == '__main__':
    main()