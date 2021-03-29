from selenium import webdriver
from selenium.webdriver.common.keys import  Keys
import csv
import requests
import os
import schedule
import time
import json as js
import cx_Oracle
# def rep(text):
#     text=text.replace("[","").replace("]","").replace("'","").replace("'","")
#     return text


def covidmap():
    driverPath ='{}\chromedriver.exe'.format(os.path.dirname(os.path.realpath(__file__)))
    driver = webdriver.Chrome(driverPath)
    driver.get('https://www.seoul.go.kr/coronaV/coronaStatus.do')
    click =driver.find_element_by_css_selector('#container > div.layout-inner.layout-sub > div > div.move-tab > ul > li:nth-child(2) > button')
    click.send_keys(Keys.ENTER)
    count=driver.find_elements_by_css_selector('#patients > strong')
    for co in count:
        countpe=co.text.replace("※ 서울 확진자 총 ","").replace("명","")
        patientcount=int(countpe)+1
    list=[]
    os.environ["NLS_LANG"] = ".AL32UTF8"

    API_KEY = 'AIzaSyD97ijUeilolAwQ2HC-0x__pLJDIAeeZ34'

    START_VALUE = u"Unicode \u3042 3".encode('utf-8')
    END_VALUE = u"Unicode \u3042 6".encode('utf-8')
    for i in range(1,199):
        if i % 2 == 0:
            for j in range(1,10):
                date = driver.find_elements_by_css_selector(
                '#DataTables_Table_0 > tbody > tr:nth-child(' + str(i) + ') > td > p:nth-child(' + str(j) + ') > b')
                cont = driver.find_elements_by_css_selector(
                '#DataTables_Table_0 > tbody > tr:nth-child(' + str(i) + ') > td > p:nth-child(' + str(j) + ') > span')
                for d in date:
                    if len(d.text) != 0:
                        pass
                    else :
                        break
                    if d.text[0] =='1' or '2' or '3' or '4' or '5' or '6' or '7' or '8' or '9':
                        if d.text[0] == '1' or '2' or '3' or '4' or '5' or '6' or '7' or '8' or '9' and d.text[1] !='1' or '2' :
                            d='0'+d.text.replace("월 ","/").replace("일","").replace("얼","/").replace(" ","").replace(".","").replace("(","").replace(")","")
                        else:
                            d =d.text.replace("월 ", "/").replace("일", "").replace("얼","/").replace(" ","").replace(".","").replace("(","").replace(")","")
                        if '~' in d:
                            sptext=d.find('~')
                            d = d[:sptext]
                            d= (d.split())[0]
                        if '월' in d:
                            d = d.replace("월", "/")
                        if ',' in d:
                            sp_text = d.find(',')
                            d = d[:sp_text]
                            d = (d.split())[0]
                        d= d.rstrip('/')
                        if '/' not in d:
                            d1=d[:2]
                            d2=d[2:]
                            d=d1+'/'+d2
                        for c in cont:
                            ctext=c.text.replace("(","").replace(")","").replace("0","").replace("1","").replace("2","").replace("3","")\
                                .replace("4","").replace("5","").replace("6","").replace("7","").replace("8","").replace("9","").replace("0","")\
                                .replace("→","").replace("자택","").replace("→","").replace("~","").replace(":","").replace("착용","")\
                                .replace(":", "").replace("마스크", "").replace("/용산구/병원", "").replace("ㅇㅇ병원","")
                            if '병원'in ctext and ctext !='병원' and '국가지정병원'not in ctext and '치료병원'not in ctext and '수원병원' not in ctext:
                                hospi=ctext.find('병원')
                                realhospi=ctext[hospi-5:hospi+2]
                                ctext = realhospi.split()
                                if len(ctext) == 2:
                                    URL = 'https://maps.googleapis.com/maps/api/geocode/json?key=' + API_KEY + '&sensor=false&language=ko&address={}'.format(
                                        ctext)
                                    response = requests.get(URL)
                                    data = response.json()
                                    if data['results']:
                                        lat = data['results'][0]['geometry']['location']['lat']
                                        lng = data['results'][0]['geometry']['location']['lng']

                                        list.append({'person':patientcount-i,'date_': d, 'content': ctext[1],'lat':lat,'lng':lng})
                                elif  ctext:
                                    URL = 'https://maps.googleapis.com/maps/api/geocode/json?key=' + API_KEY + '&sensor=false&language=ko&address={}'.format(
                                        ctext)
                                    response = requests.get(URL)
                                    data = response.json()
                                    if data['results']:
                                        lat = data['results'][0]['geometry']['location']['lat']
                                        lng = data['results'][0]['geometry']['location']['lng']
                                        list.append({'person':patientcount-i,'date_': d, 'content': ctext[0],'lat':lat,'lng':lng})
                                else:
                                    pass
                            elif '의료원'in ctext :
                                medicenter = ctext.find('의료원')
                                realmedi = ctext[medicenter - 4:medicenter+3]
                                ctext=realmedi.split()
                                if len(ctext) == 2:
                                    URL = 'https://maps.googleapis.com/maps/api/geocode/json?key=' + API_KEY + '&sensor=false&language=ko&address={}'.format(
                                        ctext)
                                    response = requests.get(URL)
                                    data = response.json()
                                    if data['results']:
                                        lat = data['results'][0]['geometry']['location']['lat']
                                        lng = data['results'][0]['geometry']['location']['lng']
                                        list.append({'person':patientcount-i,'date_': d, 'content': ctext[1],'lat':lat,'lng':lng})
                                elif ctext:
                                    URL = 'https://maps.googleapis.com/maps/api/geocode/json?key=' + API_KEY + '&sensor=false&language=ko&address={}'.format(
                                        ctext)
                                    response = requests.get(URL)
                                    data = response.json()
                                    if data['results']:
                                        lat = data['results'][0]['geometry']['location']['lat']
                                        lng = data['results'][0]['geometry']['location']['lng']
                                        list.append({'person':patientcount-i,'date_': d, 'content': ctext[0],'lat':lat,'lng':lng})
                                else:
                                    pass
                            elif '보건소' in ctext and '타구' not in ctext:
                                helathcenter = ctext.find('보건소')
                                ctext = ctext[helathcenter - 4:helathcenter+3]
                                if ctext:
                                    URL = 'https://maps.googleapis.com/maps/api/geocode/json?key=' + API_KEY + '&sensor=false&language=ko&address={}'.format(
                                        ctext)
                                    response = requests.get(URL)
                                    data = response.json()
                                    if data['results']:
                                        lat = data['results'][0]['geometry']['location']['lat']
                                        lng = data['results'][0]['geometry']['location']['lng']
                                        list.append({'person':patientcount-i,'date_': d, 'content': ctext,'lat':lat,'lng':lng})
                            elif '의원' in ctext and  '○○의원' not in ctext:
                                clinic = ctext.find('의원')
                                ctext = ctext[clinic - 3:clinic+2]
                                if ctext:
                                    URL = 'https://maps.googleapis.com/maps/api/geocode/json?key=' + API_KEY + '&sensor=false&language=ko&address={}'.format(
                                        ctext)
                                    response = requests.get(URL)
                                    data = response.json()
                                    if data['results']:
                                        lat = data['results'][0]['geometry']['location']['lat']
                                        lng = data['results'][0]['geometry']['location']['lng']
                                        list.append({'person':patientcount-i,'date_': d, 'content': ctext,'lat':lat,'lng':lng})
                            else:
                                pass
    driver.close()
    print("driver close...")
    print("list done")
    with open('Patient.csv','w',encoding='utf8',newline='') as f:
        fieldnames=['person','date_','content','lat','lng']
        writer=csv.DictWriter(f,fieldnames=fieldnames)
        writer.writeheader()
        for item in list:
            writer.writerow(item)
    #jsonresult = js.dumps(bigList, indent=1, ensure_ascii=False)
    #print(jsonresult)
    print('csv done')
    conn = cx_Oracle.connect("ADMIN/KOSMO@192.168.0.51:1521/orcl")
    cursor = conn.cursor()
    #sql="delete from corona_patient "
    #cursor.execute(sql)
    for i in range(0, len(list)):
        sql="insert into CORONA_PATIENT(person,date_,content,lat,lng) values("+str(list[i]['person'])+",to_date('"+str(list[i]['date_'])+"','MM/DD'),'"+str(list[i]['content'])+"',"+str(list[i]['lat'])+","+str(list[i]['lng'])+")"
        print(sql)
        #cursor.execute(sql)
    cursor.close()
    conn.commit()
    conn.close()
    list=[]
    print('sql insert done')



#schedule.every(5).minutes.do(covidmap)


schedule.every(48).hours.do(covidmap)
# while 1:
#     schedule.run_pending()
#     time.sleep(10)
covidmap()


