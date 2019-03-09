day = {
    "Sunday":"Minggu",
    "Monday":"Senin",
    "Tuesday":"Selasa",
    "Wednesday":"Rabu",
    "Thursday":"Kamis",
    "Friday":"Jumat",
    "Saturday":"Sabtu"
}

month = {
    "January":"",
    "February": "Februari",
    "March":"Maret",
"April":"April",
    "May":"Mei",
    "June":"Juni",
    "July":"Juli",
    "August":"Agustus",
    "October":"Oktober",
    "November":"November",
    "December":"Desember"
}


def toId(date):
    hari=day[date.strftime("%A")]
    bulan=month[date.strftime("%B")]
    tanggal=date.strftime("%d")
    tahun=date.strftime("%Y")
    return hari+", "+tanggal+" "+bulan+" "+tahun
    # date.strftime("%A, %d %B %Y")

