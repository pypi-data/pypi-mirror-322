#MobileInventoryCLI is now radboy
from . import *

def get_bool(text):
    if text in (None,'',False,'n','N','NO','No','nO','False','false',0,'0'):
        return False
    elif text in (True,'y','yes',1,'1','True','true','YES','Yes','Y'):
        return True
    else:
        try:
            return eval(text)
        except Exception as e:
            print(e)
            return False
DateTimeFormats=(
'%m/%d/%Y@%H:%M:%S',
'%H:%M:%S on %m/%d/%Y',
'%m/%d/%Y@%H:%M',
'%H:%M on %m/%d/%Y',
)
'''
 bytes are stored as base64 string
 under neu
  af2e add field to Entry
  sf2e select a field name from searched/listed and add field to entry
   these searched/listed fieldnames would be collected from already created fields
   results=search by name or use '*' to show all
   name=select index from results and get name of object
   apply name to new extra
   apply type from result
   get value
   apply entry id
   commit result
 under esu
  when a product is searched the Extras Table for corresponding
  EntryId and display that info as well before printing next Entry
'''       
TYPES_FromText={
"string":{
'cmds':['str','text',],
"exec":str,
"desc":'anything that is meant to be text'
},
"integer":{
'cmds':['integer','int'],
'exec':int,
'desc':"numbers without decimal"
},
"float":{
'cmds':['float','decimal'],
'exec':float,
'desc':"numbers with a decimal"
},
"boolean":{
'cmds':['boolean','bool'],
'exec':get_bool,
'desc':"True or False,"
},
"DateTime":{
'cmds':['datetime'],
'exec':lambda x,format:datetime.datetime.strptime(format,x),
'desc':"date values from format and string"
},
"bytes":{
'cmds':['byte','bytes','base64bytes'],
'exec':lambda x: base64.b64decode(x.encode()),
'desc':"byte values stored as a base64 string"
},
}

class EntryDataExtras(BASE,Template):
    '''Stores extra fields not in the Entry Class.
    
    will be used with esu searches
    extras will be added under the neu menu
    data is default stored as large binary, if a serializable format is found then use that but must be usable between python versions
    '''
    
    __tablename__="EntryDataExtras"
    field_name=Column(String)
    field_type=Column(String)
    field_value=Column(String)
    doe=Column(DateTime,default=datetime.now())
    EntryId=Column(Integer)
    ede_id=Column(Integer,primary_key=True)
    
    def __init__(self,*args,**kwargs):
        fields=[i.name for i in self.__table__.columns]
        for k in kwargs:
            if k in fields:
                if k in ('field_note','field_value','field_value','field_name'):
                    setattr(self,k,str(kwargs[k]))
                else:
                    setattr(self,k,kwargs[k])
            else:
                print(k,kwargs,fields,"not in fields")
                
EntryDataExtras.metadata.create_all(ENGINE)

class EntryDataExtrasMenu:
    '''
    Add,remove,list fields,create fields EntryDataExtras
    '''
    def rm_ede_id(self):
        with Session(ENGINE) as session:
            ede_id=Prompt.__init2__(None,func=FormBuilderMkText,ptext="ExtryDataExtras.ede_id to delete?",helpText="the id value for the EntryDataExtras that you wish to delete.",data="integer")
            if ede_id in [None,]:
                return
            ede=session.query(EntryDataExtras).filter(EntryDataExtras.ede_id==ede_id).first()
            session.delete(ede)
            session.commit()

    def af2e(self):
        with Session(ENGINE) as session:
            search=Prompt.__init2__(None,func=FormBuilderMkText,ptext="Search? [Barcode,Code,Name]",helpText="searches Barcode,Code,Name",data="string")
            if search in [None]:
                return
            results=session.query(Entry).filter(or_(Entry.Barcode==search,Entry.Code==search,Entry.Barcode.icontains(search),Entry.Code.icontains(search),Entry.Name.icontains(search))).all()
            ct=len(results)
            if ct == 0:
                print("No Results were Found!")
                return
            msg=[]
            for num,i in enumerate(results):
                msg.append(f"{Fore.cyan}{num}/{Fore.light_yellow}{num+1} of {Fore.light_red}{ct}{Fore.grey_50} -> {i.seeShort()}")
            msg='\n'.join(msg)
            product=None
            while True:
                print(msg)
                index=Prompt.__init2__(None,func=FormBuilderMkText,ptext="which index do you wish to use?",helpText=msg,data="integer")
                if index in [None,]:
                    return
                try:
                    product=results[index]
                    break
                except Exception as e:
                    print(e)
            if product in [None,]:
                return
            print("af2e()")
            field_name=Prompt.__init2__(None,func=FormBuilderMkText,ptext="Field Name",helpText="make a field name",data="string")
            if field_name in [None,]:
                return
            msg=[]
            ct=len(TYPES_FromText)
            '''make a list of field types to refer to by index instead of key.'''
            ftypes=[i for i in TYPES_FromText]
            for num,i in enumerate(TYPES_FromText):
                msg.append(f"{num}/{num+1} of {ct} -> {TYPES_FromText[i]["cmds"]} - {TYPES_FromText[i]["desc"]}")
            msg='\n'.join(msg)
            print(msg)
            field_type=None
            while True:
                field_type=Prompt.__init2__(self,func=FormBuilderMkText,ptext="please select a type by index.",helpText=msg,data="integer")
                if field_type in [None,]:
                    return
                try:
                    field_type=ftypes[field_type]
                    break
                except Exception as e:
                    print(e)
            field_value=Prompt.__init2__(self,func=FormBuilderMkText,ptext="What do you wish to store as the value?",helpText=field_type,data=field_type)
            if field_value in [None,]:
                return

            print(field_name,field_type,field_value)
            extra=EntryDataExtras(field_name=field_name,field_type=field_type,field_value=field_value,EntryId=product.EntryId)
            session.add(extra)
            session.commit()
            session.refresh(extra)
            print(extra)
    def lookup(self):
        with Session(ENGINE) as session:
            search=Prompt.__init2__(None,func=FormBuilderMkText,ptext="Search? [Barcode,Code,Name]",helpText="searches Barcode,Code,Name",data="string")
            if search in [None]:
                return
            results=session.query(Entry).filter(or_(Entry.Barcode==search,Entry.Code==search,Entry.Barcode.icontains(search),Entry.Code.icontains(search),Entry.Name.icontains(search))).all()
            ct=len(results)
            if ct == 0:
                print("No Results were Found!")
                return
            msg=[]
            for num,i in enumerate(results):
                msg.append(f"{Fore.cyan}{num}/{Fore.light_yellow}{num+1} of {Fore.light_red}{ct}{Fore.grey_50} -> {i.seeShort()}")
            msg='\n'.join(msg)
            product=None
            while True:
                print(msg)
                index=Prompt.__init2__(None,func=FormBuilderMkText,ptext="which index do you wish to use?",helpText=msg,data="integer")
                if index in [None,]:
                    return
                try:
                    product=results[index]
                    break
                except Exception as e:
                    print(e)
            if product in [None,]:
                return
            extras=session.query(EntryDataExtras).filter(EntryDataExtras.EntryId==product.EntryId).all()
            extras_ct=len(extras)
            if extras_ct == 0:
                print("No Extras Found For that Item")
                return
            mtext=[]
            for n,e in enumerate(extras):
                mtext.append(f"\t- {Fore.orange_red_1}{e.field_name}:{Fore.light_steel_blue}{e.field_type}={Fore.light_yellow}{e.field_value} {Fore.cyan}ede_id={e.ede_id} {Fore.light_magenta}doe={e.doe}{Style.reset}")
            mtext='\n'.join(mtext)
            print(product.seeShort())
            print(mtext)


    def __init__(self):
        cmds={
            'af2e':{
            'cmds':['af2e','add field to entry','add field 2 entry'],
            'exec':self.af2e,
            'desc':"add field to Entry"
            },
            'rm':{
            'cmds':['rm','delete','del','remove'],
            'exec':self.rm_ede_id,
            'desc':"delete an EntryDataExtras item"
            },
            'lookup':{
            'cmds':['s','search','lu','lookup'],
            'exec':self.lookup,
            'desc':"lookup an EntryDataExtras from Entry Data"
            },

        }
        helpText=[]
        for m in cmds:
            helpText.append(f"{cmds[m]['cmds']} - {cmds[m]['desc']}")
        helpText='\n'.join(helpText)
        while True:
            doWhat=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"EntryDataExtras@{Fore.light_green}Menu{Fore.light_yellow}",helpText=helpText,data="string")
            if doWhat in [None,]:
                return
            elif doWhat in ['d',]:
                print(helpText)
                continue
            for cmd in cmds:
                check=[i.lower() for i in cmds[cmd]['cmds']]
                if doWhat.lower() in check:
                    try:
                        cmds[cmd]['exec']()
                        break
                    except Exception as e:
                        print(e)