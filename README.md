# Tugas 1 : Implementasi Smoothing dan Blurring Real-Time
Inti dari operasi ini adalah Konvolusi menggeser kernel (matriks filter) di atas piksel citra untuk menghasilkan efek tertentu. Disini menggunakan cv2.filter2D() untuk mengimplementasikan ketiga filter, termasuk Gaussian Blur yang wajib menggunakan kernel kustom.

# Mode Filter yang Diimplementasikan
| Tombol | Mode Filter | Efek & Fungsi |
|:---|:---:|---:|
| 0 | Normal | Menampilkan background tanpa filter.|
| 1 | Average Blurring 5x5 | Blurring sederhana dengan kernel 
5
×
5
 yang terbobot rata |
| 2 | Average Blurring 9x9 | Blurring sederhana dengan kernel 
9
×
9
. |
| 3 | Gaussian Blurring | Blurring yang halus dan natural, menggunakan kernel 
9
×
9
 berbasis Distribusi Gaussian. |
| 4 | Sharpening | Meningkatkan ketajaman dan detail (kebalikan dari blurring). |

# Tugas 2 : Interaksi Berbasis Deteksi Warna HSV (RGB)
HSV memisahkan warna dari kecerahan, sehingga deteksi warna menjadi lebih stabil terhadap perubahan pencahayaan dibandingkan BGR/RGB. Dengan mengisolasi Hue kita dapat mencari rentang warna tertentu tanpa terlalu dipengaruhi oleh kecerahan atau bayangan. (Penting): di OpenCV nilai Hue berada pada rentang 0–179, bukan 0–360, sehingga rentang harus disesuaikan saat menentukan batas deteksi.


| Warna Terdeteksi | Perubahan | Status |
|:---|:---:|---:|
| Biru | Background berubah menjadi Biru | Deteksi: Biru |
| Hijau | Background berubah menjadi Hijau | Deteksi: Hijau |
| Merah | Background berubah menjadi Merah | Deteksi: Merah |
| Tidak ada | Background kembali ke warna gradient default | Tidak ada objek terdeteksi |
