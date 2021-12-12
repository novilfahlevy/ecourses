import platform
import pwinput
import os

data_user = [
  {
    'nama': 'Novil',
    'password': '123',
    'usia': 21,
    'saldo': 100000,
    'epoint': 1000,
    'premium': False,
    'kelas': [],
    'gender': 1,
  },
  {
    'nama': 'Fauzan',
    'password': '123',
    'usia': 11,
    'saldo': 100000,
    'epoint': 100,
    'premium': False,
    'kelas': [],
    'gender': 1,
  },
  {
    'nama': 'Rizki',
    'password': '123',
    'usia': 16,
    'saldo': 100000,
    'epoint': 0,
    'premium': False,
    'kelas': [],
    'gender': 1,
  },
]

data_kelas = [
  { 'judul': 'Kursus Bahasa Inggris', 'harga': 100 },
  { 'judul': 'Belajar Memasak', 'harga': 150 },
  { 'judul': 'Kursus Bahasa Jepang', 'harga': 200 },
]

data_epoint = [
  { 'epoint': 100, 'harga': 10000 },
  { 'epoint': 150, 'harga': 12000 },
  { 'epoint': 300, 'harga': 18000 },
]

# variabel untuk menyimpan index user yang login
user_login_index = None

def bersihkan_console() :
  if platform.system() == 'Windows' :
    os.system('cls')
  else :
    os.system('clear')

def cek_kelas_sudah_dibeli(judul_kelas) :
  user = data_user[user_login_index]
  kelas_user = user['kelas']
  return judul_kelas in list(map(lambda kelas: kelas['judul'], kelas_user))

def kelas_saya() :
  kelas = data_user[user_login_index]['kelas']

  # cek jika user memiliki kelas
  print()
  if len(kelas) < 1 :
    print('Anda belum memiliki kelas.')
  else :
    print('List kelas saya : ')
    for k in range(len(kelas)) :
      nomor = k + 1
      judul = kelas[k]['judul']
      print(f'[{nomor}] {judul}')

  # Kembali ke piilhan()
  return aplikasi()

def beli_kelas() :
  print('\n=== List Kelas ===')

  kelas = list(filter(lambda kelas: not cek_kelas_sudah_dibeli(kelas['judul']), data_kelas))

  if len(kelas) > 0 :
    for k in range(len(kelas)) :
      nomor = k + 1
      judul = kelas[k]['judul']
      harga = kelas[k]['harga']
      kelas_sudah_dibeli = cek_kelas_sudah_dibeli(judul)

      diskon = 20 # persen
      harga = int((harga - ((harga / 100) * diskon))) if data_user[user_login_index]['premium'] else harga

      # Jangan tampilkan kelas yang sudah dibeli
      if not kelas_sudah_dibeli :
        print(f'[{nomor}] {judul} | {harga} Epoint')

    print('[88] Kembali')
  else :
    print('Tidak ada kelas tersedia')
    return aplikasi()

  p = int(input('Pilih : '))

  # pilihan 88 mengarah ke menu pilihan
  if p == 88 :
    return aplikasi()

  # cek apakah pilihan sesuai dengan kelas yang tersedia
  if p < 0 or p > len(kelas) :
    print('Pilih pilihan yang tersedia')
    return beli_kelas()

  kelas_dipilih = kelas[p - 1]
  user = data_user[user_login_index]

  # cek apakah endpoint mencukupi
  if user['epoint'] < kelas_dipilih['harga'] :
    print('Epoint anda tidak mencukupi')
    return beli_kelas()

  # kurangi epoint sesuai harga kelas dan tambahkan kelas yang sudah dibeli ke user
  if user['premium'] :
    harga = kelas_dipilih['harga']
    diskon = 20 # persen
    user['epoint'] = user['epoint'] - int((harga - ((harga / 100) * diskon)))
  else :
    user['epoint'] = user['epoint'] - kelas_dipilih['harga']
  
  # Tambahkan kelas yang sudah dibeli
  user['kelas'].append(kelas_dipilih)
  
  return aplikasi()

def beli_epoint() :
  print('\n=== List Epoint ===')

  for e in range(len(data_epoint)) :
    nomor = e + 1
    epoint = data_epoint[e]['epoint']
    harga = data_epoint[e]['harga']
    print(f'[{nomor}] {epoint} | Rp {harga}')

  print('[88] Kembali')

  p = int(input('Pilih : '))

  # pilihan 88 mengarah ke menu pilihan
  if p == 88 :
    return aplikasi()

  # cek apakah pilihan sesuai dengan epoint yang tersedia
  if p < 0 or p > len(data_epoint) :
    print('Pilih pilihan yang tersedia')
    return beli_epoint()

  epoint_dipilih = data_epoint[p - 1]
  user = data_user[user_login_index]
  
  # cek apakah endpoint mencukupi
  if user['saldo'] < epoint_dipilih['harga'] :
    print('Epoint anda tidak mencukupi')
    return beli_epoint()

  # tambah epoint user sesuai dengan yang dibeli
  # dan kurangi saldo user sesuai harga epoint yang dibeli
  user['epoint'] = user['epoint'] + epoint_dipilih['epoint']
  user['saldo'] = user['saldo'] - epoint_dipilih['harga']

  print('\nEpoint berhasil dibeli :)')
  print(f"\nSisa saldo anda Rp {user['saldo']}")
  print(f"Epoint anda {user['epoint']}\n")
  return aplikasi()

def upgrade_premium() :
  jawaban = input('\nApakah anda ingin membeli premium fitur, seharga Rp 50000 (Y/n) ? ').lower()
  if jawaban == 'y' or jawaban == '' :
    user = data_user[user_login_index]
    if user['saldo'] >= 50000 :
      user['premium'] = True
      user['saldo'] -= 50000
      print('Selamat, anda sudah menjadi user premium.')
    else :
      print('Maaf, saldo anda tidak mencukupi')
  
  return aplikasi()

def pilihan() :
  print('[1] Beli kelas')
  print('[2] Kelas saya')
  print('[3] Beli epoint')

  # Pilihan hanya tersedia jika user belum premium
  if not data_user[user_login_index]['premium'] :
    print('[4] Upgrade premium')

  print('[0] Logout')

  pilihan = int(input('Pilih : '))
  return pilihan

def aplikasi() :
  print('\n=== E Courses ===')

  # Selamat datang berdasarkan usia dan gender
  user = data_user[user_login_index]
  if user['usia'] <= 15 :
    print(f"Halo dek {user['nama']}")
  elif user['usia'] > 15 and user['usia'] <= 20 :
    print(f"Halo kak {user['nama']}")
  else :
    if user['gender'] == 1 :
      print(f"Halo bapak {user['nama']}")
    else :
      print(f"Halo ibu {user['nama']}")

  # Tampilkan saldo dan epoint
  user_premium = user['premium']
  print(f"Saldo anda Rp {data_user[user_login_index]['saldo']}, Epoint anda {data_user[user_login_index]['epoint']}{', anda user premium.' if user_premium else '.'}\n")
  
  p = pilihan()

  if p == 1 :
    return beli_kelas()
  elif p == 2 :
    return kelas_saya()
  elif p == 3 :
    return beli_epoint()
  elif p == 4 :
    # Pilihan hanya tersedia jika user belum premium
    if not user['premium'] :
      return upgrade_premium()
    
    print('Mohon pilih pilihan yang tersedia')
    return aplikasi()
  elif p == 0 :
    return login()
  else :
    print('Mohon pilih pilihan yang tersedia')
    return aplikasi()


def login() :
  global user_login_index
  bersihkan_console()

  try :
    nama = input('Nama : ')
    password = pwinput.pwinput('Password : ')
  except KeyboardInterrupt :
    print('\nSelamat tinggal ^^')
    exit()

  for index in range(len(data_user)) :
    if nama == data_user[index]['nama'] and password == data_user[index]['password'] :
      # simpan index user berdasarkan index dari list user_data
      user_login_index = index
      return aplikasi()

  print('Akun tidak ditemukan')
  return login()

login()
