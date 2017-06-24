from lunisolar import ChineseDate

lottery_numbers = []

f = open("lottery_numbers", 'r')
for line in f.readlines():
    number = []
    numberInfo = line.split()
    year = int(numberInfo[0])
    month = int(numberInfo[1])
    day = int(numberInfo[2])
    moon_landing = ChineseDate.from_gregorian(year, month, day)
    number.append(moon_landing.month)
    number.append(moon_landing.day)
    for i in range(3, 10, 1):
        number.append(int(numberInfo[i]))
    lottery_numbers.append(number)
f.close

f = open("lottery_numbers_Chinese", 'w')
for i in range(len(lottery_numbers)):
    f.writelines(' '.join(map(str, lottery_numbers[i])))
    f.write('\n')
f.close
