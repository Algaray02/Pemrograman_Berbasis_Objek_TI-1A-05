import os
import shutil
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form, Body
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
import app.models as models
from app.crudController import KasirCRUD
from app.kasir_logic import Transaksi

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Dependency untuk koneksi DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

# === ADMIN ===

# === Makanan ===

@app.post("/makanan/")
async def upload_makanan(nama: str = Form(...),
                        harga: int = Form(...), 
                        nama_file: str = Form(...), 
                        gambar: UploadFile = File(...), db: Session = Depends(get_db)):
    ext = os.path.splitext(gambar.filename)[1].lower()
    if ext.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Format gambar tidak didukung.")

    os.makedirs("app/static/images/makanan", exist_ok=True)
    filename = f"{nama_file}{ext}"
    path = f"app/static/images/makanan/{filename}"
    with open(path, "wb") as buffer:
        shutil.copyfileobj(gambar.file, buffer)

    crud = KasirCRUD(db)
    makanan = crud.tambah_makanan(nama=nama, harga=harga, gambar=filename)
    return {"message": "Makanan berhasil ditambahkan", "data": makanan}

@app.get("/makanan/")
def get_makanan(db: Session = Depends(get_db)):
    crud = KasirCRUD(db)
    return crud.semua_makanan()

@app.put("/makanan/{id}")
async def update_makanan(id: int, nama: str = Form(...), harga: int = Form(...), nama_file: Optional[str] = Form(None), gambar: Optional[UploadFile] = File(None), db: Session = Depends(get_db)):
    filename = None

    if gambar and nama_file:
        ext = os.path.splitext(gambar.filename)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail="Format gambar tidak didukung.")

        filename = f"{nama_file}{ext}"
        path = f"app/static/images/makanan/{filename}"
        os.makedirs("app/static/images/makanan", exist_ok=True)

        with open(path, "wb") as buffer:
            shutil.copyfileobj(gambar.file, buffer)
    crud = KasirCRUD(db)
    makanan = crud.update_makanan(id=id, nama=nama, harga=harga, gambar=filename)

    if not makanan:
        raise HTTPException(status_code=404, detail="Item tidak ditemukan")

    return {"message": "Makanan berhasil diupdate", "data": makanan}

@app.delete("/makanan/{id}")
def delete_makanan(id: int, db: Session = Depends(get_db)):
    crud = KasirCRUD(db)
    crud.hapus_makanan(id)
    return {"message": "Makanan berhasil dihapus"}


# === Minuman ===

@app.post("/minuman/")
async def upload_minuman(nama: str = Form(...),
                        harga: int = Form(...), 
                        nama_file: str = Form(...), 
                        gambar: UploadFile = File(...), db: Session = Depends(get_db)):
    ext = os.path.splitext(gambar.filename)[1].lower()
    if ext.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Format gambar tidak didukung.")

    os.makedirs("app/static/images/minuman", exist_ok=True)
    filename = f"{nama_file}{ext}"
    path = f"app/static/images/minuman/{filename}"
    with open(path, "wb") as buffer:
        shutil.copyfileobj(gambar.file, buffer)
    crud = KasirCRUD(db)
    minuman = crud.tambah_minuman(nama=nama, harga=harga, gambar=filename)
    return {"message": "Minuman berhasil ditambahkan", "data": minuman}

@app.get("/minuman/")
def get_minuman(db: Session = Depends(get_db)):
    crud = KasirCRUD(db)
    return crud.semua_minuman()

@app.put("/minuman/{id}")
async def update_minuman(id: int, nama: str = Form(...), harga: int = Form(...), nama_file: Optional[str] = Form(None), gambar: Optional[UploadFile] = File(None), db: Session = Depends(get_db)):
    filename = None

    if gambar and nama_file:
        ext = os.path.splitext(gambar.filename)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail="Format gambar tidak didukung.")

        filename = f"{nama_file}{ext}"
        path = f"app/static/images/minuman/{filename}"
        os.makedirs("app/static/images/minuman", exist_ok=True)

        with open(path, "wb") as buffer:
            shutil.copyfileobj(gambar.file, buffer)
    crud = KasirCRUD(db)
    minuman = crud.update_minuman(id=id, nama=nama, harga=harga, gambar=filename)

    if not minuman:
        raise HTTPException(status_code=404, detail="Item tidak ditemukan")

    return {"message": "Minuman berhasil diupdate", "data": minuman}

@app.delete("/minuman/{id}")
def delete_minuman(id: int, db: Session = Depends(get_db)):
    crud = KasirCRUD(db)
    crud.hapus_minuman(id)
    return {"message": "Minuman berhasil dihapus"}

@app.get("/pelanggan/")
def get_semua_pelanggan(db: Session = Depends(get_db)):
    pelanggan_list = db.query(models.Pelanggan).all()
    hasil = []
    for p in pelanggan_list:
        hasil.append({
            "id": p.id,
            "nama": p.nama,
            "total_harga": p.total_harga,
            "bayar": p.bayar,
            "kembali": p.kembali,
            "items": [
                {
                    "nama_item": item.nama_item,
                    "jumlah": item.jumlah,
                    "harga_satuan": item.harga_satuan,
                    "total": item.total
                }
                for item in p.items
            ]
        })
    return hasil




# === PELANGGAN ===

@app.post("/pelanggan/")
def tambah_pesanan(data: dict = Body(...), db: Session = Depends(get_db)):
    trx = Transaksi(db)
    nama = data.get("nama")
    items = data.get("items", [])
    if not nama or not items:
        raise HTTPException(status_code=400, detail="Nama dan item harus diisi")
    
    trx.tambah_pesanan(nama=nama, items=items)
    return {
        "message": "Pesanan berhasil ditambahkan",
        "id": trx.pelanggan_id,
        "total": trx.total_keseluruhan
    }

@app.put("/pelanggan/{id}")
def update_pesanan(id: int, item_updates: list[dict] = Body(...), db: Session = Depends(get_db)):
    trx = Transaksi(db)
    updated = trx.update_pesanan(pelanggan_id=id, item_updates=item_updates)
    if not updated:
        raise HTTPException(status_code=404, detail="Pelanggan tidak ditemukan")
    
    return {
        "message": "Pesanan berhasil diperbarui",
        "total_harga_baru": trx.total_keseluruhan
    }

@app.post("/transaksi/selesai/")
def transaksi_selesai(pelanggan_id: int, bayar: int, db: Session = Depends(get_db)):
    trx = Transaksi(db)
    trx.pelanggan_id = pelanggan_id
    trx.total_keseluruhan = trx.db.query(models.Pelanggan).filter(models.Pelanggan.id == pelanggan_id).first().total_harga
    trx.nama_pelanggan = trx.db.query(models.Pelanggan).filter(models.Pelanggan.id == pelanggan_id).first().nama
    trx.list_items = [
        {
            "nama_item": item.nama_item,
            "jumlah": item.jumlah,
            "harga_satuan": item.harga_satuan,
            "total": item.total
        }
        for item in db.query(models.PemesananItem).filter(models.PemesananItem.pelanggan_id == pelanggan_id).all()
    ]
    trx.selesaikan_transaksi(bayar=bayar)
    return {
        "message": "Transaksi berhasil",
        "total": trx.total_keseluruhan,
        "bayar": trx.bayar,
        "kembali": trx.kembali
    }
