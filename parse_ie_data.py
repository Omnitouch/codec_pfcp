#This hacky script passes the data in `IE_Data.csv`` and gets it into a dict

def Get_IEs():
    f = open("IE_Data.csv", "r")
    ie_data_lines = f.readlines()
    f.close()

    import re
    ie_data_dict = {}
    for ie_data in ie_data_lines:
        ie_dict = {}
        if ie_data.startswith('#'):
            #Skip comment line
            continue
        if len(ie_data.split(' ')) <=2 :
            #This is a reserved / blank line
            ie_dict['id'] = ie_data.split(' ')[0]
            ie_dict['name'] = ie_data.split(' ')[1]
        else:
            #Get ID & Name
            regex = r"(\d{1,3})\s(.+?)(?=Extendable|Fixed|Variable)(Extendable|Fixed|Variable)(.*)"
            regex_res = re.search(regex, ie_data)
            ie_dict['id'] = int(regex_res.group(1))

            #Get Name
            ie_dict['name'] = regex_res.group(2).rstrip()

            #Get Extendable status
            ie_dict['extendable'] = regex_res.group(3)

            #Get Reference
            ie_dict['reference'] = regex_res.group(4).split('/')[1].strip()
            #Strip off the Number of Octets if present
            try:
                int(ie_dict['reference'].rsplit(' ', 1)[1])
                ie_dict['reference'] = ie_dict['reference'].rsplit(' ', 1)[0].strip()
            except:
                ie_dict['reference'] = ie_dict['reference']
            #Strip the "Not Applicable" if present
            ie_dict['reference'] = ie_dict['reference'].replace('Not Applicable', '').replace('Not applicable', '')

            #Get Number of Octets
            if "not applicable" not in ie_data.lower():
                regex_raw = regex_res.group(4).strip()
                split_value = regex_raw.split(' ')[-1]
                ie_dict['number_of_octets'] = int(split_value)
            ie_data_dict[int(ie_dict['id'])] = ie_dict
            #print(ie_dict)
    return ie_data_dict


if __name__ == "__main__":
    import pprint
    pprint.pprint(Get_IEs())
        #sys.exit()