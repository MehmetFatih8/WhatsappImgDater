import sys
from datetime import datetime
import piexif
import os
import subprocess
from pathlib import Path
from PIL import Image


klasor_yolu = sys.argv[1].replace('"', "")

def FotografDateChanger(dosya_func, tarih_bilgisi):

    tarih_bilgisi_special = tarih_bilgisi.strftime("%Y:%m:%d %H:%M:%S")

    EXIF_Bilgileri = piexif.load(dosya_func[1])

    EXIF_Bilgileri['0th'][piexif.ImageIFD.DateTime] = tarih_bilgisi_special
    EXIF_Bilgileri['Exif'][piexif.ExifIFD.DateTimeOriginal] = tarih_bilgisi_special
    EXIF_Bilgileri['Exif'][piexif.ExifIFD.DateTimeDigitized] = tarih_bilgisi_special

    EXIF_Bytes = piexif.dump(EXIF_Bilgileri)
    piexif.insert(EXIF_Bytes, dosya_func[1])



    os.utime(dosya_func[1], (tarih_bilgisi.timestamp(), tarih_bilgisi.timestamp()))


def VideoDateChanger(dosya_func, tarih_bilgisi):

    print(tarih_bilgisi)
    eskidosya = dosya_func[1] + "old"
    os.rename(dosya_func[1], dosya_func[1] + "old")

    komut = [
        'ffmpeg',
        '-y',  # Otomatik olarak üzerine yaz
        '-i', eskidosya,  # Girdi
        '-metadata', f'creation_time={tarih_bilgisi}',
        '-c:v', 'copy',
        '-c:a', 'copy',
        dosya_func[1]

    ]

    subprocess.run(komut)
    os.remove(eskidosya)
    #print(komut)



def FotografDateFinder(dosya_func):
    if dosya_func[0].startswith("IMG"):

        try:
            tarih_bilgisi_raw = dosya_func[0].split("-")[1]
        except IndexError:
            if (os.stat(dosya_func[1]).st_size / 1000) < 200: #Instagramdan gelen bir fotoğraf ise
                tarih_bilgisi_raw = dosya_func[0].split("_")[1] # Dosya IMG_XXXXxxXX olarak devam ediyorsa

            else:
                return "Bir whatsapp belgesinin tarihi değiştirilmesi engellendi"
                # SEBEBI : Belge fotoğrafları _ ile ayrılıyor.

        tarih_bilgisi_yil = tarih_bilgisi_raw[0:4]
        tarih_bilgisi_ay = tarih_bilgisi_raw[4:6]
        tarih_bilgisi_gun = tarih_bilgisi_raw[6:8]
        tarih_bilgisi = datetime(int(tarih_bilgisi_yil), int(tarih_bilgisi_ay), int(tarih_bilgisi_gun), 6, 00, 00)


        FotografDateChanger(dosya_func, tarih_bilgisi)



    elif dosya_func[0].startswith("Screenshot"):
        tarih_bilgisi_raw = dosya_func[0].split("_")[1]
        tarih_bilgisi_yil = tarih_bilgisi_raw[0:4]
        tarih_bilgisi_ay = tarih_bilgisi_raw[4:6]
        tarih_bilgisi_gun = tarih_bilgisi_raw[6:8]
        tarih_bilgisi = datetime(int(tarih_bilgisi_yil), int(tarih_bilgisi_ay), int(tarih_bilgisi_gun), 6, 00, 00)


        FotografDateChanger(dosya_func, tarih_bilgisi)



    elif dosya_func[0].startswith("20"): #2023'ün ilk 20 si
        tarih_bilgisi_raw = dosya_func[0].split("_")[0]
        tarih_bilgisi_yil = tarih_bilgisi_raw[0:4]
        tarih_bilgisi_ay = tarih_bilgisi_raw[4:6]
        tarih_bilgisi_gun = tarih_bilgisi_raw[6:8]
        tarih_bilgisi = datetime(int(tarih_bilgisi_yil), int(tarih_bilgisi_ay), int(tarih_bilgisi_gun), 6, 00, 00)


        FotografDateChanger(dosya_func, tarih_bilgisi)


def VideoDateFinder(dosya_func):

    try:
        tarih_bilgisi_raw = dosya_func[0].split("-")[1]
    except IndexError:
        print(dosya_func[0] + "'ın instagram fotoğrafı olma ihtimali var!")
        tarih_bilgisi_raw = dosya_func[0].split("_")[1]

    tarih_bilgisi_yil = tarih_bilgisi_raw[0:4]
    tarih_bilgisi_ay = tarih_bilgisi_raw[4:6]
    tarih_bilgisi_gun = tarih_bilgisi_raw[6:8]
    tarih_bilgisi = f"{tarih_bilgisi_yil}-{tarih_bilgisi_ay}-{tarih_bilgisi_gun} 06:00:00"


    VideoDateChanger(dosya_func, tarih_bilgisi)

def run_fast_scandir(dir, ext):    # dir: str, ext: list
    # https://stackoverflow.com/questions/18394147/how-to-do-a-recursive-sub-folder-search-and-return-files-in-a-list
    subfolders, files = [], []

    for f in os.scandir(dir):
        if f.is_dir():
            subfolders.append(f.path)
        if f.is_file():
            if os.path.splitext(f.name)[1].lower() in ext:
                files.append(f.path)


    for dir in list(subfolders):
        sf, f = run_fast_scandir(dir, ext)
        subfolders.extend(sf)
        files.extend(f)
    return subfolders, files


subfolders, klasor_icerigi = run_fast_scandir(klasor_yolu, [".jpg", ".png", ".mp4"])


for dosya_path in klasor_icerigi:

    dosya = ["Dosya Adı", "Dosya Yolu"]
    dosya[0] = Path(dosya_path).name
    dosya[1] = dosya_path


    #İlk değer = isim
    #İkinci değer = dosya path

    if dosya[0].endswith(".jpg"): #Whatsapp Fotoğrafı mı?

        if dosya[0].startswith("IMG") or dosya[0].startswith("Screenshot"):
            FotografDateFinder(dosya)

        elif (os.stat(dosya[1]).st_size / 1000) < 550 and dosya[0].startswith("20"): # Dosyanın boyutu 200 kbden küçükse ve 20 ile başlıyorsa (21.yüzyıl) (Screenshot ise)
            FotografDateFinder(dosya) # Şuana kadarki en büyük screenshot boyutu 528 mb imiş o yüzden 550 den küçükse olarak ayarladım.

    if dosya[0].endswith(".png"): #Screenshot mı ?

        image = Image.open(dosya[1])
        image = image.convert("RGB")
        image.save(dosya[1][:-3] + "jpg", "JPEG")
        os.remove(dosya[1])
        dosya[0] = dosya[0][:-3] + "jpg"
        dosya[1] = dosya[1][:-3] + "jpg"


        FotografDateFinder(dosya)


    if dosya[0].endswith(".mp4"): #Video mu?

        if dosya[0].startswith("VID"): #Whatsapp Videosu mu?
            VideoDateFinder(dosya)




print("Done!")
