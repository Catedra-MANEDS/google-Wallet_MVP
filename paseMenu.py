#!/usr/bin/python3

# Import modules
from walletPass import *
from emailSender import *
from views import console

#---------------Variable de entorno---------------------
#GOOGLE_APPLICATION_CREDENTIALS=/home/samuel/Desktop/documentos-wallet/clave-googleWallet-mm-maneds-prod.json ./paseMenu.py
#--------------------------------------------------------GENERAR PASE PARA GOOGLE WALLET-----------------------------------------------------------------------#

name="Catedra"
issuer="3388000000022205571"
#Issuer ID de mis pruebas, el que esta puesto es el de MM
#3388000000022217743
clase="claseLoyaltyPepePhone"+name
objeto="objetoLealtadPepe"+name
img_url="https://i.ibb.co/0j6vB0g/junio-playa.png"
offer_url="https://i.ibb.co/gMFW2Sk/promo-800mb.png"

def mostrar_menu():
    print('\033[92m' + "************************************************************************************************" + '\033[0m')
    print("1. Crear clase y objeto")
    print("2. Update del objeto")
    print("3. Modificar imagen del mes")
    print("4. Modificar oferta")
    print("5. Add/pop text item")
    print("6. Modificar un campo de texto")
    print("7. Modificar GBs")
    print("8. Mandar email")
    print("0. Salir del menú")
    print('\033[92m' + "************************************************************************************************" + '\033[0m')


pase= DemoLoyalty()
console.print_title()

while True:
    mostrar_menu()
    opcion = console.seleccionar_opcion()

    if opcion == "1":
        pase.create_class(issuer,clase,name)
        pase.create_object(issuer,clase,objeto)
        #pase.patch_class(issuer,clase)
        #pase.update_class(issuer,clase)

    elif opcion == "2":
        #-----UPDATE----modifica el objeto por completo y lo sobreescribe
        pase.update_object(issuer,clase,objeto)
        #-----PATCH-----Modifica el objeto al completo, pero los campos que no toquen no se actualizan
        #pase.patch_object(issuer,clase,objeto)

    elif opcion == "3":
        pase.patch_main_img(issuer,objeto,img_url)

    elif opcion == "4":
        pase.patch_offer(issuer,objeto,offer_url)

    elif opcion == "5":
        # Realiza las operaciones correspondientes a la opción 4
        #-------Add text item
                #Argumento accion -->  add/pop
        accion = ""
        while True:
            accion = input("pop or add: ")
            if accion == "pop" or accion== "add":
                break
            
        pase.patch_add_text(issuer,objeto,accion)

    elif opcion == "6":
        #------Modify text item
            #Argumento cambios-->id del campo texto a alterar
        text_id = ""
        while True:
            opciones=["TEXT_MODULE_ID1", "TEXT_MODULE_ID2", "TEXT_MODULE_ID3","TEXT_MODULE_ID4"]
            print("\t1. TEXT_MODULE_ID1")
            print("\t2. TEXT_MODULE_ID2")
            print("\t3. TEXT_MODULE_ID3")
            print("\t4. TEXT_MODULE_ID4")
            #text_id = input("\nSelecciona una opción: ")
            text_id = console.seleccionar_opcion()
            text_id= int(text_id)
            if 1 <= text_id <= 4:
                text_id=opciones[text_id-1]
                break

        pase.patch_modify_text(issuer,objeto,text_id)
    
    elif opcion=="7":
        pase.patch_gigas(issuer,objeto,30)

    elif opcion == "8":
        #Genera el link para añadir a wallet
        saveLink=pase.create_jwt_new_objects(issuer,clase,objeto)
        print("\n")
        email_sender("pruebas.catedra.masmovil@gmail.com",name,saveLink)

    elif opcion == "0":
        pase.update_object(issuer,clase,objeto)
        print('\033[92m' + "***********************" + '\033[0m')
        print("Saliendo del menú...")
        break
    else:
        print("Opción inválida. Por favor, selecciona una opción válida.")


#pase.object_group(issuer,"claseLoyaltyPepePhone","objetoLealtadPepe",3)






