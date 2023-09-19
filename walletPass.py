import json
import os
import uuid

from google.auth.transport.requests import AuthorizedSession
from google.oauth2.service_account import Credentials
from google.auth import jwt, crypt



class DemoLoyalty:

    """
    Attributes:
        key_file_path: Path to service account key file from Google Cloud Console. 
            Environment variable: GOOGLE_APPLICATION_CREDENTIALS.
        base_url: Base URL for Google Wallet API requests.
    """

    def __init__(self):
        self.key_file_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS',
                                            '/path/to/key.json')
        self.base_url = 'https://walletobjects.googleapis.com/walletobjects/v1'
        self.batch_url = 'https://walletobjects.googleapis.com/batch'
        self.class_url = f'{self.base_url}/loyaltyClass'
        self.object_url = f'{self.base_url}/loyaltyObject'

        # Set up authenticated client
        self.auth()

    # [END setup]

    # [START auth]
    def auth(self):
        """Create authenticated HTTP client using a service account file."""
        self.credentials = Credentials.from_service_account_file(
            self.key_file_path,
            scopes=['https://www.googleapis.com/auth/wallet_object.issuer'])

        self.http_client = AuthorizedSession(self.credentials)

    # [END auth]

    def create_class(self, issuer_id: str, class_suffix: str,name) -> str:

        #Add name as a property to the class
        self.name=name
        # Check if the class exists
        response = self.http_client.get(
            url=f'{self.class_url}/{issuer_id}.{class_suffix}')

        if response.status_code == 200:
            print(f'Class {issuer_id}.{class_suffix} already exists!')
            return f'{issuer_id}.{class_suffix}'
        elif response.status_code != 404:
            # Something else went wrong...
            print(response.text)
            return f'{issuer_id}.{class_suffix}'

        # See link below for more information on required properties
        # https://developers.google.com/wallet/generic/rest/v1/genericclass
        new_class=self.generate_class_json(issuer_id,class_suffix,name)

        response = self.http_client.post(url=self.class_url, json=new_class)

        print('Class insert response')
        print(response.text)

        #return response.json().get('id')
        return response.json()

    # [END createClass]
    def generate_class_json(self, issuer_id, class_suffix,name):
        new_class = {
            'id': f'{issuer_id}.{class_suffix}',
            'issuerName': 'PepePhone',
            'reviewStatus': 'UNDER_REVIEW',
            'programName': f'Bienvenido, {name}',
            'header': {
                'defaultValue': {
                    'language': 'en-US',
                    'value': 'Samuel Rodriguez'
                }       
            },
            'programLogo': {
                'sourceUri': {
                    'uri':
                        'https://i.ibb.co/NNZwWPH/pepe-phone-logo-peque-Tamano-Px-Google.png'
                },
                'contentDescription': {
                    'defaultValue': {
                        'language': 'en-US',
                        'value': 'PepePhone logo'
                    }
                }
            },
            'linksModuleData': {
                'uris': [
                    {
                        'uri': 'tel:2373',
                        'description': 'Atención al cliente',
                        'id': 'LINK_MODULE_TEL_ID'
                    },
                    {
                        'uri': 'https://www.pepephone.com/',
                        'description': 'Visita nuestra web',
                        'id': 'LINK_MODULE_WEB_ID'
                    }
                ]
            },
        }
        return new_class

    # [END createClass]

    # [START updateClass]
    def update_class(self, issuer_id: str, class_suffix: str) -> str:
        """Update a class.

        **Warning:** This replaces all existing class attributes!

        Args:
            issuer_id (str): The issuer ID associated to the Google Wallet Api .
            class_suffix (str): Unique ID for the pass class.
        """

        # Check if the class exists
        response = self.http_client.get(
            url=f'{self.class_url}/{issuer_id}.{class_suffix}')

        if response.status_code == 404:
            print(f'Class {issuer_id}.{class_suffix} not found!')
            return f'{issuer_id}.{class_suffix}'
        elif response.status_code != 200:
            # Something else went wrong...
            print(response.text)
            return f'{issuer_id}.{class_suffix}'

        # Class exists
        updated_class = response.json()
        
        # Note: reviewStatus must be 'UNDER_REVIEW' or 'DRAFT' for updates
        updated_class['reviewStatus'] = 'UNDER_REVIEW'

        updated_class=self.generate_class_json(issuer_id, class_suffix, self.name)
        response = self.http_client.put(
            url=f'{self.class_url}/{issuer_id}.{class_suffix}',
            json=updated_class)

        print('Class update response')
        print(response.text)

        return response.json().get('id')

    # [END updateClass]

    # [START addMessageClass]
    def add_class_message(self, issuer_id: str, class_suffix: str, header: str, body: str) -> str:
        """Add a message to a pass class.

        Args:
            issuer_id (str): The issuer ID associated to the Google Wallet Api .
            class_suffix (str): Unique ID for the pass class.
            header (str): The message header.
            body (str): The message body.

        """

        # Check if the class exists
        response = self.http_client.get(
            url=f'{self.class_url}/{issuer_id}.{class_suffix}')

        if response.status_code == 404:
            print(f'Class {issuer_id}.{class_suffix} not found!')
            return f'{issuer_id}.{class_suffix}'
        elif response.status_code != 200:
            # Something else went wrong...
            print(response.text)
            return f'{issuer_id}.{class_suffix}'

        response = self.http_client.post(
            url=f'{self.class_url}/{issuer_id}.{class_suffix}/addMessage',
            json={'message': {
                'header': header,
                'body': body
            }})

        print('Class addMessage response')
        print(response.text)

        return response.json().get('id')

    # [END addMessageClass]

    def create_object(self, issuer_id: str, class_suffix: str,object_suffix: str) -> str:
        """Create an object.

        Args:
            issuer_id (str): The issuer ID associated to the Google Wallet Api .
            class_suffix (str): Unique ID for the pass class.
            object_suffix (str): Unique ID for the pass object.

        """

        # Check if the object exists
        response = self.http_client.get(
            url=f'{self.object_url}/{issuer_id}.{object_suffix}')

        if response.status_code == 200:
            print(f'Object {issuer_id}.{object_suffix} already exists!')
            print(response.text)
            return f'{issuer_id}.{object_suffix}'
        elif response.status_code != 404:
            # Something else went wrong...
            print(response.text)
            return f'{issuer_id}.{object_suffix}'

        # See link below for more information on required properties
        # https://developers.google.com/wallet/generic/rest/v1/genericobject
        new_object=self.generate_object_json(issuer_id, class_suffix, object_suffix)
        # Create the object
        response = self.http_client.post(url=self.object_url, json=new_object)

        print('Object insert response')
        print(response.text)

        #return response.json().get('id')
        return response.json()

    # [END createObject]
    def generate_object_json(self, issuer_id, class_suffix, object_suffix):
        new_object = {
            'id': f'{issuer_id}.{object_suffix}',
            'classId': f'{issuer_id}.{class_suffix}',
            'state': 'ACTIVE',
            #Campos para la agrupacion de pases
            #   "groupingInfo": {
            #     # Note the same groupingId value
            #     "groupingId": "contrato",
            #     "sortIndex": index
            # },
            'heroImage': {
                'sourceUri': {
                    'uri':
                        'https://i.ibb.co/1s8KQMH/imagen-principal-mayo.png'
                },
                'contentDescription': {
                    'defaultValue': {
                        'language': 'en-US',
                        'value': 'Hero image description'
                    }
                }
            },
            'textModulesData': [
                {
                'header': 'Linea principal del contrato',
                'body': '654654654',
                'description' : 'tus datos restantes',
                'id': 'TEXT_MODULE_ID1'
                },
                {
                'header': 'Linea secundaria del contrato',
                'body': '654654654',
                'id': 'TEXT_MODULE_ID2'
                },
                {
                'header': 'Facturacion del mes actual',
                'body': '48€',
                'id': 'TEXT_MODULE_ID3'
                },
            ],
            'disableExpirationNotification':'false',
            'imageModulesData': [{
                'mainImage': {
                    'sourceUri': {
                        'uri':
                            'https://i.ibb.co/1Mb8MtB/oferta-500mb.png'
                    },
                    'contentDescription': {
                        'defaultValue': {
                            'language': 'en-US',
                            'value': 'Image module description'
                        }
                    }
                },
                'id': 'IMAGE_MODULE_ID'
            }],
            'barcode': {
                'type': 'QR_CODE',
                'value': 'QR Code',
                "alternateText": "Mas información en detalles"
            },
            # 'accountId': 'Account id',
            # 'accountName': 'Samuel Rodriguez',
            'loyaltyPoints': {
                'label': 'GBs contratados',
                'balance': {
                    'int': 45
                }
            },
            'secondaryLoyaltyPoints': {
                'label': 'GBs restantes',
                'balance': {
                    'int': 30
                }
            },
        }
        return new_object


    # [START updateObject]
    def update_object(self, issuer_id: str,class_suffix, object_suffix: str) -> str:
        """Update an object.

        **Warning:** This replaces all existing object attributes!

        """

        # Check if the object exists
        response = self.http_client.get(
            url=f'{self.object_url}/{issuer_id}.{object_suffix}')

        if response.status_code == 404:
            print(f'Object {issuer_id}.{object_suffix} not found!')
            return f'{issuer_id}.{object_suffix}'
        elif response.status_code != 200:
            # Something else went wrong...
            print(response.text)
            return f'{issuer_id}.{object_suffix}'

        # Object exists
        updated_object = response.json()

        updated_object=self.generate_object_json(issuer_id,class_suffix, object_suffix)
        response = self.http_client.put(
            url=f'{self.object_url}/{issuer_id}.{object_suffix}',
            json=updated_object)

        print('Object update response')
        print(response.text)

        return response.json().get('id')

    # [END updateObject]

    #Patch del objeto al completo
    def patch_object(self, issuer_id: str,class_suffix,object_suffix: str) -> str:
        """Patch an object"""
        
        # Check if the object exists
        response = self.http_client.get(
            url=f'{self.object_url}/{issuer_id}.{object_suffix}')

        if response.status_code == 404:
            print(f'Object {issuer_id}.{object_suffix} not found!')
            return f'{issuer_id}.{object_suffix}'
        elif response.status_code != 200:
            # Something else went wrong...
            print(response.text)
            return f'{issuer_id}.{object_suffix}'

        # Object exists

        objeto_patch=self.generate_object_json(issuer_id,class_suffix, object_suffix)

        response = self.http_client.patch(url=f'{self.object_url}/{issuer_id}.{object_suffix}',json=objeto_patch)
        
        print('Object patch mesage')
        print(response.text)

        return response.json().get('id')

    #Argumento accion -->  add/pop
    def patch_add_text(self, issuer_id: str, object_suffix: str, accion: str) -> str:

        response = self.http_client.get(url=f'{self.object_url}/{issuer_id}.{object_suffix}')

        if response.status_code == 404:
            print(f'Object {issuer_id}.{object_suffix} not found!')
            return f'{issuer_id}.{object_suffix}'
        elif response.status_code != 200:
            # Something else went wrong...
            print(response.text)
            return f'{issuer_id}.{object_suffix}'
        # Object exists
        existing_object = response.json()

        # Body to be patch
        patch_body = {}
        new_textData= {
                'header': 'Fibra contratada',
                'body': '300Mb',
                'description' : 'tus datos restantes',
                'id': 'TEXT_MODULE_ID4'
                }

        if existing_object.get('textModulesData'):
            patch_body['textModulesData'] = existing_object['textModulesData']
            if accion=="add":
                patch_body['textModulesData'].append(new_textData)
            elif accion=="pop":
                patch_body['textModulesData'].pop()
        else:
            patch_body['textModulesData'] = new_textData
        #patch_body['textModulesData'].clear()

        response = self.http_client.patch(url=f'{self.object_url}/{issuer_id}.{object_suffix}',json=patch_body)
        
        print('Textfield add/pop response')
        print(response.text)

    #Argumento cambios-->id del campo texto a alterar
    def patch_modify_text(self, issuer_id: str, object_suffix: str, cambios: str) -> str:

        response = self.http_client.get(url=f'{self.object_url}/{issuer_id}.{object_suffix}')

        if response.status_code == 404:
            print(f'Object {issuer_id}.{object_suffix} not found!')
            return f'{issuer_id}.{object_suffix}'
        elif response.status_code != 200:
            # Something else went wrong...
            print(response.text)
            return f'{issuer_id}.{object_suffix}'
        # Object exists
        existing_object = response.json()

        # Patch the object by adding a link
        patch_body = {}

        if existing_object.get('textModulesData'):
            patch_body['textModulesData'] = existing_object['textModulesData']
            #Recorremos los diferentes campos de texto
            for x in patch_body['textModulesData']:
                match x['id']:
                    case "TEXT_MODULE_ID1":
                        if cambios =="TEXT_MODULE_ID1":
                            x['header']='Linea principal del contrato'
                            x['body']= '655486999'
                    case "TEXT_MODULE_ID2":
                         if cambios =="TEXT_MODULE_ID2":
                            x['header']='Linea secundaria del contrato'
                            x['body']= '608686952'
                    case "TEXT_MODULE_ID3":
                         if cambios =="TEXT_MODULE_ID3":
                            x['header']='Facturación del mes actual'
                            x['body']= '60€'
                    case "TEXT_MODULE_ID4":
                         if cambios =="TEXT_MODULE_ID4":
                            x['header']='Fibra contratada'
                            x['body']= '300Mb'

        response = self.http_client.patch(url=f'{self.object_url}/{issuer_id}.{object_suffix}',json=patch_body)
        
        print('#Argumento accion -->  add/pop response')
        print(response.text)

    def patch_main_img(self, issuer_id: str, object_suffix: str, img_url: str) -> str:

        response = self.http_client.get(url=f'{self.object_url}/{issuer_id}.{object_suffix}')

        if response.status_code == 404:
            print(f'Object {issuer_id}.{object_suffix} not found!')
            return f'{issuer_id}.{object_suffix}'
        elif response.status_code != 200:
            # Something else went wrong...
            print(response.text)
            return f'{issuer_id}.{object_suffix}'
        # Object exists
        existing_object = response.json()

        # Body to be patch
        patch_body= existing_object
        if existing_object.get('heroImage'):
            patch_body['heroImage']['sourceUri']['uri']=img_url

        response = self.http_client.patch(url=f'{self.object_url}/{issuer_id}.{object_suffix}',json=patch_body)
        
        print('Main img patch response')
        print(response.text)
    
    def patch_offer(self, issuer_id: str, object_suffix: str, img_url: str) -> str:

        response = self.http_client.get(url=f'{self.object_url}/{issuer_id}.{object_suffix}')

        if response.status_code == 404:
            print(f'Object {issuer_id}.{object_suffix} not found!')
            return f'{issuer_id}.{object_suffix}'
        elif response.status_code != 200:
            # Something else went wrong...
            print(response.text)
            return f'{issuer_id}.{object_suffix}'
        # Object exists
        existing_object = response.json()

        # Body to be patch
        patch_body= existing_object
        if existing_object.get('imageModulesData'):
            patch_body['imageModulesData'][0]['mainImage']['sourceUri']['uri']=img_url

        response = self.http_client.patch(url=f'{self.object_url}/{issuer_id}.{object_suffix}',json=patch_body)
        
        print('Main img patch response')
        print(response.text)

    def patch_gigas(self, issuer_id: str, object_suffix: str, gigas: int) -> str:

        response = self.http_client.get(url=f'{self.object_url}/{issuer_id}.{object_suffix}')

        if response.status_code == 404:
            print(f'Object {issuer_id}.{object_suffix} not found!')
            return f'{issuer_id}.{object_suffix}'
        elif response.status_code != 200:
            # Something else went wrong...
            print(response.text)
            return f'{issuer_id}.{object_suffix}'
        # Object exists
        existing_object = response.json()

        # Body to be patch
        patch_body= existing_object
        if existing_object.get('secondaryLoyaltyPoints'):
            patch_body['secondaryLoyaltyPoints']['balance']['int'] = gigas

        response = self.http_client.patch(url=f'{self.object_url}/{issuer_id}.{object_suffix}',json=patch_body)
        
        print('Main img patch response')
        print(response.text)

    # [START jwtNew]
    def create_jwt_new_objects(self, issuer_id: str, class_suffix: str,object_suffix: str) -> str:

        new_class = {
            'id': f'{issuer_id}.{class_suffix}',
            'issuerName': 'Issuer name',
            'reviewStatus': 'UNDER_REVIEW',
        }

        # See link below for more information on required properties
        # https://developers.google.com/wallet/retail/loyalty-cards/rest/v1/loyaltyobject
        new_object = {
            'id': f'{issuer_id}.{object_suffix}',
            'classId': f'{issuer_id}.{class_suffix}',
            'state': 'ACTIVE',
        }
        # Create the JWT claims
        claims = {
            'iss': self.credentials.service_account_email,
            'aud': 'google',
            'origins': ['www.example.com'],
            'typ': 'savetowallet',
            'payload': {
                # The listed classes and objects will be created
                'loyaltyClasses': [new_class],
                'loyaltyObjects': [new_object],
            },
        }

        # The service account credentials are used to sign the JWT
        signer = crypt.RSASigner.from_service_account_file(self.key_file_path)
        token = jwt.encode(signer, claims).decode('utf-8')

        print('Add to Google Wallet link')
        print(f'https://pay.google.com/gp/v/save/{token}')

        return f'https://pay.google.com/gp/v/save/{token}'
    # [END jwtNew]
    
    def expire_object(self, issuer_id: str, object_suffix: str) -> str:
        """Expire an object.

        Sets the object's state to Expired. If the valid time interval is
        already set, the pass will expire automatically up to 24 hours after.

        Args:
            issuer_id (str): The issuer ID being used for this request.
            object_suffix (str): Developer-defined unique ID for the pass object.

        Returns:
            The pass object ID: f"{issuer_id}.{object_suffix}"
        """

        # Check if the object exists
        response = self.http_client.get(
            url=f'{self.object_url}/{issuer_id}.{object_suffix}')

        if response.status_code == 404:
            print(f'Object {issuer_id}.{object_suffix} not found!')
            return f'{issuer_id}.{object_suffix}'
        elif response.status_code != 200:
            # Something else went wrong...
            print(response.text)
            return f'{issuer_id}.{object_suffix}'

        # Patch the object, setting the pass as expired
        patch_body = {'state': 'EXPIRED'}

        response = self.http_client.patch(
            url=f'{self.object_url}/{issuer_id}.{object_suffix}',
            json=patch_body)

        print('Object expiration response')
        print(response.text)

