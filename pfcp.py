from parse_ie_data import Get_IEs
import socket
import sys
PFCP_Attribute_IEs = Get_IEs()

ie_dict = {}

def Vomit_UDP(hex_data, dst_ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes.fromhex(hex_data), (dst_ip, 8805))

def PFCP_IE_Decode(hex_data):
    ie_dict = {}
    ie_dict['type_id'] = int(hex_data[0:4], 16)
    #Map Type
    ie_dict['type'] = PFCP_Attribute_IEs[ie_dict['type_id']]['name']
    length = int(hex_data[4:8], 16)
    print("length is: " + str(length))
    ie_dict['raw'] = hex_data[8:8+(length*2)]
    reamaining_data = hex_data[8+(length*2):]
    print(ie_dict)
    return ie_dict, reamaining_data

def PFCP_IE_Decode_all(hex_data):
    ie_dict_list = []
    while len(hex_data) != 0:
        print("Still got " + str(len(hex_data)) + " to decode")
        ie_dict, hex_data = PFCP_IE_Decode(hex_data)
        ie_dict_list.append(ie_dict)
    return ie_dict_list

def PFCF_Decode(hex_data):
    pfcp_dict = {}
    pfcp_dict['flags'] = hex_data[0:2]
    pfcp_dict['msg_type'] = hex_data[2:4]
    pfcp_dict['length'] = hex_data[4:8]
    pfcp_dict['seid'] = hex_data[8:24]
    pfcp_dict['seqno'] = hex_data[24:30]
    pfcp_dict['spare'] = hex_data[30:32]
    pfcp_dict['ie_blob'] = hex_data[32:]
    pfcp_dict['ie_list'] = PFCP_IE_Decode_all(pfcp_dict['ie_blob'])
    return pfcp_dict


def PFCP_Factory(flags, msg_type, seid, seqno, spare, ie_list):
    hex_data = ''
    hex_data += str(format(int(seid), 'x').zfill(16))
    hex_data += str(format(int(seqno), 'x').zfill(6))
    hex_data += spare
    for ie in ie_list:
        hex_data += ie

    #Calculate Length
    length = len(hex_data)/2   
    length = str(format(int(length), 'x').zfill(4))

    #Translate Message Type
    msg_type = str(format(int(msg_type), 'x').zfill(2))

    #Put it all together
    hex_data = flags + msg_type + length + hex_data
    return hex_data

if __name__ == "__main__":
    #Stuff for testing:
    import pprint

    ie_list = [
        '003c0005007f000004',
        #FTIED
        '0039000d0200000000000000017f000004',
        #Create PDR
        '00010045003800020001001d0004000000ff0002001b00140001010016000908696e7465726e6574005d000506ac171701006c0004000000010051000400000001006d000400000001',
        #Create PDR
        '00010050003800020002001d0004000000ff000200210014000100001500020f050016000908696e7465726e6574005d000502ac171701005f000100006c0004000000020051000400000001006d000400000001',
        #Create PDR
        '00010069003800020004001d0004000000010002004a0014000100001500020f050016000908696e7465726e65740017002e0100002a7065726d6974206f75742035382066726f6d20666630323a3a322f31323820746f2061737369676e6564005f000100006c000400000003',
        #Create FAR
        '00030032006c000400000001002c0002020000040020002a0001000016000908696e7465726e65740054000a010000000075ac170005',
        #Create FAR
        '00030024006c000400000002002c0002020000040012002a0001010016000908696e7465726e6574',
        #Create FAR
        '00030032006c000400000003002c0002020000040020002a0001030016000908696e7465726e65740054000a0100000000017f000004',
        #Create URR
        '000600210051000400000001003e0001010025000300800000b500040000001e0064000108',
        #Create QER
        '0007001b006d0004000000010019000100001a000a0000003a9800000249f0',
        #Create BAR
        '005500050058000101',
        #PDN Type
        '0071000101',
        #User ID
        '008d0019070899990800000076f7085999946990966432059999999999',
        #APN/DNN
        '009f000908696e7465726e6574'
        ]

    hex_data = PFCP_Factory(flags='21', msg_type=50, seid=0, seqno=1, spare='00', ie_list=ie_list)

    Vomit_UDP(hex_data, '127.0.0.4')

    pprint.pprint(PFCF_Decode(hex_data))