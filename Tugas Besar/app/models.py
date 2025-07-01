from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Makanan(Base):
    __tablename__ = "makanan"
    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String)
    harga = Column(Integer)
    gambar = Column(String)


class Minuman(Base):
    __tablename__ = "minuman"
    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String)
    harga = Column(Integer)
    gambar = Column(String)

class Pelanggan(Base):
    __tablename__ = "pelanggan"
    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String, nullable=False)
    total_harga = Column(Integer, default=0)
    bayar = Column(Integer, default=0)
    kembali = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now())
    items = relationship("PemesananItem", back_populates="pelanggan")


class PemesananItem(Base):
    __tablename__ = "pemesanan_item"
    id = Column(Integer, primary_key=True, index=True)
    pelanggan_id = Column(Integer, ForeignKey("pelanggan.id"), nullable=False)
    nama_item = Column(String, nullable=False)
    jumlah = Column(Integer, nullable=False)
    harga_satuan = Column(Integer, nullable=False)
    total = Column(Integer, nullable=False)
    pelanggan = relationship("Pelanggan", back_populates="items")

