import concurrent.futures
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import re
import json
import pandas as pd
from apikey import *
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition, ContentId)
options = Options()
options.headless = True
from collections import Counter
#url of the page we want to scrape
col1 = "Advanced_courses"
col2 = "Test_scores"
col3="Equity_overview"
col4 = "Race_ethnicity"
col5 = "Low-income_students"
col6 = "Students_with_Disabilities"
col7 = "Students"
col8 = "response_clearfix"
col9 = "academic_progress"
col10 = "courses_and_program"
col11 = "web_link"
col12 = "neighborhood"
col13 = "module_name"
col14 ="schl_name"
col15="College_readiness"
col16="College_success"
col17="Review"
col18="grade"
col19="tab_Race_ethnicity"
col20="tab_low_income"
col21="tab_student"
col22="num"
col23="temp"
d1=[]
d2=[]
d3=[]
d4=[]
d5=[]
d6=[]
d7=[]
d8=[]
d9=[]
d10=[]
d11=[]
d12=[]
d13=[]
d14=[]
d15=[]
d16=[]
d17=[]
d18=[]   
d19=[]
d20=[]
d21=[]
d22=[]     
cl=["p","e","m","h","public","charter","private"]
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

driver3 = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
li=[]
temp_sl=[]
count=0
try:
    for num in range(2,3):
            
            t_li=["Advanced_courses","Test_scores","Equity_overview","Race_ethnicity","Low-income_students","Students_with_Disabilities","Students","College_readiness","College_success"]

            ad_course=[]
            for page in range(120,130):
                print(page)
                url = "https://www.greatschools.org/texas/schools/?gradeLevels%5B%5D="+cl[num]+"&page="+str(page)+"&view=table"
                
                
                # initiating the webdriver. Parameter includes the path of the webdriver.
                driver3.get(url)
                # this is just to ensure that the page is loaded
                time.sleep(3)            

                html = driver3.page_source
                soup = BeautifulSoup(html, "html.parser")
                name = soup.find_all('a', {'class' : 'name'})
                names = list(name)[0:25]
                fs=1
                
                      
                for p in names:
                
                    ds={}
                    df2={}
                    
                    d18.append(cl[num])
                    x=p.get("href")
                    t_x=x.split("/")[3]
                    d22.append(t_x.replace("-"," "))
                    
                    d14.append(p.text.lower().replace("-"," "))
                    url="https://www.greatschools.org"+x
                    
                    driver3.get(url)
                    # this is just to ensure that the page is loaded
                    time.sleep(3)            
                    html = driver3.page_source
                    soup = BeautifulSoup(html, "html5lib")
                    d={"l_Advanced_courses":[],"l_Test_scores":[],"l_Equity_overview":[],"l_Race_ethnicity":[],"l_Low-income_students":[],"l_Students_with_Disabilities":[],"l_Students":[],"l_College_readiness":[],"l_College_success":[]}
                    
                    li_module=[]
                    student_demography_2=soup.find_all('div', {'class' : 'breakdown'})
                    web_link=soup.find_all('a',{'target':"_blank"})
                    percentage=soup.find_all('div', {'class' : 'percentage'})
                    response_clearfix=soup.find_all('div', {'class' : 'response clearfix'})
                    Courses_and_programs = soup.find('div', attrs = {'id':'Courses_and_programs'})
                    academic_progress=soup.find_all('div', {'id' : 'academic_progress'})
                    neighborhood_2=soup.find_all('div', {'class' : 'contact-row'})
                    main_module=soup.find_all('li', {'class' : 'toc-item'})
                    l_mm=soup.find_all('div', {'class' : 'module-container toc-module'})
                    review=soup.find_all('span', {'class' : 'filled-bar'},style=True)
                    academic_progress_2=soup.find_all('p',{'class':'side-bar'})   
            
                    l_mm=list(l_mm)
                    for i in l_mm:
                        t=i.get("id").strip()
                        if t in t_li:
                            li_module.append(i.get("id"))
                    web_link=list(web_link)
                    percentage=list(percentage)
                    student_demography_2=list(student_demography_2)
                    
                    response_clearfix=list(response_clearfix)
                    #Courses_and_programs=list(Courses_and_programs)
                    neighborhood_2=list(neighborhood_2)
                    main_module=list(main_module)
                    review=list(review)
                    Race_ethnicity = soup.find('div', attrs = {'id':'Race_ethnicity'})

                    academic_progress_2=list(academic_progress_2)
                    
                    res = 0
                    try:
                        Race_ethnicity_script = Race_ethnicity.find('script')
                        res = Race_ethnicity_script.contents[0]
                    except:
                        res = ''
                        pass
                    College_readiness = soup.find('div', attrs = {'id':'College_readiness'})
                    try:
                        College_readiness_script = College_readiness.find('script')
                        crs = College_readiness_script.contents[0]
                    except:
                        crs = ''
                        pass
                    
                    lis = 0
                    Low_income_students = soup.find('div', attrs = {'id':'Low-income_students'})
                    try:
                        Low_income_students_script = Low_income_students.find('script')
                        lis = Low_income_students_script.contents[0]
                    except:
                        lis = ''
                        pass
                    
                    swd = 0
                    Students_with_Disabilities = soup.find('div', attrs = {'id':'Students_with_Disabilities'})
                    try:
                        Students_with_Disabilities_script = Students_with_Disabilities.find('script')
                        swd = Students_with_Disabilities_script.contents[0]
                    except:
                        swd = ''
                        pass

                    school_name = soup.find('h1', attrs = {'class':'school-name'})
                    school_name = school_name.text
                    school_name = school_name.rstrip()
                    school_name = school_name.lstrip()
                    
                    #college readiness
                    df2 = {}
                    drt = []
                    
                    try:
                        dic2 = json.loads(College_readiness_script.contents[0])

                        for i in dic2['data']:
                            #drt[i['breakdown']] = [i['value'],i['state_value']]
                            drt.append(str(i['breakdown'])+":"+str(i['value']))
                        
                        
                    except :
                        pass
                    all_data = "["+res+","+lis+","+swd+"]"




                    d15.append(','.join(drt))
                   
                    
                    
                    # j = open("s1.json", "a")
                    # j.write(all_data)
                    # j.close()

                    ad  = []
                    try:
                        for h_sec in range(3):
                                
                                f = ''
                                dic = json.loads(all_data)
                                race_dic = dic[h_sec]                                       #selecting race tab
                                if "context" in race_dic:
                                
                                    continue
                                else:
                                    race_dic_data = race_dic['data']
                                    for mt in range(len(race_dic_data)):
                                            race_dic_data_0 = race_dic_data[mt]                      #selecting main tab
                                            tab  = race_dic_data_0['title'] # main tab
                                            race_dic_data_0_data = race_dic_data_0['data']
                                            
                                            no_sub_tab = False
                                            if not race_dic_data_0_data:
                                                    no_sub_tab = True
                                                    race_dic_data_0_data_coll = race_dic_data_0['values']
                                                    race_dic_data_0_data = [1]
                                            for st in range(len(race_dic_data_0_data)):
                                                    race_dic_data_0_data_0 = race_dic_data_0_data[st]        #selecting secondary tab
                                                    if no_sub_tab == False:
                                                            sub_tab = race_dic_data_0_data_0['anchor'] #sub tab    

                                                    try:    
                                                            if no_sub_tab == True:
                                                                    l1 = race_dic_data_0_data_coll

                                                            else:
                                                                    values = race_dic_data_0_data_0['values']
                                                                    test_scores = values['test_scores']
                                                                    l1 = test_scores['California Assessment of Student Performance and Progress (CAASPP)']
                                                    except:
                                                            l1 = race_dic_data_0_data_0['values']
                                                    if no_sub_tab == False:
                                                            f = "{};{};{};".format(race_dic['anchor'],tab,sub_tab)
                                                    else:
                                                            f = "{};{};".format(race_dic['anchor'],tab)

                                                    
                                                    for i in l1:
                                                            br = i['breakdown']     
                                                            label = i['label']     
                                                            if i['visualization'] == 'bar_graph':
                                                                    f = f + br + ":"+label+' % ,'
                                                            else:
                                                                    f = f + br + ":"+str(label)+' /10 ,'
                                                            try:
                                                                    if i['grades']:
                                                                            grades = i['grades']
                                                                            for grade in grades:
                                                                                    if i['visualization'] == 'bar_graph':
                                                                                            f = f + 'grade {} : {}% ,'.format(grade['grade'],grade['score']) 
                                                                                    else:
                                                                                            f = f + 'grade {} : {} /10 ,'.format(grade['grade'],grade['score'])
                                                                            continue
                                                            except:
                                                                    pass
                                                    ad.append(f[:-1])
                    except :
                        pass
                    
                    
                    
                    ds[school_name] = ad
                    Race_ethnicity=[]
                    r_t1=""
                    low_income=[]
                    l_t1=""
                    s_w_d=[]
                    swd_t1=""
                    
                    for i in ad:
                        if "Race_ethnicity" in i:
                            temp_s=i.split(";")
                            
                            if len(temp_s)==4:
                            
                                t_S=temp_s[1]
                                if t_S in r_t1:                           
                                    r_t1+=","+str(t_S)+":"+str(temp_s[2])
                                else:
                                    r_t1+=","+str(t_S)+":"+str(temp_s[2])
                                Race_ethnicity.append(temp_s[3])
                            elif len(temp_s)==3:
                                r_t1+=","+str(temp_s[1])+":"+"''"
                                Race_ethnicity.append(temp_s[2])
                            else:
                                Race_ethnicity.append(temp_s[len(temp_s)-1])
                        
                        elif "Low-income_students" in i:
                            temp_s=i.split(";")
                            
                            if len(temp_s)==4:
                                t_S=temp_s[1]
                                if t_S in l_t1:                           
                                    l_t1+=","+str(t_S)+":"+str(temp_s[2])
                                else:
                                    l_t1+=","+str(t_S)+":"+str(temp_s[2])
                                low_income.append(temp_s[3])
                            elif len(temp_s)==3:
                                l_t1+=","+str(temp_s[1])+":"+"''"
                                low_income.append(temp_s[2])
                            else:
                                low_income.append(temp_s[len(temp_s)-1])    
                        else:
                            temp_s=i.split(";")
                            if len(temp_s)==4:
                                t_S=temp_s[1]
                                if t_S in r_t1:                           
                                    swd_t1+=","+str(t_S)+":"+str(temp_s[2])
                                else:
                                    swd_t1+=","+str(t_S)+":"+str(temp_s[2])
                                s_w_d.append(temp_s[3])
                            elif len(temp_s)==3:
                                swd_t1+=","+str(temp_s[1])+":"+"''"
                                s_w_d.append(temp_s[2])
                            else:
                                s_w_d.append(temp_s[len(temp_s)-1])
                            
                    d4.append(';'.join(Race_ethnicity))
                    d5.append(';'.join(low_income))
                    d6.append(';'.join(s_w_d))
                    d19.append(r_t1[1:])
                    d20.append(l_t1[1:])
                    d21.append(swd_t1[1:])
                        
                    re=[]
                    
                    for i in review:
                        x=i["style"].split(":")
                        re.insert(0,x[1].strip())
                    d17.append(",".join(re))
                    j=0
                    k=0
                    #To get all the values and their percentage
                    for m in li_module:
                        
                        n=soup.find_all('div', {'id' : m})
                        n=list(n)
                        a_c=""
                        for i in n:
                            a_c+=str(i)
                        loop1=a_c.count('<div class="breakdown">')
                        loop2=a_c.count('<div class="percentage">')
                        
                        ad_temp=[]
                        if loop2==0:
                            k+=loop1
                        if loop1>loop2:
                            for y in range(loop2):
                                try:
                                    z=student_demography_2[k].text.split("\xa0")
                                    ad_temp.append(z[0]+":"+str(percentage[j].text.strip()))
                                except:
                                    pass
                                j+=1
                                k+=(loop1-loop2)+1
                        else:
                            for y in range(loop1):
                                try:
                                    z=student_demography_2[k].text.split("\xa0")
                                    ad_temp.append(z[0]+":"+str(percentage[j].text.strip()))
                                except:
                                    pass
                                j+=1
                                k+=(loop2-loop1)+1
                        d["l_"+m].append(','.join(ad_temp))
                    
                    x=list(d.values())
                    
                    d1.append(','.join(x[0]))
                    d2.append(','.join(x[1]))
                    d3.append(','.join(x[2]))        
                    d7.append(','.join(x[6]))
                    d16.append(','.join(x[8]))
                    
                    # To get the 'from the school' values
                    r_c=[]
                    for j in response_clearfix:
                        st=j.text
                        if "Start time" in st:
                            s=j.text.replace("Start time","Start time ")
                            r_c.append(s)
                        elif "Schedule" in st:
                            s=j.text.replace("Schedule","Schedule ")
                            r_c.append(s)
                        elif "End time" in st:
                            s=j.text.replace("End time","End time ")
                            r_c.append(s)
                        elif "Transportation" in st:
                            s=j.text.replace("Transportation","Transportation ")
                            r_c.append(s)
                        elif "Dress code" in st:
                            s=j.text.replace("Dress code","Dress code ")
                            r_c.append(s)
                        elif "Boarding school" in st:
                            s=j.text.replace("Boarding school","Boarding school ")
                            r_c.append(s)
                        elif "Coed" in st:
                            s=j.text.replace("Coed","Coed ")
                            r_c.append(s)
                        else:
                            r_c.append(st)
                    d8.append(','.join(r_c))
                    
                    #Academic Progress
                    t=[]
                    
                    for i,k in zip(academic_progress,academic_progress_2):  
                        a_c=(i.text).split("\n")
                        
                        for j in a_c:
                            if "/" in j:
                                j=j[0:j.find("/")]
                                
                                t.append(j.strip())
                                break
                                
                        t.append(i.find('p').text.replace("\n","").strip())
                        t.append(k.text)
                    d9.append(','.join(t))
                    
                    
                    #Courses and program
                    temp=[]
                    lll = [] 
                    dc={}
                    try:
                        Courses_and_programs_script = Courses_and_programs.findAll('script')
                        
                        lo = json.loads(Courses_and_programs_script[-1].contents[0])
                        if 'categories' in lo:
                        
                           
                            for fv in lo['categories']:
                                f = []
                                for jk in fv['items']:
                                    f.append(jk['display_text'])
                                dc[fv['display_text']] = f
                        else:
                           
                            cats= soup.findAll('div', attrs = {'class':'category'})
                            for cat in  cats:
                                Courses_and_programs_script = Courses_and_programs.findAll('script')
                                car_name = cat.contents[0]
                                for script in Courses_and_programs_script:
                                    lo = json.loads(script.contents[0])
                                    lll.append(lo['content'])
                                dc[car_name] = lll
                    
                    except:
                        pass    
              
                    d10.append(dc)  
                    #Weblink
                    for i in web_link:
                        d11.append(i.get("href"))
                        break
                        
                    #neighborhood
                    temp=""
                    for i in neighborhood_2:
                        temp+=i.text
                        temp+="\n"
                    d12.append(temp)
                    
                    #Main Module
                    l=[]    
                    for i in main_module:
                        x=(i.text).strip("\n")
                        if x not in l:
                            l.append(x)
                    d13.append(','.join(l))

                 
                
    driver3.close()  
      
    data = pd.DataFrame({col1:d1,col2:d2,col3:d3,col4:d4,col5:d5,col6:d6,col7:d7,col8:d8,col9:d9,col10:d10,col11:d11,col12:d12,col13:d13,col14:d14,col15:d15,col16:d16,col17:d17,col18:d18,col19:d19,col20:d20,col21:d21,col22:d22})
    data.to_excel(r'sample_data_main_texas_3_2'+'.xlsx', sheet_name='sheet1', index=False)
    
except:
    
    print(len(d1),len(d2),len(d3),len(d4),len(d5),len(d6),len(d7),len(d8),len(d9),len(d10),len(d11),len(d12),len(d13),len(d14),len(d15),len(d16),len(d17),len(d18),len(d19),len(d20),len(d21),len(d22))
    data = pd.DataFrame({col1:d1,col2:d2,col3:d3,col4:d4,col5:d5,col6:d6,col7:d7,col8:d8,col9:d9,col10:d10,col11:d11,col12:d12,col13:d13,col14:d14,col15:d15,col16:d16,col17:d17,col18:d18,col19:d19,col20:d20,col21:d21,col22:d22})
    data.to_excel(r'sample_data_main_texas_3_2'+'.xlsx', sheet_name='sheet1', index=False) 
    
