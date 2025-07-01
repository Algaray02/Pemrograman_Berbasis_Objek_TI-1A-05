from sqlalchemy.orm import Session
import app.models as models
import os


class KasirCRUD:
    def __init__(self, db: Session):
        self.db = db

    # === Makanan ===
    def tambah_makanan(self, nama: str, harga: int, gambar: str):
        makanan = models.Makanan(nama=nama, harga=harga, gambar=gambar)
        self.db.add(makanan)
        self.db.commit()
        self.db.refresh(makanan)
        return makanan

    def semua_makanan(self):
        return self.db.query(models.Makanan).all()

    def update_makanan(self, id: int, nama: str, harga: int, gambar: str = None):
        makanan = self.db.query(models.Makanan).filter(models.Makanan.id == id).first()
        if makanan:
            makanan.nama = nama
            makanan.harga = harga
            if gambar:
                old_path = f"app/static/images/makanan/{makanan.gambar}"
                if os.path.exists(old_path):
                    os.remove(old_path)
                makanan.gambar = gambar
            self.db.commit()
        return makanan

    def hapus_makanan(self, id: int):
        makanan = self.db.query(models.Makanan).filter(models.Makanan.id == id).first()
        if makanan:
            self.db.delete(makanan)
            self.db.commit()

    # === Minuman ===
    def tambah_minuman(self, nama: str, harga: int, gambar: str):
        minuman = models.Minuman(nama=nama, harga=harga, gambar=gambar)
        self.db.add(minuman)
        self.db.commit()
        self.db.refresh(minuman)
        return minuman

    def semua_minuman(self):
        return self.db.query(models.Minuman).all()

    def update_minuman(self, id: int, nama: str, harga: int, gambar: str = None):
        minuman = self.db.query(models.Minuman).filter(models.Minuman.id == id).first()
        if minuman:
            minuman.nama = nama
            minuman.harga = harga
            if gambar:
                old_path = f"app/static/images/minuman/{minuman.gambar}"
                if os.path.exists(old_path):
                    os.remove(old_path)
                minuman.gambar = gambar
            self.db.commit()
        return minuman

    def hapus_minuman(self, id: int):
        minuman = self.db.query(models.Minuman).filter(models.Minuman.id == id).first()
        if minuman:
            self.db.delete(minuman)
            self.db.commit()