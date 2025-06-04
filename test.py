def penambahan(jumlah):
   total = 1
   total = total + jumlah
   print(jumlah)
   return total


def main():
   jumlah = 50
   penambahan(jumlah)
   # print(penambahan(jumlah))
   total2 = 10 + penambahan(10)
   print(total2)
   
main()