import qrcode
def qrcreator(data, name):
    qr  = qrcode.QRCode(version=1,
                        error_correction=qrcode.ERROR_CORRECT_L,
                        box_size=20,
                        border=5)
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black",back_color="white")
    img.save("qrshilda\\"+name+".jpg")