from colorama import Fore, Style

class HANDPHONE:
   def __init__(self, id_hp, nama_hp, harga, stok):
      self.id = id_hp
      self.nama = nama_hp
      self.harga = harga
      self.stok = stok
   
   def info_hp(self):
      print(f'ID : {self.id}\nNama Handphone : {self.nama}\nHarga : {self.harga}\nStok : {self.stok}\n')


class PEMBELIAN:
   def __init__(self):
      self.daftar_hp = []
      self.keranjang = {}
   
   def tambah_hp(self, hp):  
      self.daftar_hp.append(hp)
      print(f'{hp.nama} Berhasil Ditambahkan!!')

   def cek_id_hp(self, id_hp):
      for hp in self.daftar_hp:
         if id_hp == hp.id:
            return hp
      return None
   
   def tampilkan_hp(self):
      if not self.daftar_hp:
         print(f"{Fore.RED}Tidak ada list HP yang tersedia!!{Style.RESET_ALL}")
         return None
      
      print(f'{Fore.CYAN}\n===DAFTAR HP TERSEDIA==={Style.RESET_ALL}')
      for hp in self.daftar_hp:
         hp.info_hp()

   def tambah_keranjang(self, id_hp, jumlah):
      hp = self.cek_id_hp(id_hp)

      if not hp:
         print(f'{Fore.RED}Tidak ada HP dengan ID : {id_hp}!!{Style.RESET_ALL}')
         return False
      
      if jumlah > hp.stok:
         print(f'{Fore.YELLOW}Stok HP yang tersedia : {hp.stok}{Style.RESET_ALL}')
         return False

      if id_hp in self.keranjang:
         self.keranjang[id_hp] += jumlah
      else:
         self.keranjang[id_hp] = jumlah
      hp.stok -= jumlah

      print(f'{Fore.GREEN}{hp.nama} berhasil ditambahkan!!{Style.RESET_ALL}')
      return True
   
   def hapus_keranjang(self, id_hp, jumlah):
      if id_hp in self.keranjang:
         if jumlah <= self.keranjang[id_hp]:
            self.keranjang[id_hp] -= jumlah
            print(f'Penghapusan berhasil dilakukan')
         else:
            print(f'{Fore.RED}Jumlah melebihi batas!!{Style.RESET_ALL}')
      else:
         print(f'{Fore.RED}Tidak ada HP dengan ID : {id_hp}!!!{Style.RESET_ALL}')

   def tampilkan_keranjang(self):
      if not self.keranjang:
         print(f'{Fore.RED}Keranjang kosong!!!{Style.RESET_ALL}')
         return
      
      print(f'{Fore.CYAN}\n===KERANJANG==={Style.RESET_ALL}')
      total = 0
      
      for id_hp, jumlah in self.keranjang.items():
         hp = self.cek_id_hp(id_hp)
         subtotal = hp.harga * jumlah
         total += subtotal
         print(f"{hp.nama} - {jumlah} unit x Rp{hp.harga:,} = Rp{subtotal:,}")
      print(f"\nTotal: Rp{total:,}")

   def checkout(self):
      if not self.keranjang:
         print(f'{Fore.RED}Keranjang kosong!!!{Style.RESET_ALL}')
         return

      print(f'{Fore.CYAN}\n===CHECKOUT==={Style.RESET_ALL}')
      total = 0

      for id_hp, jumlah in self.keranjang.items():
         hp = self.cek_id_hp(id_hp)
         subtotal = hp.harga * jumlah
         total += subtotal
         print(f"{hp.nama} - {jumlah} unit x Rp{hp.harga:,} = Rp{subtotal:,}")
      print(f"\nTotal: Rp{total:,}")
      print(f'{Fore.GREEN}Transaksi Berhasil!!{Style.RESET_ALL}')
      self.keranjang = {}






