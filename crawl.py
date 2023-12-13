from lxml import etree
import requests
import json

def re_var(var):   
    return var.text if var != None else None

def get_ServiceKey(service:str) -> str:
    with open('./config.json', 'r') as f:
        data = json.load(f)
    return data[service]

def get_hospitalInfo(hpid:str):
    data = []
    uri = 'http://apis.data.go.kr/B552657/ErmctInfoInqireService/getEgytBassInfoInqire'
    params = {
        'ServiceKey': get_ServiceKey('ErmctInfoInqireService'),
        'HPID': hpid,
        'pageNo': 1,
        'numOfRows': 100,
    }

    contents = requests.get(url=uri, params=params).text
    tree = etree.fromstring(contents.encode('utf-8'))

    if tree.find('./body/items') == None: return data
    
    data = {
        'addr': tree.find('./body/items/item/dutyAddr').text,
        'lat': float(tree.find('./body/items/item/wgs84Lat').text),
        'lon': float(tree.find('./body/items/item/wgs84Lon').text)
    }
    return data


def emer_crawl(state:str, city:str=None, isAdult:bool=True):
    data = []
    uri = 'http://apis.data.go.kr/B552657/ErmctInfoInqireService/getEmrrmRltmUsefulSckbdInfoInqire'
    params = {
        'ServiceKey':get_ServiceKey('ErmctInfoInqireService'),
        'pageNo': 1,
        'numOfRows': 100,
        'STAGE1': state,
        'STAGE2': city
    }

    contents = requests.get(url=uri, params=params).text
    tree = etree.fromstring(contents.encode('utf-8'))

    if tree.find('./body/items') == None: return data
    
    items = tree.find('./body/items')
    
    for item in items.findall('./item'):
        hospital = get_hospitalInfo(item.find('./hpid').text) 
        comm = {
                'addr': hospital['addr'],
                'hvidate': item.find('./hvidate').text,
                'name': item.find('./dutyName').text,
                'tel': item.find('./dutyTel3').text,
                'lon': hospital['lon'],
                'lat': hospital['lat']
        }
        if isAdult:
            comm.update({
                'hvcc': re_var(item.find('./hvcc')),
                'hvs11': re_var(item.find('./hvs11')),
                'hvccc': re_var(item.find('./hvccc')),
                'hvs16': re_var(item.find('./hvs16')),
                'hvicc': re_var(item.find('./hvicc')),
                'hvs17': re_var(item.find('./hvs17')),
                'hv2': re_var(item.find('./hv2')),
                'hvs06': re_var(item.find('./hvs06')),
                'hv3': re_var(item.find('./hv3')),
                'hvs07': re_var(item.find('./hvs07')),
                'hv6': re_var(item.find('./hv6')),
                'hvs12': re_var(item.find('./hvs12')),
                'hv8': re_var(item.find('./hv8')),
                'hvs13': re_var(item.find('./hvs13')),
                'hv9': re_var(item.find('./hv9')),
                'hvs14': re_var(item.find('./hvs14')),
                'hvgc': re_var(item.find('./hvgc')),
                'hvs38': re_var(item.find('./hvs38')),
                'hvec': re_var(item.find('./hvec')),
                'hvs01': re_var(item.find('./hvs01')),
                'hvoc': re_var(item.find('./hvoc')),
                'hvs22': re_var(item.find('./hvs22'))
            })
        else:
            comm.update({
                'hv12': re_var(item.find('./hv12')),
                'hv10': re_var(item.find('./hv10')),
                'hv28': re_var(item.find('./hv28')),
                'hvs02': re_var(item.find('./hvs02')),
                'hv32': re_var(item.find('./hv32')),
                'hvs09': re_var(item.find('./hvs09')),
                'hv33': re_var(item.find('./hv33')),
                'hvs10': re_var(item.find('./hvs10')),
                'hv37': re_var(item.find('./hv37')),
                'hvs20': re_var(item.find('./hvs20'))
            })
        data.append(comm)
    return data

def moon_crawl(state:str, city:str=None) -> list:
    data = []
    uri = 'http://apis.data.go.kr/B552657/HsptlAsembySearchService/getBabyListInfoInqire'
    params = {
        'ServiceKey':get_ServiceKey('HsptlAsembySearchService'),
        'pageNo': 1,
        'numOfRows': 10,
        'Q0': state,
        'Q1': city
    }

    contents = requests.get(url=uri, params=params).text
    tree = etree.fromstring(contents.encode('utf-8'))

    if tree.find('./body/items') == None: return data
    
    items = tree.find('./body/items')
    for item in items.findall('./item'):
        data.append(
            {
                'addr': item.find('./dutyAddr').text,
                'name': item.find('./dutyName').text,
                'info': item.find('./dutyInf').text if item.find('./dutyInf') != None else None,
                'tel': item.find('./dutyTel1').text,
                'lon': float(item.find('wgs84Lon').text),
                'lat': float(item.find('wgs84Lat').text)
            }
        )
    return data

if __name__ == '__main__':
    print(moon_crawl('서울특별시'))
    
