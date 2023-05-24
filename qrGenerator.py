#Library for generating QRCodes
import qrcode    

#--------------------------------------------------------GENERAR QR VINCULADO AL PASE-----------------------------------------------------------------------#
def qrGenerator(data):
    #Creating an instance of QRCode class, it automatically selects the best version fit for the data used
    qr = qrcode.QRCode(version = 1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size = 10, border = 5)
    # Adding data to the instance 'qr'
    qr.add_data(data)
    qr.make(fit = True)
    img = qr.make_image(fill_color = 'black', back_color = 'white')
    img.save('/home/samuel/Desktop/prototipoPase/resources/contratoQR.png')