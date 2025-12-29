#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pandas as pd
def load_mortality_table(gender):
    filename = "tmi_pria.csv" if gender == "L" else "tmi_wanita.csv"
    try:
        df = pd.read_csv(filename)
        df.columns = [col.lower() for col in df.columns]
        return df
    except FileNotFoundError:
        print(f"\n[ERROR] File {filename} tidak ditemukan di folder!")
        return None

def calculate_commutation(df, interest_rate):
    v = 1 / (1 + interest_rate)
    df['dx_comm'] = df.apply(lambda row: (v**row['x']) * row['lx'], axis=1)
    df['nx_comm'] = df['dx_comm'][::-1].cumsum()[::-1]
    df['cx_comm'] = df.apply(lambda row: (v**(row['x'] + 1)) * row['dx'], axis=1)
    df['mx_comm'] = df['cx_comm'][::-1].cumsum()[::-1]
    return df

def hitung_premi(data, jenis, x, n_tanggung, n_bayar, up):
    row_x = data[data['x'] == x].iloc[0]
    Dx, Nx, Mx = row_x['dx_comm'], row_x['nx_comm'], row_x['mx_comm']
    def get_val(age, column):
        res = data[data['x'] == age][column].values
        return res[0] if len(res) > 0 else 0
    Mx_n = get_val(x + n_tanggung, 'mx_comm')
    Dx_n = get_val(x + n_tanggung, 'dx_comm')
    Nx_k = get_val(x + n_bayar, 'nx_comm')
    if jenis == "1":  
        nsp = (Mx - Mx_n) / Dx
    elif jenis == "2": 
        nsp = Mx / Dx
    elif jenis == "3":  
        nsp = ((Mx - Mx_n) + Dx_n) / Dx
    else:
        return 0, 0
    if n_bayar <= 1:
        annuity_factor = 1
    else:
        annuity_factor = (Nx - Nx_k) / Dx
    
    annual_p = nsp / annuity_factor
    return nsp * up, annual_p * up

def get_input_polis():
    nama = input("Nama Nasabah: ")
    umur = int(input("Usia Nasabah (x): "))
    while True:
        gender = input("Jenis Kelamin (L/P): ").upper()
        if gender in ["L", "P"]: break
        print("Input salah! Gunakan 'L' atau 'P'.")
    
    up = float(input("Uang Pertanggungan (UP): "))
    
    print("Jenis Produk: [1] Term, [2] Whole Life, [3] Endowment")
    while True:
        tipe = input("Pilihan Produk: ")
        if tipe in ["1", "2", "3"]: break
        print("Input salah! Pilih 1, 2, atau 3.")  
    if tipe == "2":
        n_tanggung = 110 - umur 
    else:
        n_tanggung = int(input("Masa Pertanggungan (n tahun): "))
        
    n_bayar = int(input("Masa Pembayaran Premi (k tahun): "))
    
    return nama, umur, gender, up, tipe, n_tanggung, n_bayar

def main():
    print("="*65)
    print("   SISTEM AUTOMASI PREMI ASURANSI JIWA (Python Actuary)   ")
    print("="*65) 
    try:
        i = float(input("Masukkan Asumsi Bunga (contoh 0.05 untuk 5%): "))
    except ValueError:
        print("Input bunga harus angka!")
        return
    data_pria = load_mortality_table("L")
    data_wanita = load_mortality_table("P")
    
    if data_pria is None or data_wanita is None: return

    data_pria = calculate_commutation(data_pria, i)
    data_wanita = calculate_commutation(data_wanita, i)

    n_polis = int(input("\nBerapa banyak polis yang ingin diinput? "))
    hasil_list = []

    for j in range(n_polis):
        print(f"\n--- DATA POLIS KE-{j+1} ---")
        nama, umur, gender, up, tipe, n_tanggung, n_bayar = get_input_polis()
        ref_data = data_pria if gender == "L" else data_wanita
        tunggal, tahunan = hitung_premi(ref_data, tipe, umur, n_tanggung, n_bayar, up)
        hasil_list.append({
            "Nama": nama,
            "Tipe": "Term" if tipe=="1" else "Whole Life" if tipe=="2" else "Endowment",
            "Tunggal": tunggal,
            "Tahunan": tahunan
        })
    print("\n" + "="*75)
    print(f"{'NAMA':<15} | {'PRODUK':<12} | {'PREMI TUNGGAL':>18} | {'PREMI TAHUNAN':>18}")
    print("-" * 75)
    for h in hasil_list:
        print(f"{h['Nama']:<15} | {h['Tipe']:<12} | {h['Tunggal']:>18,.2f} | {h['Tahunan']:>18,.2f}")
    print("="*75)

if __name__ == "__main__":
    main()


# 
