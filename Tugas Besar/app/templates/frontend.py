import streamlit as st
import requests

API_URL = "http://localhost:8000"

# Inisialisasi session state
if 'current_page' not in st.session_state:
   st.session_state.current_page = 'login'
if 'user' not in st.session_state:
   st.session_state.user = ''
if 'is_admin' not in st.session_state:
   st.session_state.is_admin = False
if 'keranjang' not in st.session_state:
   st.session_state.keranjang = []
if 'last_added' not in st.session_state:
    st.session_state.last_added = None
if 'transaksi_selesai' not in st.session_state:
   st.session_state.transaksi_selesai = False

def login_page():
    st.title("Kasir Restoran 🧾")

    nama = st.text_input("Masukkan Nama Anda")
    if nama == "admin":
        passwd = st.text_input("Masukkan password", type="password")
        if st.button("Masuk sebagai Admin"):
            if passwd == "admin123": 
                st.session_state.user = nama
                st.session_state.is_admin = True
                st.session_state.current_page = 'admin'
            else:
                st.error("Password salah!")
    elif nama:
        if st.button("Lanjutkan"):
            st.session_state.user = nama
            st.session_state.is_admin = False
            st.session_state.current_page = 'dashboard_user'

def admin_page():
    st.title("Admin Page")
    col1, col2 = st.columns([4, 1])
    with col1:
        st.write(f"Selamat datang, {st.session_state.get('user', 'Admin')}!")
    
    with col2:
        if st.button("⬅️ Kembali", use_container_width=True):
            if 'user' in st.session_state:
                del st.session_state['user']
            st.session_state.current_page = "login"
            st.rerun()

    tab1, tab2, tab3 = st.tabs(["📄 Riwayat Transaksi", "🍽️ CRUD Makanan", "🥤 CRUD Minuman"])

    # ========== RIWAYAT ==========
    with tab1:
        st.header("Riwayat Transaksi Pelanggan")

        res = requests.get(f"{API_URL}/pelanggan/")
        if res.ok:
            data = res.json()
            for pelanggan in data:
                st.subheader(f"{pelanggan['nama']} (ID: {pelanggan['id']})")
                st.write("Total:", f"Rp {pelanggan['total_harga']:,}".replace(",", "."))
                st.write("Bayar:", f"Rp {pelanggan['bayar']:,}".replace(",", "."))
                st.write("Kembali:", f"Rp {pelanggan['kembali']:,}".replace(",", "."))

                if pelanggan["items"]:
                    with st.expander("Lihat Pesanan"):
                        for item in pelanggan["items"]:
                            st.write(f"- {item['nama_item']} × {item['jumlah']} = Rp {item['total']:,}".replace(",", "."))
        else:
            st.error("Gagal memuat data pelanggan")

    # ========== CRUD MAKANAN ==========
    with tab2:
        st.header("Kelola Menu Makanan")
        makanan = requests.get(f"{API_URL}/makanan/").json()
        for item in makanan:
            with st.expander(f"{item['nama']} (Rp {item['harga']:,})".replace(",", ".")):
                new_nama = st.text_input(f"Nama Baru - {item['id']}", value=item["nama"], key=f"nama_mkn_{item['id']}")
                new_harga = st.number_input(f"Harga Baru - {item['id']}", value=item["harga"], key=f"harga_mkn_{item['id']}")
                new_file_name = st.text_input(f"Nama File Gambar - {item['id']}", key=f"file_mkn_{item['id']}")
                new_gambar = st.file_uploader("Gambar Baru", key=f"img_mkn_{item['id']}", type=["jpg", "jpeg", "png"])

                if st.button("💾 Simpan Perubahan", key=f"edit_mkn_{item['id']}"):
                    files = {"gambar": new_gambar} if new_gambar else None
                    data = {
                        "nama": new_nama,
                        "harga": new_harga,
                        "nama_file": new_file_name or item["gambar"].split(".")[0]
                    }
                    r = requests.put(f"{API_URL}/makanan/{item['id']}", data=data, files=files)
                    if r.ok:
                        st.success("Berhasil diperbarui!")
                        st.rerun()

                if st.button("🗑️ Hapus", key=f"del_mkn_{item['id']}"):
                    r = requests.delete(f"{API_URL}/makanan/{item['id']}")
                    if r.ok:
                        st.success("Berhasil dihapus!")
                        st.rerun()

        st.subheader("➕ Tambah Makanan Baru")
        nama_baru = st.text_input("Nama Makanan", key="tambah_makanan_nama")
        harga_baru = st.number_input("Harga", min_value=0, step=500, key="tambah_makanan_harga")
        nama_file_baru = st.text_input("Nama File Gambar (tanpa ekstensi)", key="tambah_makanan_file")
        gambar_baru = st.file_uploader("Upload Gambar", type=["jpg", "jpeg", "png"], key="tambah_makanan_gambar")

        if st.button("Tambah Makanan"):
            if not gambar_baru or not nama_file_baru:
                st.warning("Mohon isi nama file dan upload gambar.")
            else:
                files = {"gambar": (gambar_baru.name, gambar_baru.getvalue(), gambar_baru.type)}
                data = {
                    "nama": nama_baru,
                    "harga": harga_baru,
                    "nama_file": nama_file_baru
                }
                res = requests.post(f"{API_URL}/makanan/", data=data, files=files)
                if res.ok:
                    st.success("Berhasil ditambahkan!")
                    st.rerun()
                else:
                    st.error(f"Terjadi kesalahan. Status Code: {res.status_code}")
                    # Tampilkan pesan error dari FastAPI
                    st.json(res.json())

    # ========== CRUD MINUMAN ==========
    with tab3:
        st.header("Kelola Menu Minuman")
        minuman = requests.get(f"{API_URL}/minuman/").json()
        for item in minuman:
            with st.expander(f"{item['nama']} (Rp {item['harga']:,})".replace(",", ".")):
                new_nama = st.text_input(f"Nama Baru - {item['id']}", value=item["nama"], key=f"nama_mnm_{item['id']}")
                new_harga = st.number_input(f"Harga Baru - {item['id']}", value=item["harga"], key=f"harga_mnm_{item['id']}")
                new_file_name = st.text_input(f"Nama File Gambar - {item['id']}", key=f"file_mnm_{item['id']}")
                new_gambar = st.file_uploader("Gambar Baru", key=f"img_mnm_{item['id']}", type=["jpg", "jpeg", "png"])

                if st.button("💾 Simpan Perubahan", key=f"edit_mnm_{item['id']}"):
                    files = {"gambar": new_gambar} if new_gambar else None
                    data = {
                        "nama": new_nama,
                        "harga": new_harga,
                        "nama_file": new_file_name or item["gambar"].split(".")[0]
                    }
                    r = requests.put(f"{API_URL}/minuman/{item['id']}", data=data, files=files)
                    if r.ok:
                        st.success("Berhasil diperbarui!")
                        st.rerun()

                if st.button("🗑️ Hapus", key=f"del_mnm_{item['id']}"):
                    r = requests.delete(f"{API_URL}/minuman/{item['id']}")
                    if r.ok:
                        st.success("Berhasil dihapus!")
                        st.rerun()

        st.subheader("➕ Tambah Minuman Baru")
        nama_baru = st.text_input("Nama Minuman", key="tambah_minuman_nama")
        harga_baru = st.number_input("Harga", min_value=0, step=500, key="tambah_minuman_harga")
        nama_file_baru = st.text_input("Nama File Gambar (tanpa ekstensi)", key="tambah_minuman_file")
        gambar_baru = st.file_uploader("Upload Gambar", type=["jpg", "jpeg", "png"], key="tambah_minuman_gambar")

        if st.button("Tambah Minuman"):
            if not gambar_baru or not nama_file_baru:
                st.warning("Mohon isi nama file dan upload gambar.")
            else:
                files = {"gambar": (gambar_baru.name, gambar_baru.getvalue(), gambar_baru.type)}
                data = {
                    "nama": nama_baru,
                    "harga": harga_baru,
                    "nama_file": nama_file_baru
                }
                res = requests.post(f"{API_URL}/minuman/", data=data, files=files)
                if res.ok:
                    st.success("Berhasil ditambahkan!")
                    st.rerun()


def dashboard_user_page():
    st.title(f"Halo, {st.session_state.user}👋. Pesen Apa Hari Ini?")
    if st.session_state.last_added:
      st.success(f"✅ {st.session_state.last_added} berhasil ditambahkan ke keranjang!")
      st.session_state.last_added = None
    st.header("Menu Makanan")
    makanan_res = requests.get(f"{API_URL}/makanan/")
    if makanan_res.ok:
        makanan_list = makanan_res.json()
        for item in makanan_list:
            col1, col2, col3 = st.columns([1, 3, 1])
            with col1:
                st.image(f"{API_URL}/static/images/makanan/{item['gambar']}", width=80)
            with col2:
                st.subheader(item["nama"])
                st.write(f"Rp {item['harga']:,}".replace(",", "."))
            with col3:
                if st.button(f"➕ Tambah", key=f"add_makanan_{item['id']}"):
                    st.session_state.keranjang.append({
                        "nama_item": item["nama"],
                        "jumlah": 1,
                        "harga_satuan": item["harga"]
                    })
                    st.session_state.last_added = item["nama"]
                    st.rerun()

    st.header("Menu Minuman")
    minuman_res = requests.get(f"{API_URL}/minuman/")
    if minuman_res.ok:
        minuman_list = minuman_res.json()
        for item in minuman_list:
            col1, col2, col3 = st.columns([1, 3, 1])
            with col1:
                st.image(f"{API_URL}/static/images/minuman/{item['gambar']}", width=80)
            with col2:
                st.subheader(item["nama"])
                st.write(f"Rp {item['harga']:,}".replace(",", "."))
            with col3:
                if st.button(f"➕ Tambah", key=f"add_minuman_{item['id']}"):
                    st.session_state.keranjang.append({
                        "nama_item": item["nama"],
                        "jumlah": 1,
                        "harga_satuan": item["harga"]
                    })
                    st.session_state.last_added = item["nama"]
                    st.rerun() 

    if st.button("Lanjut ke Transaksi"):
        st.session_state.current_page = 'transaksi'



def transaksi_page():
    import requests

    st.title("Halaman Transaksi")

    if "keranjang" not in st.session_state:
        st.session_state.keranjang = []
    if "transaksi_selesai" not in st.session_state:
        st.session_state.transaksi_selesai = False
    if "user" not in st.session_state:
        st.session_state.user = ''

    # bagian transaksi selesai
    if st.session_state.transaksi_selesai:
        st.success("Transaksi berhasil!")
        
        total = st.session_state.get("total_harga", 0)
        bayar = st.session_state.get("bayar", 0)
        kembali = st.session_state.get("kembali", 0)

        st.write(f"Total Belanja: Rp {total:,}".replace(",", "."))
        st.write(f"Jumlah Bayar: Rp {bayar:,}".replace(",", "."))
        st.write(f"Kembalian: Rp {kembali:,}".replace(",", "."))
        
        if st.button("✅ Selesai"):
            for key in ["keranjang", "total_harga", "pelanggan_id", "transaksi_selesai", "bayar", "kembali", "user"]:
                if key in st.session_state:
                    del st.session_state[key]
            
            st.session_state.current_page = "login"
            st.rerun()
        return

    # bagian list transaksi
    keranjang = st.session_state.keranjang
    if not keranjang:
        st.warning("Keranjang belanja masih kosong.")
        if st.button("⬅️ Kembali ke Menu"):
            st.session_state.current_page = 'dashboard_user'
            st.rerun()
        return

    st.write("### Ringkasan Pesanan:")
    
    for idx, item in enumerate(keranjang):
        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
        with col1:
            st.write(item["nama_item"])
        with col2:
            new_jumlah = st.number_input("Jumlah", min_value=1, value=item["jumlah"], key=f"jumlah_{idx}")
            st.session_state.keranjang[idx]["jumlah"] = new_jumlah
        with col3:
            st.write(f"Rp {item['harga_satuan']:,}".replace(",", "."))
        with col4:
            if st.button("❌", key=f"hapus_{idx}"):
                st.session_state.keranjang.pop(idx)
                st.rerun()

    total = sum(item["jumlah"] * item["harga_satuan"] for item in st.session_state.keranjang)
    st.session_state.total_harga = total
    st.write(f"### Total Belanja: Rp {total:,}".replace(",", "."))
    bayar = st.number_input("Nominal Bayar", min_value=0, step=1000, format="%d")
    col_selesai, col_kembali = st.columns(2)
    
    with col_kembali:
        if st.button("⬅️ Kembali ke Menu", use_container_width=True):
            st.session_state.current_page = 'dashboard_user'
            st.rerun()

    with col_selesai:
        if st.button("Selesaikan Transaksi", use_container_width=True):
            items = [item for item in st.session_state.keranjang if item["jumlah"] > 0]

            if not items:
                st.error("Tidak ada item valid dalam keranjang.")
                return

            if bayar < total:
                st.error("Nominal bayar kurang dari total belanja.")
                return

            try:
                res = requests.post(f"{API_URL}/pelanggan/", json={
                    "nama": st.session_state.user,
                    "items": items
                })
                res.raise_for_status()

                pelanggan_id = res.json()["id"]
                st.session_state.pelanggan_id = pelanggan_id

                bayar_res = requests.post(f"{API_URL}/transaksi/selesai/", params={
                    "pelanggan_id": pelanggan_id,
                    "bayar": bayar
                })
                bayar_res.raise_for_status()
                kembali = bayar - total
                st.session_state.bayar = bayar
                st.session_state.kembali = kembali
                st.session_state.transaksi_selesai = True
                st.rerun()

            except requests.exceptions.RequestException as e:
                st.error(f"Gagal terhubung ke server: {e}")
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")

# Routing antar halaman
if st.session_state.current_page == 'login':
    login_page()
elif st.session_state.current_page == 'admin':
    admin_page()
elif st.session_state.current_page == 'dashboard_user':
    dashboard_user_page()
elif st.session_state.current_page == 'transaksi':
    transaksi_page()