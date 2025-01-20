import pandas as pd
import csv
from datetime import datetime
from pathlib import Path
from colored import Fore,Style,Back
from barcode import Code39,UPCA,EAN8,EAN13
import barcode,qrcode,os,sys,argparse
from datetime import datetime,timedelta
import zipfile,tarfile
import base64,json
from ast import literal_eval
import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base as dbase
from sqlalchemy.ext.automap import automap_base
from pathlib import Path
import upcean
from radboy.ExtractPkg.ExtractPkg2 import *
from radboy.Lookup.Lookup import *
from radboy.DayLog.DayLogger import *
from radboy.DB.db import *
from radboy.DB.Prompt import *
from radboy.DB.SMLabelImporter import *
from radboy.DB.ResetTools import *

from radboy.ConvertCode.ConvertCode import *
from radboy.setCode.setCode import *
from radboy.Locator.Locator import *
from radboy.ListMode2.ListMode2 import *
from radboy.TasksMode.Tasks import *
from radboy.ExportList.ExportListCurrent import *
from radboy.TouchStampC.TouchStampC import *
from radboy import VERSION
import radboy.possibleCode as pc
from radboy.Unified.clearalll import *

class Unified:
    def unified(self,line):
        args=line.split(",")
        #print(args)
        if len(args) > 1:
            if args[0].lower() in ["remove","rm",'del','delete']:
                try:
                    with Session(self.engine) as session:
                        result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
                        if result:
                            print(result)
                            result.before_entry_delete()
                            session.delete(result)
                        session.commit()
                        session.flush()
                except Exception as e:
                    print(e)
                return True
            elif args[0].lower() in ['smle']:
                if len(args) >= 2:
                    if args[1].lower() in ['?','s','search','lu']:
                        while True:
                            def search(text,self):
                                code=text.lower()
                                with Session(self.engine) as session:
                                    result=session.query(Entry).filter(or_(Entry.Barcode==code,Entry.Code==code),Entry.InList==True).first()
                                    if result:
                                        result.listdisplay_extended(num=0)  
                                    else:
                                        print(f"{Style.bold+Style.underline+Fore.orange_red_1}No Such Item by {Style.underline}{code}{Style.reset}")
                            return Prompt(func=search,ptext="code|barcode|q/quit|b/back",helpText=self.help(print_no=True),data=self).state
                    else:
                        with Session(self.engine) as session:
                            result=session.query(Entry).filter(or_(Entry.Barcode==args[1],Entry.Code==args[1]),Entry.InList==True).first()
                            if result:
                                result.listdisplay_extended(num=0)
                            else:
                                print(f"{Style.bold+Style.underline+Fore.orange_red_1}No Such Item by {Style.underline}{args[1]}{Style.reset}")             
                return True
            elif args[0].lower() in ["search","s",'sch']:
                print("Search Mod")
                with Session(self.engine) as session:
                    #session.query(Entries).filter
                    for field in Entry.__table__.columns:
                        if field.name.lower() == args[1].lower():
                            print(field)
                            if str(field.type) in ['FLOAT','INTEGER']:
                                term=0
                                if str(field.type) == 'FLOAT':
                                    term=float(args[2])
                                elif str(field.type) == 'INTEGER':
                                    term=int(args[2])
                                operators=['==','!=','<','<=','>','>=','q','b']
                                print(f"""
{Fore.yellow}=={Style.reset} -> equal to
{Fore.yellow}=!{Style.reset} -> not equal to
{Fore.yellow}<{Style.reset} -> less than
{Fore.yellow}<={Style.reset} -> less than, or equal to
{Fore.yellow}>{Style.reset} -> greater than
{Fore.yellow}>={Style.reset} -> greater than, or equal to
{Style.bold+Style.underline+Fore.orange_red_1}q{Style.reset} -> quit
{Style.bold+Style.underline+Fore.orange_red_1}b{Style.reset} -> back
                                    """)
                                while True:
                                    operator=input(f"operator {operators}:").lower()
                                    if operator not in operators:
                                        continue
                                    if operator == 'q':
                                        exit('user quit')
                                    elif operator == 'b':
                                        break
                                    elif operator == '==':
                                        query=session.query(Entry).filter(field==term)
                                        save_results(query)
                                        results=query.all()
                                        for num,e in enumerate(results):
                                            print(f"{Style.bold+Style.underline+Fore.orange_red_1}{Style.bold}{Style.underline}{num}{Style.reset}->{e}")
                                        print(f"Number of Results: {len(results)}")
                                        break
                                    elif operator == '!=':
                                        query=session.query(Entry).filter(field!=term)
                                        save_results(query)
                                        results=query.all()
                                        for num,e in enumerate(results):
                                            print(f"{Style.bold+Style.underline+Fore.orange_red_1}{Style.bold}{Style.underline}{num}{Style.reset}->{e}")
                                        print(f"Number of Results: {len(results)}")
                                        break
                                    elif operator == '<':
                                        query=session.query(Entry).filter(field<term)
                                        save_results(query)
                                        results=query.all()
                                        for num,e in enumerate(results):
                                            print(f"{Style.bold+Style.underline+Fore.orange_red_1}{Style.bold}{Style.underline}{num}{Style.reset}->{e}")
                                        print(f"Number of Results: {len(results)}")
                                        break
                                    elif operator == '<=':
                                        query=session.query(Entry).filter(field<=term)
                                        save_results(query)
                                        results=query.all()
                                        for num,e in enumerate(results):
                                            print(f"{Style.bold+Style.underline+Fore.orange_red_1}{Style.bold}{Style.underline}{num}{Style.reset}->{e}")
                                        print(f"Number of Results: {len(results)}")
                                        break
                                    elif operator == '>':
                                        query=session.query(Entry).filter(field>term)
                                        save_results(query)
                                        results=query.all()
                                        for num,e in enumerate(results):
                                            print(f"{Style.bold+Style.underline+Fore.orange_red_1}{Style.bold}{Style.underline}{num}{Style.reset}->{e}")
                                        print(f"Number of Results: {len(results)}")
                                        break
                                    elif operator == '>=':
                                        query=session.query(Entry).filter(field>=term)
                                        save_results(query)
                                        results=query.all()
                                        for num,e in enumerate(results):
                                            print(f"{Style.bold+Style.underline+Fore.orange_red_1}{Style.bold}{Style.underline}{num}{Style.reset}->{e}")
                                        print(f"Number of Results: {len(results)}")
                                        break
                                break
                            elif str(field.type) == 'VARCHAR':
                                operators=['=','%','q','b','!%','!=']
                                print(f"""
 {Fore.yellow}={Style.reset} -> entry in Field is exactly
 {Fore.yellow}!={Style.reset} -> entry is not equal to
 {Fore.yellow}%{Style.reset} -> entry is contained within field but is NOT exact to the total of the field
 {Fore.yellow}!%{Style.reset} -> entry is not contained within field but is NOT exact to the total of the field
 {Style.bold+Style.underline+Fore.orange_red_1}q{Style.reset} -> quit
 {Style.bold+Style.underline+Fore.orange_red_1}b{Style.reset} -> back
                                    """)
                                while True:
                                    operator=input(f"operator {operators}:").lower()
                                    if operator not in operators:
                                        continue
                                    if operator == 'q':
                                        exit('user quit')
                                    elif operator == 'b':
                                        break
                                    elif operator == '=':
                                        query=session.query(Entry).filter(field==args[2])
                                        save_results(query)
                                        results=query.all()
                                        for num,e in enumerate(results):
                                            print(f"{Style.bold+Style.underline+Fore.orange_red_1}{Style.bold}{Style.underline}{num}{Style.reset}->{e}")
                                        print(f"Number of Results: {len(results)}")
                                        break
                                    elif operator == '!=':
                                        query=session.query(Entry).filter(field!=args[2])
                                        save_results(query)
                                        results=query.all()
                                        for num,e in enumerate(results):
                                            print(f"{Style.bold+Style.underline+Fore.orange_red_1}{Style.bold}{Style.underline}{num}{Style.reset}->{e}")
                                        print(f"Number of Results: {len(results)}")
                                        break
                                    elif operator == '%':
                                        query=session.query(Entry).filter(field.icontains(args[2]))
                                        save_results(query)
                                        results=query.all()
                                        for num,e in enumerate(results):
                                            print(f"{Style.bold+Style.underline+Fore.orange_red_1}{Style.bold}{Style.underline}{num}{Style.reset}->{e}")
                                        print(f"Number of Results: {len(results)}")
                                        break
                                    elif operator == '!%':
                                        query=session.query(Entry).filter(field.icontains(args[2])==False)
                                        save_results(query)
                                        results=query.all()
                                        for num,e in enumerate(results):
                                            print(f"{Style.bold+Style.underline+Fore.orange_red_1}{Style.bold}{Style.underline}{num}{Style.reset}->{e}")
                                        print(f"Number of Results: {len(results)}")
                                        break

                                break
                            else:
                                print(field.type)
                return True
            elif args[0].lower() in ['img','im','Image']:
                if len(args) == 2:

                    with Session(self.engine) as session:
                            result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
                            if result:
                                print(result.Image)
                            else:
                                print(f"{Fore.yellow}{Style.blink}{Style.bold}Nothing by that EntryId{Style.reset}")
                elif len(args) == 3:
                    with Session(self.engine) as session:
                        result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
                        try:
                            imtext=str(args[2])
                            f=importImage(image_dir=img_dir,src_path=imtext,nname=f'{result.EntryId}.png',ow=True)
                            setattr(result,'Image',f)
                            
                            session.commit()
                            session.flush()
                            session.refresh(result)
                            print(result.Image)
                        except Exception as e:
                            print("No Such EntryId!")
                return True
            elif args[0].lower() in ['rm_img','rm_im','del_img']:
                try:
                    with Session(self.engine) as session:
                        result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
                        try:
                            imtext=result.Image
                            removeImage(image_dir=img_dir,img_name=imtext)
                            setattr(result,'Image','')
                            
                            session.commit()
                            session.flush()
                            session.refresh(result)
                            print(result.Image)
                        except Exception as e:
                            print(e)
                            print("No Such EntryId!")
                except Exception as e:
                    print(e)
                return True
            elif args[0].lower() in ['upce2upca','u2u','e2a']:
                if len(args) == 2:
                    with Session(self.engine) as session:
                            result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
                            if result:
                                print(result.upce2upca)
                            else:
                                print(f"{Fore.yellow}{Style.blink}{Style.bold}Nothing by that EntryId{Style.reset}")
                elif len(args) == 3:
                    with Session(self.engine) as session:
                        result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
                        setattr(result,'upce2upca',args[2])
                        
                        session.commit()
                        session.flush()
                        session.refresh(result)
                        print(result.upce2upca)     
                return True
            elif args[0].lower() in ['+','-','=']:
                if len(args) == 3:
                    with Session(self.engine) as session:
                        result=session.query(Entry).filter(or_(Entry.Barcode==args[2],Entry.Code==args[2])).first()
                        if result:
                            if args[0] == '-':
                                result.ListQty=result.ListQty-float(args[1])
                            elif args[0] == '+':
                                result.ListQty=result.ListQty+float(args[1])
                            elif args[0] == '=':
                                result.ListQty=float(args[1])
                            result.InList=True
                            session.commit()
                            session.flush()
                            session.refresh(result)
                            print(result)       
                        else:
                            print(f"{Fore.yellow}{Style.blink}{Style.bold}Nothing by that EntryId{Style.reset}")
                else:
                    print(f"{Style.bold+Style.underline+Fore.orange_red_1}[+,-,=]{Style.reset},{Fore.yellow}QTY{Style.reset},{Fore.green}Code/Barcode{Style.reset}")
                return True
            elif args[0].lower() == "show":
                with Session(self.engine) as session:
                        result=session.query(Entry).filter(Entry.EntryId==int(args[1])).all()
                        for num,e in enumerate(result):
                            print(num,e)
                return True
        elif args[0].lower() in ["list_all","la"]:
            print("-"*10)
            with Session(self.engine) as session:
                    result=session.query(Entry).all()
                    for num,e in enumerate(result):
                        print(num,e)
            print("-"*10)
            return True
        elif args[0].lower() in ["show_list","sl",]:
            print("-"*10)
            with Session(self.engine) as session:
                    result=session.query(Entry).filter(Entry.InList==True).all()
                    for num,e in enumerate(result):
                        print(num,e)
            print("-"*10)
            return True
        elif args[0].lower() in ["clear_list","cl","clrl"]:
            print("-"*10)
            with Session(self.engine) as session:
                    result=session.query(Entry).filter(Entry.InList==True).update({'InList':False,'ListQty':0})
                    session.commit()
                    session.flush()
                    print(result)
            print("-"*10)
            return True
        elif args[0].lower() in ["clear_which","cw","clrw"]:
            print("-"*10)
            color_1=Fore.light_red
            color_2=Fore.light_magenta
            hstring=f'''
{Fore.orange_red_1}{Style.bold}Does not set InList==0{Style.reset}
Location Fields:
{Fore.deep_pink_3b}Shelf - {color_1}{Style.bold}0{Style.reset}
{Fore.light_steel_blue}BackRoom - {color_2}{Style.bold}1{Style.reset}
{Fore.cyan}Display_1 - {color_1}{Style.bold}2{Style.reset}
{Fore.cyan}Display_2 - {color_2}{Style.bold}3{Style.reset}
{Fore.cyan}Display_3 - {color_1}{Style.bold}4{Style.reset}
{Fore.cyan}Display_4 - {color_2}{Style.bold}5{Style.reset}
{Fore.cyan}Display_5 - {color_1}{Style.bold}6{Style.reset}
{Fore.cyan}Display_6 - {color_2}{Style.bold}7{Style.reset}
{Fore.cyan}SBX_WTR_DSPLY - {color_1}{Style.bold}8{Style.reset}
{Fore.cyan}SBX_CHP_DSPLY - {color_2}{Style.bold}9{Style.reset}
{Fore.cyan}SBX_WTR_KLR - {color_1}{Style.bold}10{Style.reset}
{Fore.violet}FLRL_CHP_DSPLY - {color_2}{Style.bold}11{Style.reset}
{Fore.violet}FLRL_WTR_DSPLY - {color_1}{Style.bold}12{Style.reset}
{Fore.grey_50}WD_DSPLY - {color_2}{Style.bold}13{Style.reset}
{Fore.grey_50}CHKSTND_SPLY - {color_1}{Style.bold}14{Style.reset}
{Fore.grey_50}InList - {color_2}{Style.bold}15{Style.reset}'''

            def mkfields(text,data):
                def print_selection(selected):
                    print(f"{Fore.light_yellow}Using selected {Style.bold}{Fore.light_green}'{selected}'{Style.reset}!")
                try:
                    selected=None
                    #use upper or lower case letters/words/fieldnames
                    fields=tuple([i.name for i in Entry.__table__.columns])
                    fields_lower=tuple([i.lower() for i in fields])
                    if text.lower() in fields_lower:
                        index=fields_lower.index(text.lower())
                        selected=fields[index]
                        print_selection(selected)
                        return fields[index]
                    else:
                        #use numbers
                        mapped={
                            '0':"Shelf",
                            '1':"BackRoom",
                            '2':"Display_1",
                            '3':"Display_2",
                            '4':"Display_3",
                            '5':"Display_4",
                            '6':"Display_5",
                            '7':"Display_6",
                            '8':"SBX_WTR_DSPLY",
                            '9':"SBX_CHP_DSPLY",
                            '10':"SBX_WTR_KLR",
                            '11':"FLRL_CHP_DSPLY",
                            '12':"FLRL_WTR_DSPLY",
                            '13':"WD_DSPLY",
                            '14':"CHKSTND_SPLY",
                            '15':"ListQty"
                        }
                        #print(text,mapped,text in mapped,mapped[text])
                        if text in mapped:
                            selected=mapped[text]
                            print_selection(selected)
                            return mapped[text]
                except Exception as e:
                    print(e)
            #for use with header
            z='TaskMode'
            mode='Clear Which Field'
            header_here=f'{Prompt.header.format(Fore=Fore,mode=mode,fieldname=z,Style=Style)}'
            while True:
                fieldname=Prompt.__init2__(None,func=mkfields,ptext=f"{header_here}Location Field(see h|help)",helpText=hstring,data=self)
                if fieldname in [None,]:
                    break
                break
            if fieldname in [None,]:
                return True
            with Session(self.engine) as session:
                    result=session.query(Entry).filter(Entry.InList==True).update({fieldname:0})
                    session.commit()
                    session.flush()
                    print(result)
            print("-"*10)
            return True
        elif args[0].lower() in ['code_len']:
                while True:
                    def display_lcl(text,self):
                        print(f"{Fore.cyan}{text}{Style.reset} is {Fore.green}'{len(text)}'{Style.reset} characters long!")
                    return Prompt(func=display_lcl,ptext="code|barcode[q/b]",helpText=self.help(print_no=True),data=self).state
                return True
        elif args[0].lower() in ["clear_all","ca","clrall"]:
            '''
            def mkBool(text,self):
                try:
                    if text.lower() in ['','y','yes','ye','true','1']:
                        return True
                    elif text.lower() in ['n','no','false','0']:
                        return False
                    else:
                        return eval(text)
                except Exception as e:
                    print(e)
            fieldname='TaskMode'
            mode='ClearAll'
            h=f'{Prompt.header.format(Fore=Fore,mode=mode,fieldname=fieldname,Style=Style)}'
            htext=f"""{Fore.light_red}Type one of the following between commas:
{Fore.light_yellow}y/yes/ye/true/1 {Fore.green} to continue, this is the default so <Enter>/<return> will also result in this!!!
{Fore.light_green}n/no/false/0 {Fore.green} to cancel delete{Style.reset}"""
            really=True
            while True:
                try:
                    really=Prompt.__init2__(None,func=mkBool,ptext=f"{h}Really Clear All Lists, and set InList=0?",helpText=htext,data=self)
                    break
                except Exception as e:
                    print(e)
            if really in [False,None]:
                print(f"{Fore.light_steel_blue}Nothing was {Fore.orange_red_1}{Style.bold}Deleted!{Style.reset}")
                return True
            else:
                print(f"{Fore.orange_red_1}Deleting {Fore.light_steel_blue}{Style.bold}All Location Field Values,{Fore.light_blue}{Style.underline} and Setting InList=0!{Style.reset}")

            
            print("-"*10)
            with Session(self.engine) as session:
                    result=session.query(Entry).update(
                        {'InList':False,
                        'ListQty':0,
                        'Shelf':0,
                        'Note':'',
                        'BackRoom':0
                        ,'Display_1':0,
                        'Display_2':0,
                        'Display_3':0,
                        'Display_4':0,
                        'Display_5':0,
                        'Display_6':0,
                        'Stock_Total':0,
                        'CaseID_BR':'',
                        'CaseID_LD':'',
                        'CaseID_6W':'',
                        'SBX_WTR_DSPLY':0,
                        'SBX_CHP_DSPLY':0,
                        'SBX_WTR_KLR':0,
                        'FLRL_CHP_DSPLY':0,
                        'FLRL_WTR_DSPLY':0,
                        'WD_DSPLY':0,
                        'CHKSTND_SPLY':0,
                        })
                    session.commit()
                    session.flush()
                    print(result)
            print("-"*10)
            return True
            '''
            self.clear_all=clear_all
            self.clear_all(self)
        elif args[0].lower() in ["total_entries","te","count_all",'cta']:
            print("-"*10)
            with Session(self.engine) as session:
                    result=session.query(Entry).all()
                    ct=len(result)
                    bcode=Fore.light_yellow
                    ccode=Fore.dark_goldenrod
                    ncode=Fore.light_red
                    cur=Fore.cyan
                    total=Fore.medium_violet_red
                    line=f"{cur}Current/{total}Total -> {bcode}Barcode | {ccode}Code | {ncode}Name{Style.reset}"
                    for num,item in enumerate(result):
                        line=f"{cur}{num}/{total}{ct} -> {bcode}{item.Barcode} | {ccode}{item.Code} | {ncode}{item.Name}{Style.reset}"
                        print(line)
        elif args[0].lower() in ["qsl","quick_show_list",]:
            print("-"*10)
            with Session(self.engine) as session:
                    result=session.query(Entry).filter(Entry.InList==True).all()
                    ct=len(result)
                    bcode=Fore.light_yellow
                    ccode=Fore.dark_goldenrod
                    ncode=Fore.light_red
                    cur=Fore.cyan
                    total=Fore.medium_violet_red
                    line=f"{cur}Current/{total}Total -> {bcode}Barcode | {ccode}Code | {ncode}Name{Style.reset}"
                    for num,item in enumerate(result):
                        line=f"{cur}{num}/{total}{ct} -> {bcode}{item.Barcode} | {ccode}{item.Code} | {ncode}{item.Name}{Style.reset}"
                        print(line)
        elif args[0].lower() in ["clear_all_img","cam","clrallimg"]:
            print("-"*10)
            with Session(self.engine) as session:
                    result=session.query(Entry).all()
                    for num,item in enumerate(result):
                        print(f"{Style.bold+Style.underline+Fore.orange_red_1}{num} - clearing img field -> {item}")
                        if Path(item.Image).exists():
                            try:
                                if Path(item.Image).is_file():
                                    Path(item.Image).unlink()
                                    item.ImagePath=''
                                    session.commit()
                                    #session.flush()
                                    #session.refresh(item)
                            except Exception as e:
                                item.Image=''
                                session.commit()
                                #session.flush()
                                #session.refresh(item)
                        else:
                            item.Image=''
                            session.commit()
                            #session.flush()
                            #session.refresh(item)
                    session.commit()
                    session.flush()
                    print(result)
            print("-"*10)
            return True
        elif args[0].lower() in ["save_csv","save","sv"]:
            def save_csv(sfile,self):
                if sfile == "":
                    sfile="./db.csv"
                    print(f'{Fore.orange_3}{Path(sfile).absolute()}{Style.reset}')
                try:
                    print("Exporting")          
                    
                    with Session(self.engine) as session,Path(sfile).open("w") as CSV:
                        writer=csv.writer(CSV,delimiter=',')
                        allResults=session.query(Entry).all()
                        headers=[]
                        ct=len(allResults)

                        for num,r in enumerate(allResults):
                            if headers==[]:
                                headers=r.csv_headers()
                            print(f"{Fore.light_green}{num}{Style.reset}/{Fore.light_yellow}{ct-1}{Style.reset}")
                            if num == 0:
                                writer.writerow(headers)
                            elif num > 0:
                                writer.writerow(r.csv_values())
                            #if r.csv_headers() != headers and num > 1:
                            #   exit(f'{headers}|{r.csv_headers()}')

                        print(f"{Fore.light_red}Done!{Style.reset} - {Fore.green_yellow}{Path(sfile).absolute()}{Style.reset}")
                    
                except Exception as e:
                    print(e)
            return Prompt(func=save_csv,ptext="Save Where",helpText=self.help(print_no=True),data=self).state
        elif args[0].lower() in ["save_bar","sb","svbr"]:
            def save_csv(sfile,self):
                df=pd.read_sql_table('Entry',self.engine)
                if sfile == "":
                    sfile="./db.csv"
                    print(f'{Fore.orange_3}{Path(sfile).absolute()}{Style.reset}')
                df=df['Barcode']
                df.to_csv(sfile,index=False)
            return Prompt(func=save_csv,ptext="Save Where",helpText=self.help(print_no=True),data=self).state
        elif args[0].lower() in ["save_bar_cd","sbc","svbrcd"]:
            def save_csv(sfile,self):
                df=pd.read_sql_table('Entry',self.engine)
                if sfile == "":
                    sfile="./db.csv"
                    print(f'{Fore.orange_3}{Path(sfile).absolute()}{Style.reset}')
                df=df[['Barcode','Code']]
                df.to_csv(sfile,index=False)
            return Prompt(func=save_csv,ptext="Save Where",helpText=self.help(print_no=True),data=self).state
        elif args[0].lower() in ["factory_reset"]:
            #just delete db file and re-generate much simpler
            ResetTools(engine=self.engine,parent=self)
            #reInit()
            '''with Session(self.engine) as session:
                done=session.query(Entry).delete()
                session.commit()
                session.flush()
                print(done)'''
            return True
        elif args[0].lower() in ["fields","f","flds"]:
            print("fields in table!")
            for column in Entry.__table__.columns:
                print(column.name)
            return True
        elif args[0].lower() in ['tlm']:
            self.listMode=not self.listMode
            print(f"ListMode is now: {Style.bold+Style.underline+Fore.orange_red_1}{self.listMode}{Style.reset}")
            return True
        elif args[0].lower() in ['slm']:
            print(f"ListMode is: {Style.bold+Style.underline+Fore.orange_red_1}{self.listMode}{Style.reset}")
            return True
        elif args[0].lower() in ['sum_list','smzl']:
            with Session(self.engine) as session:
                results=session.query(Entry).filter(Entry.InList==True).all()
                for num,result in enumerate(results):
                    result.listdisplay(num=num)
            
            return True
        elif args[0].lower() in ['?','help']:
            self.help()
            return True
        elif args[0].lower() in ['smle']:
                    with Session(self.engine) as session:
                        results=session.query(Entry).filter(Entry.InList==True).all()
                        if len(results) < 1:
                            print(f"{Fore.dark_goldenrod}No Items in List!{Style.reset}")
                        for num,result in enumerate(results):
                            result.listdisplay_extended(num=num)
        elif args[0].lower() in ['smle-e']:
                    with Session(self.engine) as session:
                        results=session.query(Entry).filter(Entry.InList==True).all()
                        if len(results) < 1:
                            print(f"{Fore.dark_goldenrod}No Items in List!{Style.reset}")
                        for num,result in enumerate(results):
                            result.saveListExtended(num=num)
        elif args[0].lower() in ['le-img']:
                    with Session(self.engine) as session:
                        results=session.query(Entry).filter(Entry.InList==True).all()
                        if len(results) < 1:
                            print(f"{Fore.dark_goldenrod}No Items in List!{Style.reset}")
                        for num,result in enumerate(results):
                            result.saveItemData(num=num)
        elif args[0].lower() in 'export_list_field|elf'.split("|"):
            with Session(self.engine) as session:
                        results=session.query(Entry).filter(Entry.InList==True).all()
                        if len(results) < 1:
                            print(f"{Fore.dark_goldenrod}No Items in List!{Style.reset}")
                        def mkT(text,self):
                            return text
                        fieldName=Prompt.__init2__(self,func=mkT,ptext="FieldName",helpText="Export FieldData to Encoded Img "+','.join([i.name for i in Entry.__table__.columns]),data=self)
                        if fieldName in [i.name for i in Entry.__table__.columns]:
                            for num,result in enumerate(results):
                                result.save_field(fieldname=fieldName)
                        else:
                            print(f"{Fore.light_red}Invalid fieldname!{Style.reset}")
        elif args[0].lower() in ['le-img-bc']:
                    with Session(self.engine) as session:
                        results=session.query(Entry).filter(Entry.InList==True).all()
                        if len(results) < 1:
                            print(f"{Fore.dark_goldenrod}No Items in List!{Style.reset}")
                        for num,result in enumerate(results):
                            print(num)
                            result.save_barcode()
        elif args[0].lower() in ['le-img-c']:
                    with Session(self.engine) as session:
                        results=session.query(Entry).filter(Entry.InList==True).all()
                        if len(results) < 1:
                            print(f"{Fore.dark_goldenrod}No Items in List!{Style.reset}")
                        for num,result in enumerate(results):
                            print(num)
                            result.save_code()
        elif args[0].lower() in ['clear','reset','screen_reset','#<>?']:
                    print(os.system("clear "))
                    return True
        elif args[0].lower() in ['backup',]:
                    startTime=datetime.now()
                    print(f"{Fore.orange_red_1}Backing {Fore.light_yellow}Files {Fore.light_green}up!{Style.reset}")
                    backup=''
                    while True:
                        try:
                            def mkBool(text,data):
                                try:
                                    if text.lower() in ['','true','y','yes','1']:
                                        return True
                                    elif text.lower() in ['n','false','no','0']:
                                        return False
                                    else:
                                        return bool(eval(text))
                                except Exception as e:
                                    print(e)
                                    return False
                            date_file=Prompt.__init2__(None,func=mkBool,ptext="Date and Time restore File?",helpText="y/n?",data=self)
                            if date_file in [None,]:
                                return True
                            elif isinstance(date_file,bool):
                                if date_file:
                                    d=datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
                                    backup=Path(f"./codesAndBarcodes-{d}.tgz")
                                else:
                                    backup=Path(f"./codesAndBarcodes.tgz")
                            else:
                                backup=Path(f"./codesAndBarcodes-{d}.tgz")
                            break
                        except Exception as e:
                            print(e)
                            return True
                    if backup.exists():
                        backup.unlink()
                    
                    with tarfile.open(backup,"w:gz") as gzf:
                        #gzf.add("codesAndBarcodes.db")
                        #gzf.add("Images")
                        #gzf.add("LCL_IMG")
                        with open("Run.py","wb") as runner:
                            oldlines=b'''
#!/usr/bin/env python3
import radboy.RecordMyCodes as rmc
rmc.quikRn()
'''
                            lines=b'''
#!/usr/bin/env python3
from radboy import RecordMyCodes as rmc
rmc.quikRn()
'''
                            runner.write(lines)
                        '''
                        try:
                            print("adding module...")
                            m=Path("module")
                            if m.exists():
                                shutil.rmtree(m)
                                m.mkdir()
                            else:
                                m.mkdir()
                            os.system(f"pip download MobileInventoryCLI=={VERSION} -d {m}")
                            gzf.add(m)
                            print("added module code!")
                        except Exception as e:
                            print("could not finish adding modules/")
                        '''
                        #shutil.rmtree(m)
                        print(f"{Fore.spring_green_3b}Adding {Fore.green_yellow}{Path('Run.py')}{Style.reset}")
                        gzf.add("Run.py")
                        
                        while True:
                            try:
                                def mkBool(text,self):
                                    if text.lower() in ['','n','no','-']:
                                        return False
                                    elif text.lower() in ['y','yes','+']:
                                        return True
                                    else:
                                        try:
                                            return bool(eval(text))
                                        except Exception as e:
                                            print(e)
                                            return False
                                rmRunner=Prompt.__init2__(None,func=mkBool,ptext="Delete 'Run.py'",helpText="default == 'No'",data=self)
                                if rmRunner:
                                    Path("Run.py").unlink()
                                break
                            except Exception as e:
                                print(e)

                        with open("version.txt","w+") as version_txt:
                            version_txt.write(VERSION)

                        if Path("version.txt").exists():
                            print(f'{Fore.spring_green_3b}Adding {Fore.green_yellow}{Path("version.txt")}{Style.reset}')
                            gzf.add("version.txt")
                            Path("version.txt").unlink()

                        api_key_file=Path("./api_key")
                        if api_key_file.exists():
                            print(f"{Fore.spring_green_3b}Adding {Fore.green_yellow}{api_key_file}{Style.reset}")
                            gzf.add(api_key_file)

                        msg=f'''
{Fore.orange_red_1}Getting system settings files, testing for existance, if not found leaving alone!!!{Style.reset}
                        '''
                        print(msg)
                        #from ExportUtility/ExportTableClass.py
                        import_odf=detectGetOrSet("ImportODF",value="ImportExcel.xlsx.ods",literal=True)
                        if import_odf:
                            import_odf=Path(import_odf)
                            if import_odf.exists():
                                print(f"{Fore.spring_green_3b}Adding {Fore.green_yellow}{import_odf}{Style.reset}")
                                gzf.add(import_odf)
                        
                        import_excel=detectGetOrSet("ImportExcel",value="ImportExcel.xlsx",literal=True)
                        if import_excel:
                            import_excel=Path(import_excel)
                            if import_excel.exists():
                                print(f"{Fore.spring_green_3b}Adding {Fore.green_yellow}{import_excel}{Style.reset}")
                                gzf.add(import_excel)

                        export_folder=Path(detectGetOrSet("ExportTablesFolder",value="ExportedTables",literal=True))
                        if export_folder:
                            export_folder=Path(export_folder)
                            if export_folder.exists() and export_folder.is_dir():
                                print(f"{Fore.spring_green_3b}Adding {Fore.green_yellow}{export_folder}{Style.reset}")
                                gzf.add(export_folder)
                        #from DB/Prompt.py
                        scanout=detectGetOrSet('CMD_TO_FILE',str(Path('./SCANNER.TXT')))
                        if scanout:
                            scanout=Path(scanout)
                            if scanout.exists():
                                print(f"{Fore.spring_green_3b}Adding {Fore.green_yellow}{scanout}{Style.reset}")
                                gzf.add(scanout)

                        #from TouchStampC/TouchStampC.py
                        ts_outfile=detectGetOrSet("TouchStampSearchExport",value="TS_NOTE.txt",literal=True)
                        if ts_outfile:
                            ts_outfile=Path(ts_outfile)
                            if ts_outfile.exists():
                                print(f"{Fore.spring_green_3b}Adding {Fore.green_yellow}{ts_outfile}{Style.reset}")
                                gzf.add(ts_outfile)

                        #from Roster/Roster.py
                        src_t="Downloads/Roster.xlsx"
                        lcl_e_src=detectGetOrSet("localEXCEL",src_t,literal=True,setValue=False)
                        if lcl_e_src:
                            lcl_e_src=Path(lcl_e_src)
                            if lcl_e_src.exists():
                                print(f"{Fore.spring_green_3b}Adding {Fore.green_yellow}{lcl_e_src}{Style.reset}")
                                gzf.add(lcl_e_src)
                        #from TasksMode/Tasks.py
                        bcd_final_out=detectGetOrSet("IMG_GEN_OUT_QR","GENERATED_QR.png",literal=True)
                        if bcd_final_out:
                            bcd_final_out=Path(bcd_final_out)
                            if bcd_final_out.exists():
                                print(f"{Fore.spring_green_3b}Adding {Fore.green_yellow}{bcd_final_out}{Style.reset}")
                                gzf.add(bcd_final_out)

                        qr_final_out=detectGetOrSet("IMG_GEN_OUT","GENERATED_BCD",literal=True)
                        if qr_final_out:
                            qr_final_out=Path(qr_final_out+".png")
                            if qr_final_out.exists():
                                print(f"{Fore.spring_green_3b}Adding {Fore.green_yellow}{qr_final_out}{Style.reset}")
                                gzf.add(qr_final_out)


                        EMSGFILE=detectGetOrSet("OBFUSCATED MSG FILE","MSG.txt",literal=True)
                        if EMSGFILE:
                            EMSGFILE=Path(EMSGFILE)
                            if EMSGFILE.exists():
                               print(f"{Fore.spring_green_3b}Adding {Fore.green_yellow}{EMSGFILE}{Style.reset}") 
                               gzf.add(EMSGFILE)
                               
                        dbf=Path("codesAndBarcodes.db")
                        if dbf.exists():
                            print(f"{Fore.spring_green_3b}Adding {Fore.green_yellow}{dbf}{Style.reset}")
                            gzf.add(dbf)
                            
                        with Session(ENGINE) as session:
                            files=session.query(SystemPreference).filter(SystemPreference.name.icontains('ClipBoordImport_')).all()
                            for num,i in enumerate(files):
                                #print(num,json.loads(i.value_4_Json2DictString)[i.name],"Being Added from SystemPreference!")
                                try:
                                    print(f"{Fore.spring_green_3b}Adding {Fore.green_yellow}{json.loads(i.value_4_Json2DictString)[i.name]}{Style.reset}")
                                    gzf.add(json.loads(i.value_4_Json2DictString)[i.name])
                                except Exception as e:
                                    print(e,"couldn't not add!")

                        imd=Path("Images")
                        if imd.exists():
                            print(f"{Fore.spring_green_3b}Adding {Fore.green_yellow}{imd}{Style.reset}")
                            gzf.add(imd)
                        lclimg=Path("LCL_IMG")
                        if lclimg.exists():
                            print(f"{Fore.spring_green_3b}Adding {Fore.green_yellow}{lclimg}{Style.reset}")
                            gzf.add(lclimg)
                        
                    print(backup.absolute())
                    endTime=datetime.now()
                    msg=f'''{Fore.light_red}{backup}{Fore.light_steel_blue} Took {Fore.green_yellow}{endTime-startTime}{Fore.light_steel_blue} to backup.'''
                    print(msg)
                    return True

        elif args[0].lower() in ['restore',]:
            def lcl_bu(backup,self):
                backup=Path(backup)
                if backup.exists():
                    print("clearing old data...")
                    dbf=Path("codesAndBarcodes.db")
                    if dbf.exists():
                        dbf.unlink()
                    imd=Path("Images")
                    if imd.exists():
                        shutil.rmtree(str(imd))
                    lclimg=Path("LCL_IMG")
                    if lclimg.exists():
                        shutil.rmtree(str(lclimg
                            ))
                    
                    with tarfile.open(backup,"r:gz") as gzf:
                        gzf.extractall()
            s=Prompt(func=lcl_bu,ptext="backup file: ",helpText=self.help(print_no=True),data=self).state
            exit(f"{Style.bold}{Fore.light_red}The application {Fore.orange_red_1}needs to restart{Fore.light_yellow}...{Fore.light_green}.!!!{Style.reset}")
        elif args[0].lower() in ['set_all_inlist_1','sai1']:
            with Session(self.engine) as session:
                result=session.query(Entry).all()
                ct=len(result)
                for num,r in enumerate(result):
                    print(f"{Fore.green}{num+1}{Style.reset}/{Style.bold+Style.underline+Fore.orange_red_1}{ct}{Style.reset}")
                    r.InList=True
                    if num % 100 == 0:
                        session.commit()
                session.commit()
                session.flush()
            return True
        elif args[0].lower() in ['set_all_userUpdated_1','sau1']:
            with Session(self.engine) as session:
                result=session.query(Entry).all()
                ct=len(result)
                for num,r in enumerate(result):
                    print(f"{Fore.green}{num+1}{Style.reset}/{Style.bold+Style.underline+Fore.orange_red_1}{ct}{Style.reset}")
                    r.userUpdated=True
                    if num % 100 == 0:
                        session.commit()
                session.commit()
                session.flush()
            return True
        elif args[0].lower() in ['list_all_userUpdated_1','lau1']:
            with Session(self.engine) as session:
                result=session.query(Entry).filter(Entry.userUpdated==True).all()
                ct=len(result)
                for num,r in enumerate(result):
                    print(f"{Fore.green}{num}{Style.reset}/{Style.bold+Style.underline+Fore.orange_red_1}{ct}{Style.reset} -> {r}") 
            return True
        elif args[0].lower() in ['list_all_userUpdated_0','lau0']:
            with Session(self.engine) as session:
                result=session.query(Entry).filter(Entry.userUpdated==False).all()
                ct=len(result)
                for num,r in enumerate(result):
                    print(f"{Fore.green}{num}{Style.reset}/{Style.bold+Style.underline+Fore.orange_red_1}{ct}{Style.reset} -> {r}") 
            return True
        elif args[0].lower() in ['ts','touchstamp']:
            self.ts=TouchStampC(engine=self.engine,parent=self)
        elif args[0].lower() in ['import_csv','import csv']:
            def import_csv_lcl(codefile,self):
                try:
                    codefile_path=Path(codefile)
                    if codefile_path.exists() and codefile_path.is_file():  
                        with Session(self.engine) as session:
                            df=pd.read_csv(codefile_path,dtype=str)
                            headers=df.keys()
                            if 'Barcode' not in headers:
                                print("missing barcode header")
                                return True
                            if 'Code' not in headers:
                                print("missing Code header")
                                return True
                            if 'Name' not in headers:
                                print("missing Name header")
                                return True
                            a=df
                            dt=[dict(zip(a.keys(),i.tolist())) for i in a.to_numpy()]
                            for num,r in enumerate(dt):
                                check=session.query(Entry).filter(Entry.Barcode==r['Barcode']).first()
                                if check:
                                    print(f"{Fore.light_red}Exists Already! -> {check}")
                                    continue
                                ne=Entry(**r)
                                ne.InList=True
                                session.add(ne)
                                session.commit()
                                session.refresh(ne)
                                ne.Image=ne.cp_src_img_to_entry_img(ne.Image)
                                session.commit()
                                session.refresh(ne)
                                print(f"{ne}\n{num+1}/{len(dt)} - {r}")

                        session.commit()
                except Exception as e:
                    print(e)
                print(f"Remember CSV must have {Style.underline}'Barcode,Code,Name'{Style.reset} headers as first line")
            return Prompt(func=import_csv_lcl,ptext="File Path",helpText=self.help(print_no=True),data=self).state
        elif args[0].lower() in ['import_smartlabel_html','ish']:
            ScrapeLocalSmartLabelList(engine=self.engine)
            return True
        elif args[0].lower() in ['set_all_inlist_0','sai0']:
            with Session(self.engine) as session:
                result=session.query(Entry).all()
                ct=len(result)
                for num,r in enumerate(result):
                    print(f"{Fore.green}{num+1}{Style.reset}/{Style.bold+Style.underline+Fore.orange_red_1}{ct}{Style.reset}")
                    r.InList=False
                    r.ListQty=0
                    if num % 100 == 0:
                        session.commit()
                session.commit()
                session.flush()
            return True
        elif args[0].lower() in ['set_all_userUpdated_0','sau0']:
            with Session(self.engine) as session:
                result=session.query(Entry).all()
                ct=len(result)
                for num,r in enumerate(result):
                    print(f"{Fore.green}{num+1}{Style.reset}/{Style.bold+Style.underline+Fore.orange_red_1}{ct}{Style.reset}")
                    r.userUpdated=False
                    if num % 100 == 0:
                        session.commit()
                session.commit()
                session.flush()
            return True
        elif args[0].lower() in ['export_list','el']:
            ExportListCSV(parent=self,engine=self.engine)
        elif args[0].lower() in ['ie','item_editor','itm_edt']:
            editor=EntrySet(engine=self.engine,parent=self)
        elif args[0].lower() in ['ni','new_item']:
            while True:
                try:
                    data={}
                    for column in Entry.__table__.columns:
                        value=None
                        #print(column.type,type(column.type))
                        if str(column.type) in ['FLOAT','INTEGER']:
                            if str(column.type) == 'FLOAT':
                                #value=input("f{column.name}({column.type})[q/b/value/enter to skip]: ")
                                def mkFloat(text,self):
                                    if text == '':
                                        return float(0)
                                    else:
                                        return float(text)
                                pt=f"{column.name}({column.type})[q/b/value/enter to skip]"
                                value=Prompt.__init2__(None,func=mkFloat,ptext=pt,helpText=self.help(print_no=True))
                                #value=float(value)
                            elif str(column.type) == 'INTEGER':
                                def mkFloat(text,self):
                                    if text == '':
                                        return int(0)
                                    else:
                                        return int(text)
                                pt=f"{column.name}({column.type})[q/b/value/enter to skip]"
                                value=Prompt.__init2__(None,func=mkFloat,ptext=pt,helpText=self.help(print_no=True))
                        else:
                            def mkT(text,column):
                                if text == '' and column in ['Code','Barcode']:
                                    return Entry.synthetic_field_str(None)
                                else:
                                    return str(text)

                            pt=f"{column.name}({column.type})[q/b/value/enter to skip]"
                            value=Prompt.__init2__(None,func=mkT,ptext=pt,helpText=self.help(print_no=True),data=column.name)
                        data[column.name]=value
                        data['InList']=True
                    newEntry=Entry(**data)
                    with Session(self.engine) as session:
                        session.add(newEntry)
                        session.commit()
                        session.flush()
                        session.refresh(newEntry)
                        print(newEntry)
                    break
                except Exception as e:
                    print(e)
        return False