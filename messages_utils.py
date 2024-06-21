import sys
from os import path
from struct import unpack
from json import dump

def read_messages(data: bytearray, messages_count: int) -> dict:
    """
    Reads messages from a bytearray and returns a dictionary containing the messages and their headers.

    Args:
        data (bytearray): The bytearray containing the messages.
        messages_count (int): The number of messages in the bytearray.

    Returns:
        dict: A dictionary containing the messages and their headers. The dictionary has the following structure:
            {
                message_id (int): {
                    'message_length_in_bytes' (int): The length of the message in bytes.
                    'message_length_in_rasters' (int): The length of the message in rasters.
                    'eth_setting' (int): The Ethernet setting.
                    'inter_raster_width' (int): The inter-raster width.
                    'print_delay' (int): The print delay.
                    'message_name_string' (str): The name of the message.
                    'message_type_string' (str): The type of the message.
                    'message_name_bytes' (str): The name of the message in hexadecimal.
                    'fields' (dict): A dictionary containing the fields of the message.
                }
            }
    """

    messages = {}
    for n in range(messages_count): # messages iterator
        if data[41] != 28:
            message_length_in_bytes, \
            message_length_in_rasters, \
            eth_setting, \
            inter_raster_width, \
            print_delay, message_name_string, message_type_string = unpack('<2HB2H16s16s', data[:41])

            if message_length_in_bytes > 1000: # TODO rever a possiblidade de pegar somente o message length
                del data[0] # remover byte inicial se o byte na posição 41 for diferente de 1C(Field header character
            else:
                del data[-1]

        message_length_in_bytes, \
        message_length_in_rasters, \
        eth_setting, \
        inter_raster_width, \
        print_delay, message_name_string, message_type_string = unpack('<2HB2H16s16s', data[:41]) # desempacota cada variável do cabeçalho

        del data[:41] # apagar cabeçalho da mensagem n + 1

        message_header = {'message_length_in_bytes': message_length_in_bytes,
                        'message_length_in_rasters': message_length_in_rasters,
                        'eth_setting': eth_setting,
                        'inter_raster_width': inter_raster_width,
                        'print_delay': print_delay,
                        'message_name_string': message_name_string.replace(b'\x00', b'').decode(errors='ignore'),
                        'message_name_bytes': message_name_string.hex(),
                        'message_type_string': message_type_string.replace(b'\x00', b'').decode(errors='ignore')}
    
        messages[n+1] = message_header
        fields = {}
        _pos_field = 41 # valor inicial é o tamanho do cabeçalho da mensagem e é incrimentado com o tamanho de cada campo para sair do while quando for maior que o tamanho da mensagem
        n_field = 1

        while _pos_field < message_header['message_length_in_bytes']:
                if len(data) == 0: break
                if data[0] == 28: # validar se primeiro caractere é 1c
                    # campo
                    field_header_character, \
                    field_type, \
                    field_length_in_bytes, \
                    y_position, \
                    x_position, \
                    field_length_in_rasters, \
                    field_height_in_drops, \
                    format_3, \
                    bold_multiplier, \
                    text_length, \
                    format_1, \
                    format_2, \
                    linkage, \
                    data_set_name = unpack('<2BHB2H7B16s', data[:32])
                    field_complement = unpack(f'<{field_length_in_bytes - 32}s', data[32:field_length_in_bytes])[0]

                    field = {
                        'field_header_character': field_header_character,
                        'field_type': field_type,
                        'field_length_in_bytes': field_length_in_bytes,
                        'y_position': y_position,
                        'x_position': x_position,
                        'field_length_in_rasters': field_length_in_rasters,
                        'field_height_in_drops': field_height_in_drops,
                        'format_3': format_3,
                        'bold_multiplier': bold_multiplier,
                        'text_length': text_length,
                        'format_1': format_1,
                        'format_2': format_2,
                        'linkage': linkage,
                        'data_set_name': data_set_name.replace(b'\x00', b'').decode(errors='ignore'),
                        'field_complement': field_complement.replace(b'\x00', b'').decode(errors='ignore')
                    }

                    fields[n_field] = field
                    n_field += 1
                    _pos_field += field['field_length_in_bytes']
                    del data[:field_length_in_bytes]
                else:
                    del data[0]
                    _pos_field += 1
            
        messages[n+1]['fields'] = fields
    
    return messages

def parse_messages(full_messages: dict) -> dict:
    '''
	Parses full messages and extracts message names, bytes, and content.
	
	Args:
	    full_messages (dict): A dictionary containing full messages with message names, bytes, and fields.
	
	Returns:
	    dict: A dictionary with parsed messages containing message names, bytes, and extracted content.
	'''

    messages: dict = {}
    for message in full_messages:

        message_name_string: str = full_messages[message]['message_name_string']
        message_name_bytes: str = full_messages[message]['message_name_bytes']

        fields: dict = full_messages[message]['fields']

        content: str = ''

        for field in fields:

            if fields[field]['field_type'] == 0:
                content += fields[field]['field_complement'] + ' '

        content = content.strip()   
        
        messages[message] = {
            'message_name_string': message_name_string,
            'message_name_bytes': message_name_bytes,
            'content': content
        }
        
    return messages

def convert_messages() -> None:
    '''Convert binary messages to json    
    '''

    this_file_path: str = path.abspath(path.dirname(__file__))

    message_dat_path: str = path.join(this_file_path, 'messages.dat')

    if not path.exists(message_dat_path): sys.exit(1) # message file not found
    
    data: bytearray = bytearray()

    # open file
    with open(message_dat_path, 'rb') as f:
        data = bytearray(f.read())

    if len(data) <= 7: sys.exit(1) # message length not valid, not message data. See Linx-RCI manual CHAPTER 3: RECEIVING DATA FROM THE PRINTER

    del data[0:5] # remove ESC | ACK/NAK | P-STATUS | C-STATUS | Command ID
    
    messages_count: int = data[0]
    del data[0] # remove messages count byte

    messages: dict = read_messages(data=data, messages_count=messages_count)

    # write json
    with open('full_messages.json', 'w', encoding='utf-8') as f:
        dump(messages, f, indent=4, ensure_ascii=False)

    messages = parse_messages(full_messages=messages)

    with open('messages.json', 'w', encoding='utf-8') as f:
        dump(messages, f, indent=4)