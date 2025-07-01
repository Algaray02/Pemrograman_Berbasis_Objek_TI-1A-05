from app.crudController import KasirCRUD
from app.models import Pelanggan, PemesananItem

class Transaksi(KasirCRUD):
    def __init__(self, db):
        super().__init__(db)
        self.pelanggan_id = id
        self.nama_pelanggan = ""
        self.list_items = []
        self.list_pemesanan = {}
        self.total_keseluruhan = 0
        self.bayar = 0
        self.kembali = 0
        
    def tambah_pesanan(self, nama: str, items: list[dict]):
        total_harga = 0
        list_objs = []

        for item in items:
            jumlah = item["jumlah"]
            harga = item["harga_satuan"]
            total = jumlah * harga
            total_harga += total
             
            item_obj = PemesananItem(
                nama_item=item["nama_item"],
                jumlah=jumlah,
                harga_satuan=harga,
                total=total
            )
            list_objs.append(item_obj)
        
        pelanggan = Pelanggan(
            nama=nama,
            total_harga=total_harga,
            items=list_objs
        )
        self.nama_pelanggan = nama
        self.list_items.append(list_objs)
        self.total_keseluruhan = total_harga
        self.db.add(pelanggan)
        self.db.commit()
        self.db.refresh(pelanggan)
        self.pelanggan_id = pelanggan.id

    def get_semua_pesanan(self):
        return self.db.query(Pelanggan).all()
    
    def update_pesanan(self, pelanggan_id: int, item_updates: list[dict]):
        pelanggan = self.db.query(Pelanggan).filter(Pelanggan.id == pelanggan_id).first()

        if not pelanggan:
            return None

        total_baru = 0

        for upd in item_updates:
            item = self.db.query(PemesananItem).filter(
                PemesananItem.id == upd["id"],
                PemesananItem.pelanggan_id == pelanggan_id
            ).first()

            if not item:
                continue

            if upd["jumlah"] == 0:
                self.db.delete(item)
            else:
                item.jumlah = upd["jumlah"]
                item.total = item.jumlah * item.harga_satuan
                total_baru += item.total

        # Hitung ulang semua item yang masih ada
        sisa_items = self.db.query(PemesananItem).filter(
            PemesananItem.pelanggan_id == pelanggan_id
        ).all()

        total_baru = sum([i.total for i in sisa_items])
        pelanggan.total_harga = total_baru
        self.total_keseluruhan = total_baru
        self.db.commit()
        self.db.refresh(pelanggan)

        return pelanggan
        
    def selesaikan_transaksi(self, bayar: int):
        self.bayar = bayar
        self.kembali = bayar - self.total_keseluruhan

        # Simpan juga ke DB
        pelanggan = self.db.query(Pelanggan).filter(Pelanggan.id == self.pelanggan_id).first()
        if pelanggan:
            pelanggan.bayar = self.bayar
            pelanggan.kembali = self.kembali
            self.db.commit()