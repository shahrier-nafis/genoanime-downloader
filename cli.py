import genoanimee as geno

geno.init()
animelink = geno.getlink()
startt = geno.getstart()
endd = geno.getend()
quality =  geno.getquality()
filetype = geno.getfiletype()
geno.main(animelink, startt, endd, quality, filetype)
geno.success(animelink)