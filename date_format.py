day = {
    "Sunday":"Minggu",
    "Monday":"Senin",
    "Tuesday":"Selasa",
    "Wednesay":"Rabu",
    "Thursday":"Kamis",
    "Friday":"Jumat",
    "Saturday":"Sabtu"
}

month = {
    "January":"",
    "February": "Februari",
    "March":"Maret",
    "May":"Mei",
    "June":"Juni",
    "July":"Juli",
    "August":"Agustus",
    "October":"Oktober",
    "December":"Desember"
}


def toId(date):
    hari=day[date.strftime("%A")]
    bulan=month[date.strftime("%B")]
    tanggal=date.strftime("%d")
    tahun=date.strftime("%Y")
    return hari+", "+tanggal+" "+bulan+" "+tahun
    # date.strftime("%A, %d %B %Y")

