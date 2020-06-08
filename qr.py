import tkinter as tk
import tkinter.messagebox
import pickle
import qrcode
from tkinter import *
import numpy
from PIL import Image, ImageDraw, ImageFont

window = tk.Tk()                               # Create root window
window.title('Welcome to the QRcode System')
window.geometry('500x400')
tk.Label(window, text='', font=('Arial', 20)).pack()
tk.Label(window, text='QRcode generate & identify', font=('Arial', 20)).pack()
# Generate QRcode
def sign_in():

    root = Tk()
    root.title('Generate QRcode')
    Label(root, text='Plz enter your IDnum:').grid(row=0, column=0)
    Label(root, text='').grid(row=1, column=0)
    e1 = Entry(root)
    e1.grid(row=0, column=1, padx=10, pady=5)

    # e2.grid(row=1, column=1, padx=10, pady=5)

    def show():
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        # print("enter info of the identity：press enter to comfrim")
        data = e1.get()  # enter date while opertaing
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="red", back_color="white")

        import matplotlib.pyplot as plt  # plt use to show image
        plt.imshow(img)  # display image
        plt.axis('off')  # xy off
        plt.show()

    Button(root, text='Generate QRcode', width=10, command=show).grid(row=3, column=0, sticky=W, padx=10, pady=5)

    Button(root, text='Exit', width=10, command=root.quit).grid(row=3, column=1, sticky=E, padx=10, pady=5)

    
    mainloop()
# QRcode identify
def b_register():
    import cv2                         # use CV2 to open up camera
    import pyzbar.pyzbar as pyzbar     # pyzbar analysis QRcode


    # root.mainloop()

    def decodeDisplay(image):
        barcodes = pyzbar.decode(image)  
        for barcode in barcodes:
                                       
            (x, y, w, h) = barcode.rect
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 225, 0), 2)

                                                                
            barcodeData = barcode.data.decode("")
                                                                 
            barcodeType = barcode.type
                                                                  
            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        .5, (225, 225, 225), 2)

                                                                  
            print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
            # root = Tk()
            # w = Label(root, text=t)
            # w.pack()
            # root.mainloop()
            # t="[INFO] Found {} barcode: {}".format(barcodeType, barcodeData)

        return image

    def detect():
        camera = cv2.VideoCapture(0)
                                                                     
        while (1):
                                                                  
            ret, frame = camera.read()
                                                                    
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            im = decodeDisplay(gray)
            cv2.waitKey(5)
                                                                   
            cv2.imshow("camera", im)
                                                                    
            if cv2.waitKey(1) == ord('Q'):
                break
        camera.release()
        cv2.destroyAllWindows()

    if __name__ == '__main__':
        detect()
# Video ideinfy
def a_register():
    import cv2
    import pyzbar.pyzbar as pyzbar

    def decodeDisplay(image):
        barcodes = pyzbar.decode(image)  
        for barcode in barcodes:
         
            (x, y, w, h) = barcode.rect
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 225, 0), 2)
           
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type
            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(image, text, (x, y - 15), cv2.FONT_HERSHEY_COMPLEX,0.8, (0, 0, 255), 2)
          
            print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
        return image

    def detect():
        camera = cv2.VideoCapture(r'C:\Users\Administrator\Documents\Tencent Files\2879663097\FileRecv\MobileFile\SVID_20200104_214804_1.mp4')
        while (1):
            ret, frame = camera.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            im = decodeDisplay(gray)
            cv2.waitKey(8)
            cv2.imshow("camera", im)
            # press q exit loop
            if cv2.waitKey(1) == ord('Q'):
                break
        camera.release()
        cv2.destroyAllWindows()

    if __name__ == '__main__':
        detect()

def distinguish():
    window_distinguish = tk.Toplevel(window)
    # window_distinguish = tk.Tk()
    window_distinguish.title('QRcode Identify sys')
    window_distinguish.geometry('350x200')
    Label(window_distinguish, text='Plz enter the way you want to identify your QRcode：',font=('Arial',14)).place(x=10,y=5)
    Button(window_distinguish, text='Real-time identification', font=('Arial', 16), fg='black', command=b_register).place(x=30, y=80)
    Button(window_distinguish, text='video identification', font=('Arial', 16), fg='black', command=a_register).place(x=160, y=80)

tk.Button(window, text='QRcode identified', font=('Arial', 16), fg='red',command=distinguish).place(x=280, y=220)
tk.Button(window, text='QRcode generated',font=('Arial',16),fg='green',command=sign_in).place(x=70,y=220)
window.mainloop()     
