# pod.py


'''
    version 1.0.0
    POD.py is the very simplified version of the upcoming go implementation of POD.
    You can output the entire metadata structure for an NFT collection with a single command.
    e.g $ python3 pod.go -date:True -obj:obj
'''


''' Imports'''

import os as _
import platform
import sys as __
import json as j_
import secrets as s_
from sys import argv
from glob import iglob
from hashlib import sha256
from time import sleep, time
from random import choice, randint, uniform, sample


# Windows cmd does not support unicode characters (unless Powershell is used)
if 'Windows' in platform.system(): SP = "※"; SN = "-"; _.system("cls")
if 'Linux' in platform.system(): SP = "🟩"; SN = "⬛️"; _.system("clear")
    
    
''' Helpers '''

def open_json(file_, serious = True, msg = "[EXIT]"):
    file_json = {"Empty" : "Empty"}; filepath = _.getcwd() + file_
    try:
        with open(filepath + ".json", 'r') as r_: file_json = j_.loads(r_.read())
    except FileNotFoundError:
        print("[< {f}.json > not found]".format(f=filepath))
        if serious == True:  __.exit(msg)
    return file_json

def write_json(file_, dict_, serious = True, msg = "[EXIT]"):
    payload = False; filepath = _.getcwd() + file_
    try:
        with open(filepath + ".json", 'w') as w_:  w_.write(j_.dumps(dict_, indent = 3))
    except FileNotFoundError:
        print("[< {f}.json > not found]".format(f=filepath))
        if serious == True:  __.exit(msg)
    test = open_json(file_)
    if test == dict_: payload == True
    return payload

def map_value(value, in_min, in_max, out_min, out_max):
        in_ = in_max - in_min; out_ = out_max - out_min
        value_scaled = float(value - in_min) / float(in_)
        return out_min + (value_scaled * out_)
    
''' Sys args '''

def args():
    config_ = open_json("/POD.config")
    arg_dict = {}
    arg_dict['-offset'] = 0
    arg_dict['-obj'] = "obj"
    arg_dict['-clean'] = "True"
    arg_dict['-type'] = "opensea"
    arg_dict['-date'] = "False"
    arg_dict['-verbose'] = "False"
    arg_dict['-supply'] = config_['Collection Metadata']['Supply']
    for arg,i in zip(argv, range(len(argv))):
        if i > 0 and len(arg.split(":")) > 1:
            arg_dict[arg.split(":")[0]] = arg.split(":")[1]
    OFFSET = int(arg_dict['-offset'])
    OBJ_EXTENSION = arg_dict['-obj'] 
    CLEAN = eval(arg_dict['-clean'])
    META_TYPE = arg_dict['-type']
    DATE_B = eval(arg_dict['-date'])
    VERBOSE = eval(arg_dict['-verbose'])
    SUPPLY = int(arg_dict['-supply'])
    return OFFSET, OBJ_EXTENSION, CLEAN, META_TYPE, DATE_B, VERBOSE, SUPPLY
OFFSET, OBJ_EXTENSION, CLEAN, META_TYPE, DATE_B, VERBOSE, SUPPLY = args()

''' A small loading bar utility '''

def loading(i, limit, new_limit, comment):
    global SP, SN
    slash = ("\\ | / - "*round(limit)).split(" "); ds = " "*30
    print(" [" + comment + "]" + slash[i] + "[" + (SP*round(map_value(i,0,limit,0,new_limit))) + (SN*(new_limit-round(map_value(i,0,limit,0,new_limit)))) + "]" + ds, end = "\r")
    return None

''' Clean directory before proceding '''

def clean():
    global VERBOSE
    filepath = _.getcwd() + "/Metadata/*.json"
    files_in_dir = iglob(filepath); test_dir = iglob(filepath);i=0;I=0
    for f in test_dir: i+=1
    for _file in files_in_dir:
        _.remove(_file);loading(I,i,30,"Clean up in ./Metadata");I+=1
    if VERBOSE == True:
        print("")
    return True

''' Application intro and outro '''

def intro():
    global SUPPLY
    config_ = open_json("/POD.config")
    HASH = s_.token_hex(32)
    print("[POD][NFT Metadata generator]\n[")
    print(f" Collection: {config_['Collection Metadata']['Name']}")
    print(f"  Symbol: {config_['Collection Metadata']['Symbol']}")
    print(f"  Supply: {SUPPLY}")
    print(f"  Price per Unit: {config_['Collection Metadata']['Price']}/{config_['Collection Metadata']['Unit']}")
    print(f"  Hash: 0x{HASH}")
    return HASH

def outro(ping):
    if ping == True: ds = (" "*60); print(f" [Success]{ds}\n]")
        
        
''' 
    Token object
    Create attributes on initialization
    Dump all attributes to dictionary
    Dump dictionary to a json file in /Metadata folder
'''

class Token():
    def __init__(self, ID):
        self.ID = ID
        self.NAME = ''
        self.description = ''
        self.image = ''
        self.url = ''
        self.attributes = []
        self.hash = '0x'
        
    def dump(self):
        payload = {}
        payload['Name'] = self.NAME
        payload['Description'] = self.description
        payload['Image'] = self.image
        payload['External_Url'] = self.url
        payload['Attributes'] = self.attributes
        payload['Hash'] = self.hash
        return payload
    
    def dump2_file(self):
        payload = self.dump()
        write_json("/Metadata/"+str(self.ID), payload)
        
''' Main function '''

def GENERATE():
    CHASH = intro()
    sleep(.5)
    LOADING_BAR = 30
    global OFFSET, OBJ_EXTENSION, CLEAN, META_TYPE, DATE_B, VERBOSE, SUPPLY
    # DELETE ALL EXISTING TOKENS B4 creating new ones
    if CLEAN == True: clean()
    # Open config file
    config_ = open_json("/POD.config")
    ITERATIONS = SUPPLY
    # CREATE TOKENS
    tokens = []
    for ID in range(OFFSET, ITERATIONS):
        tokens.append(Token(ID))
        loading(ID, ITERATIONS, LOADING_BAR, "Creating tokens")
    if VERBOSE == True:
        print("")

    # LOAD OBJECTS
    objects_path = _.getcwd()+"/Attributes/Objects/*.{extension}".format(extension = OBJ_EXTENSION)
    objects_dir = iglob(objects_path); OBJECTS = []; test_dir = iglob(objects_path); i = 0; I = 0
    for obj in test_dir: i+=1
    for object in objects_dir:
        OBJECTS.append(object[len(object[0:len(_.getcwd()+"/Attributes/Objects/")]):-1][0:len(object[len(object[0:len(_.getcwd()+"/Attributes/Objects/")]):-1])-len(OBJ_EXTENSION)])
        I += 1;loading(I, i , LOADING_BAR, "Loading Objects")
    if VERBOSE == True:
        print("")

    # Read ATTRIBUTES FILE
    ATTRIBUTES = open_json("/Attributes/Attributes.config")

    # POPULATE TOKEN AND WRITE TO DISK
    for token in tokens:
        if META_TYPE == "opensea":
            atts = [{} for _ in range(len(ATTRIBUTES['ATTRIBUTES']))]
            token_objects = []
            for att,at in zip(ATTRIBUTES['ATTRIBUTES'], atts):
                if att['type'] == 'number_display':
                    at['trait_type'] = att['trait_type']
                    at['value'] = randint(att['min'], att['max'])
                    at['display_type'] = att['display_type']
                elif att['type'] == 'number':
                    at['trait_type'] = att['trait_type']
                    at['value'] = randint(att['min'], att['max'])
                elif att['type'] == 'object':
                    objects_to_select = list(set(OBJECTS).difference(token_objects))
                    choicee = choice(objects_to_select)
                    for obj in OBJECTS:
                        if choicee.split(" ")[1] in obj:
                            token_objects.append(obj)
                    at['trait_type'] = choicee.split(" ")[1]
                    at['value'] = choicee.split(" ")[0]
                if DATE_B == True:
                    if att['type'] == 'date':
                        at['trait_type'] = att['trait_type']
                        at['value'] = int(time())
                        at['display_type'] = att['display_type']
            token.NAME = f"{config_['Collection Metadata']['Unit']} 0x{token.ID:04d}"
            token.attributes = atts
            HASH = sha256( ''.join(sample((j_.dumps(token.dump(),sort_keys=True) + CHASH ),len((j_.dumps(token.dump(),sort_keys=True) + CHASH )))).encode('utf8') ).hexdigest()            
            token.hash = f'0x{HASH}'
            # Token Description as Markdown string
            token.description =  f'''
                                    # {token.NAME}
                                     
                                    *{token.NAME}* is part of the **{config_['Collection Metadata']['Name']}** collection of {SUPPLY} unique NFTs.
                                    
                                    ---

                                    ```json
                                    "hash":{token.hash}
                                    ```
                                    
                                    ---

                                    **{token.ID}**  |  {config_['Collection Metadata']['Symbol']}  |  *LLUSTR*
                                    '''
        token.dump2_file()
        loading(token.ID, len(tokens), LOADING_BAR, "Dumping tokens to file")
    if VERBOSE == True:
        print("")


    return True
if __name__ == '__main__':
    ping = GENERATE()
    outro(ping)

