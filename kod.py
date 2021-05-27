from bs4 import BeautifulSoup
import requests
bulgular = list()
dosya = open("dosya.txt","a",encoding="utf8")
r = requests.get("https://www.morhipo.com/markalar/0/marka")
source = BeautifulSoup(r.content,"lxml")
liler = source.findAll("li",attrs={"class":"chaar-item col-xxs-12 col-xs-6 col-sm-3"})
urller = list()
sayac = 0
for li in liler:
  sayac = sayac + 1
  if sayac<3500:
    urller.append("https://www.morhipo.com/"+li.find("a")["href"])
  else:
    break
print(len(urller))
linkler = list()
for url in urller:
    try:
        r = requests.get(url)
        source = BeautifulSoup(r.content,"lxml")
        urunler = source.findAll("div",attrs={"class":"ulInnerWrapDiv mh_product_container"})
        for urun in urunler:
          link = "https://www.morhipo.com/"+urun.find("a")["href"]
          print(link)
        data = requests.get(link)
        kaynak = BeautifulSoup(data.content,"lxml")
        yorumlar = kaynak.findAll("div",attrs={"class":"commenter"})
        for yorum in yorumlar:
          yildiz = yorum.find("input",attrs={"class":"starrated rating-loading"})["value"]
          icerik = yorum.find("p",attrs={"class":"bigger"})
          yildiz = yildiz[0]
          if int(yildiz)>=3:
            durum = "pozitif"
          else:
            durum = "negatif"
        bulgular.append( str(durum) +":"+ str(icerik.get_text())+"\n")
    except:
      pass
bulgular = set(bulgular)
for bulgu in bulgular:
  dosya.write(bulgu + "\n")

dosya.close()