# -*- coding: utf-8 -*-

import time
import tkinter as tk
from tkinter import filedialog
import pdfplumber
import re
import pyfiglet
import random
import sys
from termcolor import colored,cprint
from colorama import init
import os


c = []
dosyalar = []
harfler = "ABCÇDEFGĞHİIJKLMNOÖPRSŞTUÜVYZabcçdefgğhiıjklmnoöprsştuüvyz@+𝜕𝜑∑𝑁π𝑑𝐴𝑏𝑑𝑉𝜕𝑈𝑒𝑭𝑧𝑦𝑒𝜌̅𝐶()𝒊" #burada bütün harf ve sembollerr bulunuyor bunu sayı olmayan parantez içi metinleri ayırmak için kullanıcaz.
fark = []
global son
kaynakca_hata = []
kaynaklar_liste = []
kaynak_liste2 = [] 
atıf_pasr = []

init()


root = tk.Tk()
root.withdraw()    




font_list = ["starwars","larry3d","standard"]
colors = ["blue","green","red"]
font = random.choice(font_list)
color = random.choice(colors)

cprint(pyfiglet.figlet_format("Tez Kontrol",font),color)
print("Coded by:Awembley")


time.sleep(1)


cprint("Program Başlatılıyor...", 'red', attrs=['bold'], file=sys.stderr)


for dosya in  os.listdir():   #programın bulundugu konumdaki sonu pdfle biten dosyaları bir listede topluyoruz.
    if dosya.endswith(".pdf"):
        dosyalar.append(dosya)


def uyarı():
    cprint("İşleminiz Tamamlandı!", 'red', attrs=['bold'], file=sys.stderr)
    cprint("Çıkış için enter tuşuna basınız.", 'red', attrs=['bold'], file=sys.stderr)
    input()

def control(listostr):
    kelime_sınırı = 50
    pars = listostr.split(' ') #gelen stringi parçalıyoruz. 
    log_kayıt = ' '.join(listostr.split()[:4]) # uzun cümleler oldugu için fikir vermesi açısından sadece ilk 4 kelimeyi yazdırıyoruz.
    if len(pars) > kelime_sınırı: #kelime uzunluğu
        log_dosya.writelines(f'{log_kayıt} --------------> Tırnak içerisinde {kelime_sınırı} den fazla kelime olamaz.Kelime sayısı {len(pars)}.\n')
        


def islem(dosya_adı):
    
    try:
        denek = ""
        blokatıftüm = ''
        all_text = ''
        şekilsayfa = ''
        
        with pdfplumber.open(dosya_adı) as pdf:  # buradaki kodda sayfa sayfa okutup tablo ve şekilleri bir listeye atıyoruz.
            for i in range(0, len(pdf.pages)):
                page = pdf.pages[i]
                text = page.extract_text()           
                if text.startswith("ÖNSÖZ"):
                    ayrılmış = text.lower()
                    ayrılmış = ayrılmış.split("\n")
                    if "teşekkür" in ayrılmış[3]:
                        log_dosya.writelines("Önsözün ilk paragrafında  Teşekkür ibaresi bulunmaz.\n")
                            
          
                
                
                elif text.startswith("ŞEKİLLER LİSTESİ"):
                    sayfa = pdf.pages[i+1]
                    sonrakisayfa = sayfa.extract_text()
                    şekilsayfa = text + '\n' + sonrakisayfa
                    şekilliste = re.findall("Şekil ....", şekilsayfa)


                elif text.startswith("TABLOLAR LİSTESİ"):
                    tablolarliste = re.findall("Tablo ....", text)
                        
                                
                elif text.startswith("EKLER LİSTESİ"):
                    eklerliste = re.findall("Ek....",text)
                    son = i   # kontrolü bu sayfadan itibaren yapmak için.Çünkü baştan başlarsak var şekiller ve tablo sayfalarına tekrar bakacağı için otomatikmen var sayacaktır.
                    #print(son)
                    break




                
            for i in range(son, len(pdf.pages)):
                page = pdf.pages[i]
                text = page.extract_text()
                all_text = all_text + '\n' + text  # burada texti tek bir string biçiminde birleştiriyoruz.
            

       
            
            kaynak_index = all_text.rfind("KAYNAKLAR")
            kaynaklar_bölüm = all_text[kaynak_index:]
            kaynaklar_dısı_bölüm = all_text[:kaynak_index]
            kaynaklar_dısı_kaynakca_no = re.findall('\[.*?\]',kaynaklar_dısı_bölüm)
            atıflı = str(kaynaklar_dısı_bölüm)#replace#('-', ',')
            blok_atıf = re.findall(r"\[.*?]",atıflı) 
            kaynakca_no = re.findall('\[.*?\]',kaynaklar_bölüm)
            

            


            degistirilmiş = all_text.replace('“', '"').replace('”', '"')   # pdf de bazı tırnak işaretleri böyle(" ") olmadığı için okumuyor.O yüzdeen bu formata çeviriyoruz.
            tırnaklı = re.findall('"([^"]*)"', degistirilmiş) # iki tırnak arasındaki kelimeleri alıyoruz.
            
            if tırnaklı:  # ve listeye atıyoruz.
                c.append(tırnaklı)


            for i in range(len(c)):
                if len(c[i]) >= 2:
                    liste = c[i]
                    for j in range(len(c[i])):
                        a = liste[j]
                        control(a)
                else:
                    listToStr = ' '.join(map(str, c[i])) # listeden stringe çevirme
                    control(listToStr) # kontrol metodumuza yollayıp uzunluğunu buluyoruz.

            for j in range(len(şekilliste)):
                if şekilliste[j] not in all_text: # listedeki elemenlar metinde var mı diye kontrol ediliyor.
                    log_dosya.writelines(f'{şekilliste[j]} şekline metin içerisinde atıf yapılmamış.\n') # log dosyamıza yazıyoruz.
                    
        
            for k in range(len(tablolarliste)):
                if tablolarliste[k] not in all_text: # listedeki elemenlar metinde var mı diye kontrol ediliyor.
                    log_dosya.writelines(f'{tablolarliste[k]} tablosuna metin içerisinde atıf yapılmamış.\n')
            
            for ekler in eklerliste:
                ekler = ekler.upper()
                if ekler not in all_text: # listedeki elemenlar metinde var mı diye kontrol ediliyor.
                    log_dosya.writelines(f'{ekler} ekine metin içerisinde atıf yapılmamış.\n')
                       

            for kaynak in kaynaklar_dısı_kaynakca_no:    #bulduğumuz parantezli ifadelerin içinde gezip harf barındıranları siliyoruz.
                for harf in harfler:
                    if harf in kaynak:
                        #print(harf)
                        #print(atıf)
                        if kaynak in kaynaklar_dısı_kaynakca_no:
                            kaynaklar_dısı_kaynakca_no.remove(kaynak)
                            #print(harf)

            for item in blok_atıf:    #bulduğumuz parantezli ifadelerin içinde gezip harf barındıranları siliyoruz.
                for harf in harfler:
                    if harf in item:
                        #print(harf)
                        #print(atıf)
                        if item in blok_atıf:
                            blok_atıf.remove(item)
                            #print(harf)
  

            for i in range(len(blok_atıf)): #burada ise üst koddaki aldığımız sonuçara bakıyoruz ve uzunluğunun 5 ten büyük olup olmamasına göre kayda alacağız
                if len(blok_atıf[i]) >= 5:                   # sebebi ise blok atıflar genellikle 5 veya daha fazla karakterden oluşur.Örnek [2-4] [5,9,11]              
                    blokatıftüm = blokatıftüm + blok_atıf[i]
                    #print(blok_atıf[i])
                    log_dosya.writelines(f"{blok_atıf[i]} nolu kaynaklar metinde blok atıf olarak kullanılmış.\n")

            blok_atıf_tüm = re.findall(r"\[.*?]",blokatıftüm)

            test_item1 = blokatıftüm.replace("[",",")
            test_item2 = test_item1.replace("]"," ")
            test_item3 = test_item2.replace(" ","")
            test_item4 = test_item3.split(",")

            kaynakno = str(kaynakca_no)
            t1 = kaynakno.replace("[",",")
            t2 = t1.replace("]"," ")    #kaynakca noyu karşılaştırma için uygun formata getiriyoruz.
            t3 = t2.replace(" ","")     #kaynak no için calısan kod
            t4 = t3.replace("'","")
            t5 = t4.split(",")

            kaynakca_dısı = str(kaynaklar_dısı_kaynakca_no)
            k1 = kaynakca_dısı.replace("[",",")
            k2 = k1.replace("]"," ")
            k3 = k2.replace(" ","")     #aynısını kaynak dısı bölüme uyguluyoruz
            k4 = k3.replace("'","")
            k5 = k4.split(",")

            

            for element in test_item4:
                if len(element) > 2 and "–" in element:
                    denek = denek + element  + "–" #burada gerekli şartları sağlayan listenin itemnlerini birleştiriyoruz.
            
            atıf_pars = denek.split("–")  #bazı yerlerde iki sayı arasında diyerek atıf yapılmış buna göre parçalıyoruz.
            atıf_pars.remove('')


            kaynaklar_liste = []


           

            #last_element =  int(atıf_pars[-1])

            #print(atıf_pars)
            i = 0
            while i < len(atıf_pars):


                j = int(atıf_pars[i]) #ilk indeksteki alıyoruz
                z = int(atıf_pars[i+1]) #ilkini takip eden indeksdekini alıyoruz
                k = z - j # aradaki farkı alıp for döngüsüne yolluıyoruz 
                #print("j" , j)
                #print("z",z)
                #print("k", k)
                
                #buradaki mantık tamamen şu örnek 2-4 atıfımız var bu atıf 2 3 4 numaramalı kaynakları işaret ediyor.Eğer farkı alıp tekrar baştakine ekleyerek gidersek bize 2 3 4 ü verecektir.

                for t in range(1,k+1):
                    
                    kaynaklar_liste.append(j)
                    kaynaklar_liste.append(j+t)

                i += 2

                          
                
            kaynaklar_liste = str(kaynaklar_liste) # strip ve split gibi string metodlarını uygulayabilmek için stringe çeviriyoruz.
            kaynaklar_liste = kaynaklar_liste.strip("[").strip("]")    #kaynaklar listesini düzenli ve if döngüsü tarafından anlaşılacak gormata sokuyoruz.
            kaynaklar_liste = kaynaklar_liste.replace(" ",'') # önceki çıktı [2, 3, 2, 4, 5, 6, 5, 7, 9, 10, 9, 11, 9, 12, 9, 10, 9, 11, 60, 61, 60, 62, 60, 63, 60, 64]
            kaynaklar_liste = kaynaklar_liste.split(',') #şimdiki çıktı 2,3,2,4,5,6,5,7,9,10,9,11,9,12,9,10,9,11,60,61,60,62,60,63,60,64
          
            
                        
            for i in kaynaklar_liste:    # burada kaynaklar listemiz bize sürekli aynı cıktıyı vereceği için aynı olanları elimine edip log kısmında tekrarı engelliyoryz
                if i not in kaynak_liste2: 
                        kaynak_liste2.append(i)




            for kaynakca in t5:                
                if kaynakca not in k5: # blok atıf farklı türde oldugu için bazen göremeyebiliyor o yüzden çift kontrole sokuyoruz.
                        if kaynakca not in kaynak_liste2:
                        #for kaynakca in kaynak_liste2:
                            #if kaynakca not in t5:
                                #
                                # kaynakca_hata.append(kaynakca)
                                #print(kaynakca)"""
                            log_dosya.writelines(f"[{kaynakca}] nolu kaynakçaya metin içinde atıf yapılmamış.\n") # metin içerisinde kaynakça geçiyor mu diye kontrol ediyoruz.
                                #kaynak_liste2.remove(kaynakca)
                            #elif kaynakca not in:



            #fark = (list(list(set(blok_atıf)-set(kaynaklar_dısı_kaynakca_no)) + list(set(kaynaklar_dısı_kaynakca_no)-set(blok_atıf))))   #elimizdeki atıf listesiyle kaynakca dısı kaynak noyu birbirinden cıkarıyoruz ve blok atıf kaynakcalarını yok saymasını engelliyoruz.
  

            #for farkitem in fark:
            #   if fark != []:
            #      log_dosya.writelines(f"{farkitem} nolu kaynakça metin içinde geçiyor ancak kaynaklar bölümünde yok.\n")



            #print("------------------------")
            #print(fark)


            for kaynakca_metin in kaynaklar_dısı_kaynakca_no:
                if kaynakca_metin not in kaynaklar_bölüm:
                    if kaynakca_metin not in blok_atıf_tüm:
                   
                        log_dosya.writelines(f"{kaynakca_metin} nolu kaynakça metin içinde geçiyor ancak kaynaklar bölümünde yok.\n")
                        
  
    except:
       cprint("Beklenmedik bir hatayla karşılaştık lütfen tekrar deneyiniz.", 'red', attrs=['bold'], file=sys.stderr)
       sys.exit()


if __name__ == "__main__":




    cprint("[+]İşlem Modunu Seçiniz", 'red', attrs=['bold'], file=sys.stderr)
    cprint("1.Otomatik Mod \n2.Manuel mod\n3.Yazma Modu\n4.Çıkış-->'x'", 'red', attrs=['bold'], file=sys.stderr)
    
    while True:
        mod = input(">>")


        if mod == 'x':
            
            sys.exit()

        elif mod == "1":
            cprint("Otomatik Mod Başlatılıyor..", 'red', attrs=['bold'], file=sys.stderr)
            time.sleep(0.5)
            for pdf in dosyalar:
                cprint(f"{pdf} adlı dosya kontrol ediliyor..", 'red', attrs=['bold'], file=sys.stderr)
                log_dosya = open(f"{pdf[:-4]}.txt","w",encoding="utf-8")
                islem(pdf)
                cprint(f"{pdf} adlı dosyanın kontrol sonuçları yazdırılıyor.", 'red', attrs=['bold'], file=sys.stderr)
                time.sleep(0.5)
                log_dosya.close()
            uyarı()
            sys.exit()

        elif mod == "2":           
            file_path = filedialog.askopenfilename() #dosya seçim ekranını yazırma
            if file_path.endswith(".pdf"):#if else kontrol bloklarıyla kullancıya daha güzel hata mesajları yazdırıyoruz.
                dosya_format = file_path[:-4]
                cprint("Kontrol işlemi başlatılıyor.", 'red', attrs=['bold'], file=sys.stderr)
                log_dosya = open(f"{dosya_format}.txt","w",encoding="utf-8")
                islem(file_path)
                log_dosya.close()
                cprint(f"İşleminiz Tamamlandı.", 'red', attrs=['bold'], file=sys.stderr)
                
            elif  file_path == '':
                cprint("Dosya seçilmedi sistemden çıkılıyor.", 'red', attrs=['bold'], file=sys.stderr)
                time.sleep(1)
                root.destroy() 
                sys.exit()
            else:
                cprint("Hatalı dosya formatı lütfen sadece '.pdf' uzantılı dosyaları seçiniz..", 'red', attrs=['bold'], file=sys.stderr)
                time.sleep(2)
                root.destroy() 
                sys.exit()
            

        elif mod == "3":
            cprint("Dosya adını uzantısız olarak giriniz.", 'red', attrs=['bold'], file=sys.stderr)
            file_path = input()
            cprint("Kontrol işlemi başlatılıyor.", 'red', attrs=['bold'], file=sys.stderr)
            log_dosya = open(f"{file_path}.txt","w",encoding="utf-8")
            file_path = file_path + ".pdf"
            islem(file_path)
            log_dosya.close()
            cprint(f"İşleminiz Tamamlandı.", 'red', attrs=['bold'], file=sys.stderr)
            
                
        else:
            cprint("Hatalı Giriş Yaptınız!!!", 'red', attrs=['bold'], file=sys.stderr)
            

    