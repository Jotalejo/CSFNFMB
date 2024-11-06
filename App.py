import csv, json, datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from wtforms import SelectField
from flask_wtf import FlaskForm

app = Flask(__name__)

# MySQL Connection :
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Sire5997_2024*.'
app.config['MYSQL_DB'] = 'coopserfun_comparacoop'
mysql = MySQL(app)

# Settings
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():    
    return render_template('index.html')

@app.route('/logearse', methods=['POST'])
def logearse():
    if request.method == 'POST':
        vusername = request.values['username']
        vpasswduser = request.values['passwduser']        
        
        curusuarios = mysql.connection.cursor()        
        curusuarios.execute( "SELECT * FROM usuarios WHERE username_usu LIKE %s", [vusername] )
        datausuarios = curusuarios.fetchall()
        curusuarios = datausuarios

        try:
            culo=int(datausuarios[0][0])
            print(culo)
        except:
            print ("Usuario erroneo")
            culo=0        

        curpasswd = mysql.connection.cursor()        
        curpasswd.execute( "SELECT * FROM usuarios WHERE passwd_usu LIKE %s AND username_usu LIKE %s", (vpasswduser,vusername))
        datapsswus = curpasswd.fetchall()
        curpasswd = datapsswus
        
        try:
            culo2=int(datapsswus[0][0])
            print(culo2)
        except:
            print ("Error de password")
            culo2=0

        if culo > 0 and culo2 > 0 :
            flash('Bienvenido !!!')
            print('Bienvenido !!!')
            return redirect(url_for('inicial'))
        else:
            flash('Error de login !!!')
            print('Error de login !!!')
            return redirect(url_for('Index'))

@app.route('/inicial')
def inicial():    
    return render_template('inicial.html')

# CRUCES
@app.route('/cruces')
def cruces():    
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM archivos_coop')
    data = cur.fetchall()    

    curs = mysql.connection.cursor()
    curs.execute('SELECT * FROM cruce')
    datas = curs.fetchall()

    culo=float(datas[0][3])
    unidadhoy=float(datas[0][2])    

    return render_template('cruces.html', cont=data, cruc=datas, putaunidad=culo, launidad=unidadhoy)

# ACA SE DEBE ABRIR EL ARCHIVO Y CONTAR SUS LINEAS
# EXTRAER LA FECHA DEL ARCHIVO Y EL NOMBRE DE LA COOPERATIVA
@app.route('/add_arc', methods=['POST'])
def add_arc():
    if request.method == 'POST':
        vinfile = request.values['infile']
        vtxtfechacsfn = request.values['txtfechacsfn']
        vValorU = request.values['ValorU']
        print(vtxtfechacsfn)
        print(vValorU)

        lista1=[]
        with open ('C:/Cosfn/CRUCES/' + vinfile) as h:
            reader11 = csv.reader(h)
            lista1=list(reader11)

        cont1=0
        fecha1=[]
        coop1=[]

        for lineaA in lista1:
            cont1+=1
                
            if cont1 == 1:                
                fecha1=lineaA
            elif cont1 == 2:                
                coop1=lineaA
        
        if cont1 > 1 :
            cont1 = cont1-2
        
        # OPERACION DE GRABACION DE LOS DATOS DEL ARCHIVO PARA DESPLEGAR EN LA LISTA
        curarc = mysql.connection.cursor()
        curarc.execute("""
        INSERT INTO archivos_coop (fec_arcproc, nomarch_arcproc, numreg_arcproc, observ_arcproc) 
        VALUES (%s,%s,%s,%s)
        """,(fecha1[0], vinfile, cont1, coop1[0]))
        mysql.connection.commit()
     
        curdcru = mysql.connection.cursor()
        curdcru.execute("""
        UPDATE cruce SET fec_cruce=%s, valoruni_crucel=%s WHERE cruce.cod_cruce = 1        
        """,(vtxtfechacsfn, vValorU))
        mysql.connection.commit()

        flash('Archivo agregado')
        return redirect(url_for('cruces'))

@app.route('/deletearc/<string:id>')
def delete_arch(id):
    cursi = mysql.connection.cursor()
    cursi.execute('DELETE FROM archivos_coop WHERE cod_arcproc = {0}'.format(id))
    mysql.connection.commit()
    flash('Archivo eliminado')
    return redirect(url_for('cruces'))

@app.route('/pcruce')
def pcruce():
    cur1 = mysql.connection.cursor()
    cur1.execute('SELECT * FROM archivos_coop')
    data1 = cur1.fetchall()

    cur2 = mysql.connection.cursor()
    cur2.execute('SELECT * FROM cruce')
    data2 = cur2.fetchall()

    contarc=0

    posicavip=0
    estacavip='false'

    posicoopt=0
    estacoopt='false'

    posicopacr=0
    estacopacr='false'

    posicopacent=0
    estacopacent='false'

    posicopadct=0
    estacopadct='false'

    posicopcrec=0
    estacopcrec='false'

    for verarc in data1:
        if verarc[4] == 'CAVIPETROL':
            posicavip=contarc
            print(posicavip)
            contarc+=1
            print(verarc[4])
            estacavip='true'
            narchCavip = verarc[2]
            print(narchCavip)
            lista1=[]
            numregCavip = int(verarc[3])
            print("El numero de registros para Cavipetrol es de",(numregCavip))

        if verarc[4] == 'COOPETROL':
            posicoopt=contarc
            print(posicoopt)
            contarc+=1
            print(verarc[4])
            estacoopt='true'
            narchCoopt = verarc[2]
            print(narchCoopt)
            lista2=[]
            numregCoopt = int(verarc[3])
            print("El numero de registros para Coopetrol es de",(numregCoopt))

        if verarc[4] == 'COPACREDITO':
            posicopacr=contarc
            print(posicopacr)
            contarc+=1
            print(verarc[4])
            estacopacr='true'
            narchCpcred = verarc[2]
            print(narchCpcred)
            lista3=[]
            numregCpcred = int(verarc[3])
            print("El numero de registros para Copacrédito es de",(numregCpcred))

        if verarc[4] == 'COPACENTRO':
            posicopacent=contarc
            print(posicopacent)
            contarc+=1
            print(verarc[4])
            estacopacent='true'
            narchCopactr = verarc[2]
            print(narchCopactr)
            lista4=[]
            numregCopactr = int(verarc[3])
            print("El numero de registros para Copacentro es de",(numregCopactr))

        if verarc[4] == 'COOPADUCTOS':
            posicopadct=contarc
            print(posicopadct)
            contarc+=1
            print(verarc[4])
            estacopadct='true'
            narchCpduc = verarc[2]
            print(narchCpduc)
            lista5=[]
            numregCpduc = int(verarc[3])
            print("El numero de registros para Coopaductos es de",(numregCpduc))

        if verarc[4] == 'CRECENTRO':
            posicopcrec=contarc
            print(posicopcrec)
            contarc+=1
            print(verarc[4])
            estacopcrec='true'
            narchCopcrec = verarc[2]
            print(narchCopcrec)
            lista6=[]
            numregCopcrec = int(verarc[3])
            print("El numero de registros para Crecentro es de",(numregCopcrec))    
   
    print("El numero de archivos para Procesar es de",(contarc))

    vr_uni=float(data2[0][2])
    #vr_uni=float(data2[0][3])
    reputin=0

    #CAVIPETROL : si se detecta que no hay archivo o el número de registros es cero, entonces mande 0 al reporte
    rep1_cavip=0
    rep2_cavip=0
    rep3_cavip=0
    rep4_cavip=0
    rep5_cavip=0
    rep6_cavip=0
    tot_cavip=0
    subtCavip=0
    salec1='no'

    if estacavip == 'true' :
        if numregCavip > 0 :            
            with open ('C:\\Cosfn\\CRUCES\\'+narchCavip) as h:
                reader11 = csv.reader(h)
                lista1=list(reader11)
            lista1.pop(0)
            lista1.pop(0)

        else :
            print("no hay registros para Cavipetrol")
            lista1=['0','0','0']
            salec1='si'
    else:
        lista1=['0','0','0']
        salec1='si'

    #COOPETROL :
    rep1_coop=0
    rep2_coop=0
    rep3_coop=0
    rep4_coop=0
    rep5_coop=0
    rep6_coop=0
    tot_coop=0
    subtCoop=0
    salec2='no'

    if estacoopt == 'true' :
        if numregCoopt > 0 :
            with open ('C:\\Cosfn\\CRUCES\\' + narchCoopt ) as i:
                reader12 = csv.reader(i)
                lista2=list(reader12)
            lista2.pop(0)
            lista2.pop(0)
        else :
            print("no hay registros para Coopetrol")
            lista2=['1','1','1']
            salec2='si'
    else:
        lista2=['1','1','1']
        salec2='si'

    #COPACREDITO :
    rep1_copac=0
    rep2_copac=0
    rep3_copac=0
    rep4_copac=0
    rep5_copac=0
    rep6_copac=0
    tot_copac=0
    subtCopac=0
    salec3='no'

    if estacopacr == 'true' :
        if numregCpcred > 0 :
            with open ('C:\\Cosfn\\CRUCES\\' + narchCpcred ) as j:
                reader13 = csv.reader(j)
                lista3=list(reader13)
            lista3.pop(0)
            lista3.pop(0)
        else :
            print("no hay registros para Copacrédito")
            lista3=['2','2','2']
            salec3='si'
    else:
        lista3=['2','2','2']
        salec3='si'

    #COPACENTRO :
    rep1_coptro=0
    rep2_coptro=0
    rep3_coptro=0
    rep4_coptro=0
    rep5_coptro=0
    rep6_coptro=0
    tot_coptro=0
    subtCoptro=0
    salec4='no'

    if estacopacent == 'true' :
        if numregCopactr > 0 :
            with open ('C:\\Cosfn\\CRUCES\\' + narchCopactr ) as k:
                reader14 = csv.reader(k)
                lista4=list(reader14)
            lista4.pop(0)
            lista4.pop(0)
        else :
            print("no hay registros para Copacentro")
            lista4=['3','3','3']
            salec4='si'
    else:
        lista4=['3','3','3']
        salec4='si'

    #COOPADUCTOS :
    rep1_coopdc=0
    rep2_coopdc=0
    rep3_coopdc=0
    rep4_coopdc=0
    rep5_coopdc=0
    rep6_coopdc=0
    tot_coopdc=0
    subtCoopdc=0
    salec5='no'

    if estacopadct == 'true' :
        if numregCpduc > 0 :
            with open ('C:\\Cosfn\\CRUCES\\' + narchCpduc ) as l:
                reader15 = csv.reader(l)
                lista5=list(reader15)
            lista5.pop(0)
            lista5.pop(0)
        else :
            print("no hay registros para Coopaductos")
            lista5=['4','4','4']
            salec5='si'
    else:
        lista5=['4','4','4']
        salec5='si'

    #CRECENTRO :
    rep1_copcrec=0
    rep2_copcrec=0
    rep3_copcrec=0
    rep4_copcrec=0
    rep5_copcrec=0
    rep6_copcrec=0
    tot_copcrec=0
    subtCopcrec=0
    salec6='no'

    if estacopcrec == 'true' :
        if numregCopcrec > 0 :
            with open ('C:\\Cosfn\\CRUCES\\' + narchCopcrec ) as m:
                reader16 = csv.reader(m)
                lista6=list(reader16)
            lista6.pop(0)
            lista6.pop(0)
        else :
            print("no hay registros para Crecentro")
            lista6=['5','5','5']
            salec6='si'
    else:
        lista6=['5','5','5']
        salec6='si'

    # A CONTINUACION SE RECORREN LAS LISTAS PARA CALCULAR LOS CRUCES
    # CAVIPETROL :
    list_rep2_cavip = []
    list_rep3_cavip = []
    list_rep4_cavip = []
    list_rep5_cavip = []

    for recorre in lista1:
        if recorre in lista2 :
            reputin+=1
            
        if recorre in lista3 :
            reputin+=1
            
        if recorre in lista4 :
            reputin+=1
            
        if recorre in lista5 :
            reputin+=1

        if recorre in lista6 :
            reputin+=1
            
        if reputin == 1:
            rep2_cavip+=1
            list_rep2_cavip.append(recorre)
        elif reputin == 2:
            list_rep3_cavip.append(recorre)
            rep3_cavip+=1
        elif reputin == 3:
            rep4_cavip+=1
            list_rep4_cavip.append(recorre)
        elif reputin == 4:
            rep5_cavip+=1
            list_rep5_cavip.append(recorre)
        elif reputin == 5:
            rep6_cavip+=1    
            
        reputin=0

    if salec1 == 'si' :
        tot_cavip = 1
        tot_cavip1 = 0
    else:
        tot_cavip=len(lista1)
        tot_cavip1 = tot_cavip
    
    rep1_cavip = tot_cavip - ( rep2_cavip + rep3_cavip + rep4_cavip + rep5_cavip)
    subtCavip = (vr_uni * rep1_cavip) + ( vr_uni / 2 * rep2_cavip ) + ( vr_uni / 3 * rep3_cavip )
    subtCavip = subtCavip + ( vr_uni / 4 * rep4_cavip ) + ( vr_uni / 5 * rep5_cavip) + ( vr_uni / 6 * rep6_cavip)

    if salec1 == 'si' :
        rep1_cavip = 0
        subtCavip = 0

    # COOPETROL :    
    reputin=0
    for recorrecl in lista2:
        if recorrecl in lista1 :
            reputin+=1
            
        if recorrecl in lista3 :
            reputin+=1
            
        if recorrecl in lista4 :
            reputin+=1
            
        if recorrecl in lista5 :
            reputin+=1

        if recorrecl in lista6 :
            reputin+=1

        if reputin == 1:
            rep2_coop+=1
        elif reputin == 2:
            rep3_coop+=1
        elif reputin == 3:
            rep4_coop+=1
        elif reputin == 4:
            rep5_coop+=1
        elif reputin == 5:
            rep6_coop+=1

        reputin=0

    if salec2 == 'si' :
        tot_coop = 1
        tot_coop1 = 0
    else:
        tot_coop=len(lista2)
        tot_coop1 = tot_coop

    rep1_coop = tot_coop - ( rep2_coop + rep3_coop + rep4_coop + rep5_coop)
    subtCoop = (vr_uni * rep1_coop) + ( vr_uni / 2 * rep2_coop ) + ( vr_uni / 3 * rep3_coop )
    subtCoop = subtCoop + ( vr_uni / 4 * rep4_coop ) + ( vr_uni / 5 * rep5_coop) + ( vr_uni / 6 * rep6_coop)

    if salec2 == 'si' :
        rep1_coop = 0
        subtCoop = 0

    # COPACREDITO :
    reputin=0
    for recorrecR in lista3:
        if recorrecR in lista1 :
            reputin+=1
            
        if recorrecR in lista2 :
            reputin+=1
            
        if recorrecR in lista4 :
            reputin+=1
            
        if recorrecR in lista5 :
            reputin+=1

        if recorrecR in lista6 :
            reputin+=1

        if reputin == 1:
            rep2_copac+=1
        elif reputin == 2:
            rep3_copac+=1
        elif reputin == 3:
            rep4_copac+=1
        elif reputin == 4:
            rep5_copac+=1            
        elif reputin == 5:
            rep6_copac+=1

        reputin=0

    if salec3 == 'si' :
        tot_copac = 1
        tot_copac1 = 0
    else:
        tot_copac=len(lista3)
        tot_copac1 = tot_copac

    tot_copac=len(lista3)
    rep1_copac = tot_copac - ( rep2_copac + rep3_copac + rep4_copac + rep5_copac)
    subtCopac = (vr_uni * rep1_copac) + ( vr_uni / 2 * rep2_copac ) + ( vr_uni / 3 * rep3_copac )
    subtCopac = subtCopac + ( vr_uni / 4 * rep4_copac ) + ( vr_uni / 5 * rep5_copac) + ( vr_uni / 6 * rep6_copac)

    if salec3 == 'si' :
        rep1_copac = 0
        subtCopac = 0

    # COPACENTRO :
    reputin=0
    for recorrecT in lista4:
        if recorrecT in lista1 :
            reputin+=1
            
        if recorrecT in lista2 :
            reputin+=1
            
        if recorrecT in lista3 :
            reputin+=1
            
        if recorrecT in lista5 :
            reputin+=1

        if recorrecT in lista6 :
            reputin+=1
            
        if reputin == 1:
            rep2_coptro+=1
        elif reputin == 2:
            rep3_coptro+=1
        elif reputin == 3:
            rep4_coptro+=1
        elif reputin == 4:
            rep5_coptro+=1            
        elif reputin == 5:
            rep6_coptro+=1

        reputin=0

    if salec4 == 'si' :
        tot_coptro = 1
        tot_coptro1 = 0
    else:
        tot_coptro=len(lista4)
        tot_coptro1 = tot_coptro

    tot_coptro=len(lista4)
    rep1_coptro = tot_coptro - ( rep2_coptro + rep3_coptro + rep4_coptro + rep5_coptro)
    subtCoptro = (vr_uni * rep1_coptro) + ( vr_uni / 2 * rep2_coptro ) + ( vr_uni / 3 * rep3_coptro )
    subtCoptro = subtCoptro + ( vr_uni / 4 * rep4_coptro ) + ( vr_uni / 5 * rep5_coptro) + ( vr_uni / 6 * rep6_coptro)

    if salec4 == 'si' :
        rep1_coptro = 0
        subtCoptro = 0

    #COOPADUCTOS
    reputin=0
    for recorreD in lista5:
        if recorreD in lista1 :
            reputin+=1
            
        if recorreD in lista2 :
            reputin+=1
            
        if recorreD in lista3 :
            reputin+=1
            
        if recorreD in lista4 :
            reputin+=1
            
        if recorreD in lista6 :
            reputin+=1

        if reputin == 1:
            rep2_coopdc+=1
        elif reputin == 2:
            rep3_coopdc+=1
        elif reputin == 3:
            rep4_coopdc+=1
        elif reputin == 4:
            rep5_coopdc+=1
        elif reputin == 5:
            rep6_coopdc+=1
            
        reputin=0

    if salec5 == 'si' :
        tot_coopdc = 1
        tot_coopdc1 = 0
    else:
        tot_coopdc=len(lista5)
        tot_coopdc1 = tot_coopdc

    tot_coopdc=len(lista5)
    rep1_coopdc = tot_coopdc - ( rep2_coopdc + rep3_coopdc + rep4_coopdc + rep5_coopdc)
    subtCoopdc = (vr_uni * rep1_coopdc) + ( vr_uni / 2 * rep2_coopdc ) + ( vr_uni / 3 * rep3_coopdc )
    subtCoopdc = subtCoopdc + ( vr_uni / 4 * rep4_coopdc ) + ( vr_uni / 5 * rep5_coopdc) + ( vr_uni / 6 * rep6_coopdc)

    if salec5 == 'si' :
        rep1_coopdc = 0
        subtCoopdc = 0

    #CRECENTRO
    reputin=0
    for recorreE in lista6:
        if recorreE in lista1 :
            reputin+=1
            
        if recorreE in lista2 :
            reputin+=1
            
        if recorreE in lista3 :
            reputin+=1
            
        if recorreE in lista4 :
            reputin+=1

        if recorreE in lista5 :
            reputin+=1

        if reputin == 1:
            rep2_copcrec+=1
        elif reputin == 2:
            rep3_copcrec+=1
        elif reputin == 3:
            rep4_copcrec+=1
        elif reputin == 4:
            rep5_copcrec+=1
        elif reputin == 5:
            rep6_copcrec+=1    
            
        reputin=0

    if salec6 == 'si' :
        tot_copcrec = 1
        tot_copcrec1 = 0
    else:
        tot_copcrec=len(lista6)
        tot_copcrec1 = tot_copcrec

    tot_copcrec=len(lista6)
    rep1_copcrec = tot_copcrec - ( rep2_copcrec + rep3_copcrec + rep4_copcrec + rep5_copcrec + rep6_copcrec)
    subtCopcrec = (vr_uni * rep1_copcrec) + ( vr_uni / 2 * rep2_copcrec ) + ( vr_uni / 3 * rep3_copcrec )
    subtCopcrec = subtCopcrec + ( vr_uni / 4 * rep4_copcrec ) + ( vr_uni / 5 * rep5_copcrec) + ( vr_uni / 6 * rep6_copcrec)

    if salec6 == 'si' :
        rep1_copcrec = 0
        subtCopcrec = 0
        
    return render_template('pcruce.html', vunidad = vr_uni, datcru=data2, cont1=data1, 
    rep1Cavip=rep1_cavip, rep2Cavip=rep2_cavip, listarp2cavip=list_rep2_cavip, rep3Cavip=rep3_cavip, listarp3cavip=list_rep3_cavip,
    rep4Cavip=rep4_cavip, listarp4cavip=list_rep4_cavip, rep5Cavip=rep5_cavip, listarp5cavip=list_rep5_cavip, rep6Cavip=rep6_cavip,
    totCavip=tot_cavip, totCavip1=tot_cavip1, subtCavipet=subtCavip,
    rep1Coop=rep1_coop, rep2Coop=rep2_coop, rep3Coop=rep3_coop, rep4Coop=rep4_coop,
    rep5Coop=rep5_coop, rep6Coop=rep6_coop, totCoop=tot_coop, totCoop1=tot_coop1, subtCoopetr=subtCoop,
    rep1Copac=rep1_copac, rep2Copac=rep2_copac, rep3Copac=rep3_copac, rep4Copac=rep4_copac,
    rep5Copac=rep5_copac, rep6Copac=rep6_copac, totCopac=tot_copac, totCopac1=tot_copac1, subtCopacred=subtCopac,
    rep1Coptro=rep1_coptro, rep2Coptro=rep2_coptro, rep3Coptro=rep3_coptro, rep4Coptro=rep4_coptro,
    rep5Coptro=rep5_coptro, rep6Coptro=rep6_coptro, totCoptro=tot_coptro, totCoptro1=tot_coptro1, subtCopactr=subtCoptro,
    rep1Coopdc=rep1_coopdc, rep2Coopdc=rep2_coopdc, rep3Coopdc=rep3_coopdc, rep4Coopdc=rep4_coopdc,
    rep5Coopdc=rep5_coopdc, rep6Coopdc=rep6_coopdc, totCoopdc=tot_coopdc, totCoopdc1=tot_coopdc1, subtCoopad=subtCoopdc,
    rep1Copcrec=rep1_copcrec, rep2Copcrec=rep2_copcrec, rep3Copcrec=rep3_copcrec, rep4Copcrec=rep4_copcrec,
    rep5Copcrec=rep5_copcrec, rep6Copcrec=rep6_copcrec, totCopcrec=tot_copcrec, totCopcrec1=tot_copcrec1, subtCopcrec=subtCopcrec)

#Generador de Archivos para el Cruce - solo falta construir el archivo plano:
@app.route('/generacru/<idgen>,archi')
def get_sect(idgen,archi):
    archi = archi + ".csv"

    print(idgen)
    
    for verlalis in idgen:
        print(verlalis)

    file_to_output = open(archi,'w',newline='')
    csv_writer = csv.writer(file_to_output,delimiter=",")

    for laced in idgen:      
        csv_writer.writerows(laced)

    file_to_output.close()

    return archi

#DETALLES
@app.route('/detalle')
def detalle():
    cur1 = mysql.connection.cursor()
    cur1.execute('SELECT * FROM archivos_coop')
    data1 = cur1.fetchall()

    cur2 = mysql.connection.cursor()
    cur2.execute('SELECT * FROM cruce')
    data2 = cur2.fetchall()

    contarc=0

    posicavip=0
    estacavip='false'

    posicoopt=0
    estacoopt='false'

    posicopacr=0
    estacopacr='false'

    posicopacent=0
    estacopacent='false'

    posicopadct=0
    estacopadct='false'

    for verarc in data1:        
        #if verarc[4] == 'CAVIPETROL':
        #    posicavip=contarc
        #    print(posicavip)
        #    contarc+=1
        #    print(verarc[4])
        #    estacavip='true'
        #    narchCavip = verarc[2]
        #    print(narchCavip)
        #    lista1=[]
        #    numregCavip = int(verarc[3])
        #    tot_cavip = int(verarc[3])
        #    print("El numero de registros para Cavipetrol es de",(numregCavip))

        if verarc[4] == 'COOPETROL':
            posicoopt=contarc
            print(posicoopt)
            contarc+=1
            print(verarc[4])
            estacoopt='true'
            narchCoopt = verarc[2]
            print(narchCoopt)
            lista2=[]
            numregCoopt = int(verarc[3])
            tot_coop = int(verarc[3])
            print("El numero de registros para Coopetrol es de",(numregCoopt))

        if verarc[4] == 'COPACREDITO':
            posicopacr=contarc
            print(posicopacr)
            contarc+=1
            print(verarc[4])
            estacopacr='true'
            narchCpcred = verarc[2]
            print(narchCpcred)
            lista3=[]
            numregCpcred = int(verarc[3])
            tot_copac = int(verarc[3])
            print("El numero de registros para Copacrédito es de",(numregCpcred))

        if verarc[4] == 'COOPADUCTOS':
            posicopadct=contarc
            print(posicopadct)
            contarc+=1
            print(verarc[4])
            estacopadct='true'
            narchCpduc = verarc[2]
            print(narchCpduc)
            lista4=[]
            numregCpduc = int(verarc[3])
            tot_coopdc = int(verarc[3])
            print("El numero de registros para Coopaductos es de",(numregCpduc))            

        if verarc[4] == 'COPACENTRO':
            posicopacent=contarc
            print(posicopacent)
            contarc+=1
            print(verarc[4])
            estacopacent='true'
            narchCopactr = verarc[2]
            print(narchCopactr)
            lista5=[]
            numregCopactr = int(verarc[3])
            tot_coptro = int(verarc[3])
            print("El numero de registros para Copacentro es de",(numregCopactr))
   
    print("El numero de archivos para Procesar es de",(contarc))
    print('          ')

    vr_uni=float(data2[0][2])
    #vr_uni=float(data2[0][3])
    fch_uni=data2[0][1]

    print(vr_uni)
    print(fch_uni)

    # Envía un número de cédula para buscar y una lista en la cual NO, que es la que busca en las otras

    # def busca_rep(recorre, listaExc1, listaExc2, listaExc3, listaExc4, listaExc5):
    def busca_rep(recorre, listaExc2, listaExc3, listaExc4, listaExc5):
            
        reputin=0           
        
        #if (listaExc1 != "lista1" and listaExc2 != "lista1" and listaExc3 != "lista1" and listaExc4 != "lista1" and listaExc5 != "lista1") :
        #    if [recorre] in lista1 :
        #        reputin+=1       

        if (listaExc2 != "lista2" and listaExc3 != "lista2" and listaExc4 != "lista2" and listaExc5 != "lista2") :
            if [recorre] in lista2 :
                reputin+=1

        if (listaExc2 != "lista3" and listaExc3 != "lista3" and listaExc4 != "lista3" and listaExc5 != "lista3") :
            if [recorre] in lista3 :
                reputin+=1
        
        if (listaExc2 != "lista4" and listaExc3 != "lista4" and listaExc4 != "lista4" and listaExc5 != "lista4") :
            if [recorre] in lista4 :
                reputin+=1
                
        if (listaExc2 != "lista5" and listaExc3 != "lista5" and listaExc4 != "lista5" and listaExc5 != "lista5") :
            if [recorre] in lista5 :
                reputin+=1        

        return reputin

# Envía un número de cédula para buscar y una lista en la cual NO, que es la que busca en las otras

    def busca_repk(recorre, listaExc1, listaExc2, listaExc3, listaExc4, listaExc5):
    # def busca_rep(recorre, listaExc2, listaExc3, listaExc4, listaExc5):
            
        reputin=0           
        
        #if (listaExc1 != "lista1" and listaExc2 != "lista1" and listaExc3 != "lista1" and listaExc4 != "lista1" and listaExc5 != "lista1") :
        #    if [recorre] in lista1 :
        #        reputin+=1       

        if (listaExc2 != "lista2" and listaExc3 != "lista2" and listaExc4 != "lista2" and listaExc5 != "lista2") :
            if [recorre] in lista2 :
                reputin+=1

        if (listaExc2 != "lista3" and listaExc3 != "lista3" and listaExc4 != "lista3" and listaExc5 != "lista3") :
            if [recorre] in lista3 :
                reputin+=1
        
        if (listaExc2 != "lista4" and listaExc3 != "lista4" and listaExc4 != "lista4" and listaExc5 != "lista4") :
            if [recorre] in lista4 :
                reputin+=1
                
        if (listaExc2 != "lista5" and listaExc3 != "lista5" and listaExc4 != "lista5" and listaExc5 != "lista5") :
            if [recorre] in lista5 :
                reputin+=1        

        return reputin
    
    #CAVIPETROL : si se detecta que no hay archivo o el número de registros es cero, entonces mande 0 al reporte
    
    #salec1='no'

    #if estacavip == 'true' :
    #    rcavip_cooptr=0
    #    rcavip_copacred=0
    #    rcavip_coopadct=0
    #    rcavip_copacen=0  
        
    #    rcavip_copacred_cooptr=0
    #    rcavip_copacred_copacen=0
    #    rcavip_copacred_coopadct=0
    #    rcavip_cooptr_copacen=0
    #    rcavip_cooptr_coopadct=0
    #    rcavip_copacen_coopadct=0
    #    rcavip_copacred_cooptr_copacen=0
    #    rcavip_copacred_cooptr_coopadct=0
    #    rcavip_copacred_copacen_coopadct=0
    #    rcavip_cooptr_copacen_coopadct=0
    #    rcavip_copacred_cooptr_copacen_coopadct=0
    #    my_resultA=0
    #    Stot_Cavip=0
    #    rep1_cavip = 0

    #    if numregCavip > 0 :            
    #        with open ('C:\\Cosfn\\CRUCES\\'+narchCavip) as h:
    #            reader11 = csv.reader(h)
    #            lista1=list(reader11)
    #        lista1.pop(0)
    #       lista1.pop(0)

    #    else :
    #        print("no hay registros para Cavipetrol")
    #        lista1=['0','0','0']
    #        salec1='si'
    #else:
    #    lista1=['0','0','0']
    #    salec1='si'

    # << COOPETROL : >>

    salec2='no'

    if estacoopt == 'true' :
        #rcoop_caviptr=0
        rcoop_copacred=0
        rcoop_coopadct=0
        rcoop_copacen=0
        
        #rcoop_caviptr_copacred=0
        #rcoop_caviptr_copacen=0
        #rcoop_caviptr_coopadct=0
        rcoop_copacred_copacen=0
        rcoop_copacred_coopadct=0
        rcoop_copacen_coopadct=0
        #rcoop_caviptr_copacred_copacen=0
        #rcoop_caviptr_copacred_coopadct=0
        #rcoop_caviptr_copacen_coopadct=0
        rcoop_copacred_copacen_coopadct=0        
        #rcoop_caviptr_copacred_copacen_coopadct=0
        my_resultA=0
        Stot_Coop=0
        rep1_coop = 0

        if numregCoopt > 0 :
            with open ('C:\\Cosfn\\CRUCES\\' + narchCoopt ) as i:
                reader12 = csv.reader(i)
                lista2=list(reader12)
            lista2.pop(0)
            lista2.pop(0)
        else :
            print("no hay registros para Coopetrol")
            lista2=['1','1','1']
            salec2='si'
    else:
        lista2=['1','1','1']
        salec2='si'

    #  << COPACREDITO : >>
            
    salec3='no'

    if estacopacr == 'true' :
        #rcopac_caviptr=0
        rcopac_cooptr=0
        rcopac_copacen=0        
        rcopac_coopadct=0        
        
        #rcopac_caviptr_cooptr=0
        #rcopac_caviptr_copacen=0
        #rcopac_caviptr_coopadct=0        
        rcopac_cooptr_copacen=0
        rcopac_cooptr_coopadct=0        
        rcopac_copacen_coopadct=0
        #rcopac_caviptr_cooptr_copacen=0
        #rcopac_caviptr_cooptr_coopadct=0
        #rcopac_caviptr_copacen_coopadct=0
        rcopac_cooptr_copacen_coopadct=0        
        #rcopac_caviptr_cooptr_copacen_coopadct=0
        my_resultA=0
        Stot_Copac=0
        rep1_copac = 0

        if numregCpcred > 0 :
            with open ('C:\\Cosfn\\CRUCES\\' + narchCpcred ) as j:
                reader13 = csv.reader(j)
                lista3=list(reader13)
            lista3.pop(0)
            lista3.pop(0)
        else :
            print("no hay registros para Copacrédito")
            lista3=['2','2','2']
            salec3='si'
    else:
        lista3=['2','2','2']
        salec3='si'
    
    # << COOPADUCTOS : >>
    
    salec4='no'

    if estacopadct == 'true' :
        # rcoopdc_caviptr=0        
        rcoopdc_cooptr=0
        rcoopdc_copacen=0
        rcoopdc_copacred=0        
        
        # rcoopdc_caviptr_cooptr=0
        # rcoopdc_caviptr_copacen=0        
        # rcoopdc_caviptr_copacred=0
        rcoopdc_cooptr_copacen=0
        rcoopdc_cooptr_copacred=0
        rcoopdc_copacen_copacred=0
        # rcoopdc_caviptr_cooptr_copacen=0        
        # rcoopdc_caviptr_cooptr_copacred=0        
        # rcoopdc_caviptr_copacen_copacred=0
        rcoopdc_cooptr_copacen_copacred=0
        # rcoopdc_caviptr_cooptr_copacen_copacred=0
        my_resultA=0
        Stot_Coopdc=0
        rep1_coopdc = 0

        if numregCpduc > 0 :
            with open ('C:\\Cosfn\\CRUCES\\' + narchCpduc ) as l:
                reader15 = csv.reader(l)
                lista4=list(reader15)
            lista4.pop(0)
            lista4.pop(0)
        else :
            print("no hay registros para Coopaductos")
            lista4=['3','3','3']
            salec4='si'
    else:
        lista4=['3','3','3']
        salec4='si'
            
    # << COPACENTRO : >>
        
    salec5='no'

    if estacopacent == 'true' :
        # rcpctro_caviptr=0
        rcpctro_cooptr=0
        rcpctro_copacred=0
        rcpctro_coopadct=0        
        
        #rcpctro_caviptr_cooptr=0
        #rcpctro_caviptr_copacred=0
        #rcpctro_caviptr_coopadct=0
        rcpctro_cooptr_copacred=0
        rcpctro_cooptr_coopadct=0
        rcpctro_copacred_coopadct=0
        #rcpctro_caviptr_cooptr_copacred=0
        #rcpctro_caviptr_cooptr_coopadct=0
        #rcpctro_caviptr_copacred_coopadct=0
        rcpctro_cooptr_copacred_coopadct=0        
        #rcpctro_caviptr_cooptr_copacred_coopadct=0
        my_resultA=0
        Stot_Coptro=0
        rep1_coptro = 0

        if numregCopactr > 0 :
            with open ('C:\\Cosfn\\CRUCES\\' + narchCopactr ) as k:
                reader14 = csv.reader(k)
                lista5=list(reader14)
            lista5.pop(0)
            lista5.pop(0)
        else :
            print("no hay registros para Copacentro")
            lista5=['4','4','4']
            salec5='si'
    else:
        lista5=['4','4','4']
        salec5='si'
            
#ACA COMIENZA EL CALCULO DEL DETALLE PARA DESPLEGAR:

#CAVIPETROL:
    #for recorreA in lista1:
    #    if recorreA in lista2 :
    #        rcavip_cooptr+=1
    #        my_resultA = busca_rep(recorreA[0],"lista1","lista2","lista2","lista2","lista2")
    #        if my_resultA > 0:
    #            rcavip_cooptr=rcavip_cooptr-1
    #            my_resultA=0
    
    #    if recorreA in lista3 :
    #        rcavip_copacred+=1
    #        my_resultA = busca_rep(recorreA[0],"lista1","lista3","lista3","lista3","lista3")
    #        if my_resultA > 0:
    #            rcavip_copacred=rcavip_copacred-1
    #            my_resultA=0
                                    
    #    if recorreA in lista4 :
    #        rcavip_coopadct+=1
    #        my_resultA = busca_rep(recorreA[0],"lista1","lista4","lista4","lista4","lista4")
    #        if my_resultA > 0:
    #            rcavip_coopadct=rcavip_coopadct-1
    #            my_resultA=0            

    #    if recorreA in lista5 :
    #        rcavip_copacen+=1
    #        my_resultA = busca_rep(recorreA[0],"lista1","lista5","lista5","lista5","lista5")
    #        if my_resultA > 0:
    #            rcavip_copacen=rcavip_copacen-1
    #            my_resultA=0

    #    if recorreA in lista3 and recorreA in lista2 :
    #        rcavip_copacred_cooptr+=1
    #        my_resultA = busca_rep(recorreA[0],"lista1","lista2","lista3","lista3","lista3")
    #        if my_resultA > 0:
    #            rcavip_copacred_cooptr=rcavip_copacred_cooptr-1
    #            my_resultA=0
                
    #    if recorreA in lista3 and recorreA in lista5 :
    #        rcavip_copacred_copacen+=1
    #        my_resultA = busca_rep(recorreA[0],"lista1","lista5","lista3","lista3","lista3")
    #        if my_resultA > 0:
    #            rcavip_copacred_copacen=rcavip_copacred_copacen-1
    #            my_resultA=0
        
    #    if recorreA in lista3 and recorreA in lista4 :
    #        rcavip_copacred_coopadct+=1
    #        my_resultA = busca_rep(recorreA[0],"lista1","lista4","lista3","lista3","lista3")
    #        if my_resultA > 0:
    #            rcavip_copacred_coopadct=rcavip_copacred_coopadct-1
    #            my_resultA=0
                
    #    if recorreA in lista2 and recorreA in lista5 :
    #        rcavip_cooptr_copacen+=1
    #        my_resultA = busca_rep(recorreA[0],"lista1","lista5","lista2","lista2","lista2")
    #        if my_resultA > 0:
    #            rcavip_cooptr_copacen=rcavip_cooptr_copacen-1
    #            my_resultA=0
                
    #    if recorreA in lista2 and recorreA in lista4 :
    #        rcavip_cooptr_coopadct+=1
    #        my_resultA = busca_rep(recorreA[0],"lista1","lista4","lista2","lista2","lista2")
    #        if my_resultA > 0:
    #            rcavip_cooptr_coopadct=rcavip_cooptr_coopadct-1
    #            my_resultA=0
                
    #    if recorreA in lista5 and recorreA in lista4 :
    #        rcavip_copacen_coopadct+=1
    #        my_resultA = busca_rep(recorreA[0],"lista1","lista4","lista5","lista5","lista5")
    #        if my_resultA > 0:
    #            rcavip_copacen_coopadct=rcavip_copacen_coopadct-1
    #            my_resultA=0
                                                
    #    if recorreA in lista3 and recorreA in lista2 and recorreA in lista5 :
    #        rcavip_copacred_cooptr_copacen+=1
    #        my_resultA = busca_rep(recorreA[0],"lista1","lista3","lista2","lista5","lista5")
    #        if my_resultA > 0:
    #            rcavip_copacred_cooptr_copacen=rcavip_copacred_cooptr_copacen-1
    #            my_resultA=0
                
    #    if recorreA in lista3 and recorreA in lista2 and recorreA in lista4 :
    #        rcavip_copacred_cooptr_coopadct+=1
    #        my_resultA = busca_rep(recorreA[0],"lista1","lista3","lista2","lista4","lista4")
    #        if my_resultA > 0:
    #            rcavip_copacred_cooptr_coopadct=rcavip_copacred_cooptr_coopadct-1
    #            my_resultA=0
                
    #    if recorreA in lista3 and recorreA in lista5 and recorreA in lista4 :
    #        rcavip_copacred_copacen_coopadct+=1
    #        my_resultA = busca_rep(recorreA[0],"lista1","lista3","lista5","lista4","lista4")
    #        if my_resultA > 0:
    #           rcavip_copacred_copacen_coopadct=rcavip_copacred_copacen_coopadct-1
    #            my_resultA=0
                
    #    if recorreA in lista2 and recorreA in lista5 and recorreA in lista4 :
    #        rcavip_cooptr_copacen_coopadct+=1
    #        my_resultA = busca_rep(recorreA[0],"lista1","lista2","lista5","lista4","lista4")
    #        if my_resultA > 0:
    #            rcavip_cooptr_copacen_coopadct=rcavip_cooptr_copacen_coopadct-1
    #            my_resultA=0
                
    #    if recorreA in lista3 and recorreA in lista2 and recorreA in lista5 and recorreA in lista4 :
    #        rcavip_copacred_cooptr_copacen_coopadct+=1
    #        my_resultA = busca_rep(recorreA[0],"lista1","lista3","lista2","lista5","lista4")
    #        if my_resultA > 0:
    #            rcavip_copacred_cooptr_copacen_coopadct=rcavip_copacred_cooptr_copacen_coopadct-1
    #            my_resultA=0
    
     #   rep1_cavip = 0
   # rep1_cavip = rcavip_copacred+rcavip_cooptr+rcavip_copacen+rcavip_coopadct
   # rep1_cavip = rep1_cavip + rcavip_copacred_cooptr+rcavip_copacred_copacen+rcavip_copacred_coopadct+rcavip_cooptr_copacen
   # rep1_cavip = rep1_cavip + rcavip_cooptr_coopadct+rcavip_copacen_coopadct+rcavip_copacred_cooptr_copacen
   # rep1_cavip = rep1_cavip + rcavip_copacred_cooptr_coopadct+rcavip_copacred_copacen_coopadct+rcavip_cooptr_copacen_coopadct
   # rep1_cavip = rep1_cavip + rcavip_copacred_cooptr_copacen_coopadct
   # Stot_Cavip = tot_cavip - rep1_cavip   

#COOPETROL
    for recorreA in lista2:        
    
        if recorreA in lista3 :
            rcoop_copacred+=1
            my_resultA = busca_rep(recorreA[0],"lista2","lista3","lista3","lista3")
            if my_resultA > 0:
                rcoop_copacred=rcoop_copacred-1
                my_resultA=0
                                    
        if recorreA in lista4 :
            rcoop_coopadct+=1
            my_resultA = busca_rep(recorreA[0],"lista2","lista4","lista4","lista4")
            if my_resultA > 0:
                rcoop_coopadct=rcoop_coopadct-1
                my_resultA=0
            
        if recorreA in lista5 :
            rcoop_copacen+=1
            my_resultA = busca_rep(recorreA[0],"lista2","lista5","lista5","lista5")
            if my_resultA > 0:
                rcoop_copacen=rcoop_copacen-1
                my_resultA=0        
                
        #if recorreA in lista1 and recorreA in lista5 :
        #    rcoop_caviptr_copacen+=1     
        #    my_resultA = busca_rep(recorreA[0],"lista2","lista5","lista1","lista1","lista1")
        #    if my_resultA > 0:
        #        rcoop_caviptr_copacen=rcoop_caviptr_copacen-1
        #        my_resultA=0
        
        #if recorreA in lista1 and recorreA in lista4 :        
        #    rcoop_caviptr_coopadct+=1
        #    my_resultA = busca_rep(recorreA[0],"lista2","lista4","lista1","lista1","lista1")
        #    if my_resultA > 0:
        #        rcoop_caviptr_coopadct=rcoop_caviptr_coopadct-1
        #        my_resultA=0
                
        if recorreA in lista3 and recorreA in lista5 :          
            rcoop_copacred_copacen+=1
            my_resultA = busca_rep(recorreA[0],"lista2","lista5","lista3","lista3")
            if my_resultA > 0:
                rcoop_copacred_copacen=rcoop_copacred_copacen-1
                my_resultA=0
                
        if recorreA in lista3 and recorreA in lista4 :          
            rcoop_copacred_coopadct+=1
            my_resultA = busca_rep(recorreA[0],"lista2","lista4","lista3","lista3")
            if my_resultA > 0:
                rcoop_copacred_coopadct=rcoop_copacred_coopadct-1
                my_resultA=0
                
        if recorreA in lista5 and recorreA in lista4 :         
            rcoop_copacen_coopadct+=1
            my_resultA = busca_rep(recorreA[0],"lista2","lista4","lista5","lista5")
            if my_resultA > 0:
                rcoop_copacen_coopadct=rcoop_copacen_coopadct-1
                my_resultA=0
                                                
        #if recorreA in lista1 and recorreA in lista3 and recorreA in lista5 :          
        #    rcoop_caviptr_copacred_copacen+=1
        #    my_resultA = busca_rep(recorreA[0],"lista2","lista1","lista3","lista5","lista5")
        #    if my_resultA > 0:
        #        rcoop_caviptr_copacred_copacen=rcoop_caviptr_copacred_copacen-1
        #        my_resultA=0
                
        #if recorreA in lista1 and recorreA in lista3 and recorreA in lista4 :         
        #    rcoop_caviptr_copacred_coopadct+=1
        #    my_resultA = busca_rep(recorreA[0],"lista2","lista3","lista1","lista4","lista4")
        #    if my_resultA > 0:
        #        rcoop_caviptr_copacred_coopadct=rcoop_caviptr_copacred_coopadct-1
        #        my_resultA=0
                
        #if recorreA in lista1 and recorreA in lista5 and recorreA in lista4 :         
        #    rcoop_caviptr_copacen_coopadct+=1
        #    my_resultA = busca_rep(recorreA[0],"lista2","lista1","lista5","lista4","lista4")
        #    if my_resultA > 0:
        #        rcoop_caviptr_copacen_coopadct=rcoop_caviptr_copacen_coopadct-1
        #        my_resultA=0
                
        if recorreA in lista3 and recorreA in lista5 and recorreA in lista4 :         
            rcoop_copacred_copacen_coopadct+=1
            my_resultA = busca_rep(recorreA[0],"lista2","lista3","lista5","lista4")
            if my_resultA > 0:
                rcoop_copacred_copacen_coopadct=rcoop_copacred_copacen_coopadct-1
                my_resultA=0
                
        #if recorreA in lista1 and recorreA in lista3 and recorreA in lista5 and recorreA in lista4 :          
        #    rcoop_caviptr_copacred_copacen_coopadct
        #    my_resultA = busca_rep(recorreA[0],"lista2","lista1","lista3","lista5","lista4")
        #    if my_resultA > 0:
        #        rcoop_caviptr_copacred_copacen_coopadct=rcoop_caviptr_copacred_copacen_coopadct-1
        #        my_resultA=0

    # Asignación de variables de procesos anteriores
    #rcoop_caviptr = rcavip_cooptr
    #rcoop_caviptr_copacred = rcavip_copacred_cooptr
    
    rep1_coop = 0
    #rep1_coop = rcoop_caviptr + rcoop_copacred + rcoop_coopadct + rcoop_copacen
    rep1_coop = rcoop_copacred + rcoop_coopadct + rcoop_copacen
    #rep1_coop = rep1_coop + rcoop_caviptr_copacred + rcoop_caviptr_copacen + rcoop_caviptr_coopadct    
    rep1_coop = rep1_coop + rcoop_copacred_copacen + rcoop_copacred_coopadct + rcoop_copacen_coopadct
    #rep1_coop = rep1_coop + rcoop_caviptr_copacred_copacen + rcoop_caviptr_copacred_coopadct
    #rep1_coop = rep1_coop + rcoop_caviptr_copacen_coopadct + rcoop_copacred_copacen_coopadct
    rep1_coop = rep1_coop + rcoop_copacred_copacen_coopadct
    #rep1_coop = rep1_coop + rcoop_caviptr_copacred_copacen_coopadct
    Stot_Coop = tot_coop - rep1_coop

#COPACREDITO
    for recorreA in lista3:
                                    
        if recorreA in lista4 :
            rcopac_coopadct+=1
            my_resultA = busca_rep(recorreA[0],"lista3","lista4","lista4","lista4")
            if my_resultA > 0:
                rcopac_coopadct=rcopac_coopadct-1
                my_resultA=0
            
        if recorreA in lista5 :
            rcopac_copacen+=1
            my_resultA = busca_rep(recorreA[0],"lista3","lista5","lista5","lista5")
            if my_resultA > 0:
                rcopac_copacen=rcopac_copacen-1
                my_resultA=0    

        #if recorreA in lista2 and recorreA in lista1 :
        #    rcopac_caviptr_cooptr+=1
        #    my_resultA = busca_rep(recorreA[0],"lista3","lista1","lista2","lista2","lista2")
        #    if my_resultA > 0:
        #        rcopac_caviptr_cooptr=rcopac_caviptr_cooptr-1           
        #        my_resultA=0
                
        #if recorreA in lista1 and recorreA in lista5 :
        #    rcopac_caviptr_copacen+=1     
        #    my_resultA = busca_rep(recorreA[0],"lista3","lista5","lista1","lista1","lista1")
        #    if my_resultA > 0:
        #        rcopac_caviptr_copacen=rcopac_caviptr_copacen-1    
        #        my_resultA=0
        
        #if recorreA in lista1 and recorreA in lista4 :
        #    rcopac_caviptr_coopadct+=1
        #    my_resultA = busca_rep(recorreA[0],"lista3","lista4","lista1","lista1","lista1")
        #    if my_resultA > 0:
        #        rcopac_caviptr_coopadct=rcopac_caviptr_coopadct-1
        #        my_resultA=0
                
        if recorreA in lista2 and recorreA in lista5 :
            rcopac_cooptr_copacen+=1
            my_resultA = busca_rep(recorreA[0],"lista3","lista5","lista2","lista2")
            if my_resultA > 0:
                rcopac_cooptr_copacen=rcopac_cooptr_copacen-1
                my_resultA=0
                
        if recorreA in lista2 and recorreA in lista4 :   
            rcopac_cooptr_coopadct+=1
            my_resultA = busca_rep(recorreA[0],"lista3","lista4","lista2","lista2")
            if my_resultA > 0:
                rcopac_cooptr_coopadct=rcopac_cooptr_coopadct-1
                my_resultA=0
                
        if recorreA in lista5 and recorreA in lista4 :
            rcopac_copacen_coopadct+=1
            my_resultA = busca_rep(recorreA[0],"lista3","lista4","lista5","lista5")
            if my_resultA > 0:
                rcopac_copacen_coopadct=rcopac_copacen_coopadct-1
                my_resultA=0
                                                
        #if recorreA in lista1 and recorreA in lista2 and recorreA in lista5 :     
        #    rcopac_caviptr_cooptr_copacen+=1
        #     my_resultA = busca_rep(recorreA[0],"lista3","lista1","lista2","lista5","lista5")
        #    if my_resultA > 0:
        #        rcopac_caviptr_cooptr_copacen=rcopac_caviptr_cooptr_copacen-1
        #        my_resultA=0
            
        #if recorreA in lista1 and recorreA in lista2 and recorreA in lista4 :         
        #    rcopac_caviptr_cooptr_coopadct+=1
        #    my_resultA = busca_rep(recorreA[0],"lista3","lista2","lista1","lista4","lista4")
        #    if my_resultA > 0:
        #        rcopac_caviptr_cooptr_coopadct=rcopac_caviptr_cooptr_coopadct-1
        #        my_resultA=0
                
        #if recorreA in lista1 and recorreA in lista5 and recorreA in lista4 :         
        #    rcopac_caviptr_copacen_coopadct+=1  
        #    my_resultA = busca_rep(recorreA[0],"lista3","lista1","lista5","lista4","lista4")
        #    if my_resultA > 0:
        #        rcopac_caviptr_copacen_coopadct=rcopac_caviptr_copacen_coopadct-1
        #        my_resultA=0
                
        if recorreA in lista2 and recorreA in lista5 and recorreA in lista4 :         
            rcopac_cooptr_copacen_coopadct+=1
            my_resultA = busca_rep(recorreA[0],"lista3","lista2","lista5","lista4")
            if my_resultA > 0:
                rcopac_cooptr_copacen_coopadct=rcopac_cooptr_copacen_coopadct-1
                my_resultA=0
                
        #if recorreA in lista1 and recorreA in lista2 and recorreA in lista5 and recorreA in lista4 :          
        #    rcopac_caviptr_cooptr_copacen_coopadct
        #    my_resultA = busca_rep(recorreA[0],"lista3","lista1","lista2","lista5","lista4")
        #    if my_resultA > 0:
        #        rcopac_caviptr_cooptr_copacen_coopadct=rcopac_caviptr_cooptr_copacen_coopadct-1
        #        my_resultA=0

    # Asignación de variables de procesos anteriores
    # rcopac_caviptr = rcavip_copacred
    rcopac_cooptr = rcoop_copacred

    rep1_copac = 0
    #rep1_copac = rcopac_caviptr + rcopac_cooptr + rcopac_copacen + rcopac_coopadct
    rep1_copac = rcopac_cooptr + rcopac_copacen + rcopac_coopadct
    #rep1_copac = rep1_copac + rcopac_caviptr_cooptr + rcopac_caviptr_copacen + rcopac_caviptr_coopadct
    rep1_copac = rep1_copac + rcopac_cooptr_copacen + rcopac_cooptr_coopadct + rcopac_copacen_coopadct
    #rep1_copac = rep1_copac + rcopac_caviptr_cooptr_copacen + rcopac_caviptr_cooptr_coopadct    
    #rep1_copac = rep1_copac + rcopac_caviptr_copacen_coopadct + rcopac_cooptr_copacen_coopadct
    rep1_copac = rep1_copac + rcopac_cooptr_copacen_coopadct
    #rep1_copac = rep1_copac + rcopac_caviptr_cooptr_copacen_coopadct
    Stot_Copac = tot_copac - rep1_copac

#COOPADUCTOS
    for recorreA in lista4:
        if recorreA in lista5 :
            rcoopdc_copacen+=1
            my_resultA = busca_repk(recorreA[0],"lista4","lista5","lista5","lista5","lista5")
            if my_resultA > 0:
                rcoopdc_copacen=rcoopdc_copacen-1
                my_resultA=0

    # Asignación de variables de procesos anteriores usados en éste para mejorar el tiempo de procesamiento
    #rcoopdc_caviptr = rcavip_coopadct
    rcoopdc_cooptr = rcoop_coopadct
    # rcoopdc_copacen = Ésta variable SI la estoy calculando en el for anterior
    rcoopdc_copacred = rcopac_coopadct
    #rcoopdc_caviptr_cooptr = rcoop_caviptr_coopadct
    #rcoopdc_caviptr_copacen = rcavip_copacen_coopadct
    #rcoopdc_caviptr_copacred = rcopac_caviptr_coopadct
    rcoopdc_cooptr_copacen = rcoop_copacen_coopadct
    rcoopdc_cooptr_copacred = rcopac_cooptr_coopadct
    rcoopdc_copacen_copacred = rcopac_copacen_coopadct
    #rcoopdc_caviptr_cooptr_copacen = rcoop_caviptr_copacen_coopadct
    #rcoopdc_caviptr_cooptr_copacred = rcopac_caviptr_cooptr_coopadct
    #rcoopdc_caviptr_copacen_copacred = rcopac_caviptr_copacen_coopadct
    rcoopdc_cooptr_copacen_copacred = rcopac_cooptr_copacen_coopadct
    #rcoopdc_caviptr_cooptr_copacen_copacred = rcopac_caviptr_cooptr_copacen_coopadct

    #rep1_coopdc = rcoopdc_caviptr + rcoopdc_cooptr + rcoopdc_copacen + rcoopdc_copacred
    rep1_coopdc = rcoopdc_cooptr + rcoopdc_copacen + rcoopdc_copacred

    #rep1_coopdc = rep1_coopdc + rcoopdc_caviptr_cooptr + rcoopdc_caviptr_copacen + rcoopdc_caviptr_copacred    

    rep1_coopdc = rep1_coopdc + rcoopdc_cooptr_copacen + rcoopdc_cooptr_copacred + rcoopdc_copacen_copacred
    
    #rep1_coopdc = rep1_coopdc + rcoopdc_caviptr_cooptr_copacen + rcoopdc_caviptr_cooptr_copacred    

    #rep1_coopdc = rep1_coopdc + rcoopdc_caviptr_copacen_copacred + rcoopdc_cooptr_copacen_copacred
    rep1_coopdc = rep1_coopdc + rcoopdc_cooptr_copacen_copacred

    #rep1_coopdc = rep1_coopdc + rcoopdc_caviptr_cooptr_copacen_copacred    

    Stot_Coopdc = tot_coopdc - rep1_coopdc

#COPACENTRO

    # Asignación de variables de procesos anteriores usados en éste para mejorar el tiempo de procesamiento
    #rcpctro_caviptr = rcavip_copacen
    rcpctro_cooptr = rcoop_copacen
    rcpctro_copacred = rcopac_copacen
    rcpctro_coopadct = rcoopdc_copacen
    #rcpctro_caviptr_cooptr = rcoop_caviptr_copacen
    #rcpctro_caviptr_copacred = rcavip_copacred_copacen
    #rcpctro_caviptr_coopadct = rcoopdc_caviptr_copacen
    rcpctro_cooptr_copacred = rcoop_copacred_copacen
    rcpctro_cooptr_coopadct = rcoopdc_cooptr_copacen
    rcpctro_copacred_coopadct = rcoopdc_copacen_copacred
    #rcpctro_caviptr_cooptr_copacred = rcavip_copacred_cooptr_copacen
    #rcpctro_caviptr_cooptr_coopadct = rcoopdc_caviptr_cooptr_copacen
    #rcpctro_caviptr_copacred_coopadct = rcoopdc_caviptr_copacen_copacred
    rcpctro_cooptr_copacred_coopadct = rcoopdc_cooptr_copacen_copacred
    #rcpctro_caviptr_cooptr_copacred_coopadct = rcavip_copacred_cooptr_copacen_coopadct
    
    #rep1_coptro = rcpctro_caviptr + rcpctro_cooptr + rcpctro_copacred + rcpctro_coopadct
    rep1_coptro = rcpctro_cooptr + rcpctro_copacred + rcpctro_coopadct
    #rep1_coptro = rep1_coptro + rcpctro_caviptr_cooptr + rcpctro_caviptr_copacred + rcpctro_caviptr_coopadct
    rep1_coptro = rep1_coptro + rcpctro_cooptr_copacred + rcpctro_cooptr_coopadct + rcpctro_copacred_coopadct
    #rep1_coptro = rep1_coptro + rcpctro_caviptr_cooptr_copacred + rcpctro_caviptr_cooptr_coopadct
    #rep1_coptro = rep1_coptro + rcpctro_caviptr_copacred_coopadct + rcpctro_cooptr_copacred_coopadct
    rep1_coptro = rep1_coptro + rcpctro_cooptr_copacred_coopadct
    #rep1_coptro = rep1_coptro + rcpctro_caviptr_cooptr_copacred_coopadct
    Stot_Coptro = tot_coptro - rep1_coptro

# Precios discriminados para Detalle de Asociadas por cada cooperativa versus las otras

    # CAVIPETROL :

    #subTot1 = vr_uni * Stot_Cavip
    #subTot2 = (vr_uni / 2) * rcavip_copacred
    #subTot3 = (vr_uni / 2) * rcavip_cooptr  # sirve para Coopetrol también
    #subTot4 = (vr_uni / 2) * rcavip_copacen
    #subTot5 = (vr_uni / 2) * rcavip_coopadct
    #subTot6 = (vr_uni / 3) * rcavip_copacred_cooptr # sirve para Coopetrol también
    #subTot7 = (vr_uni / 3) * rcavip_copacred_copacen
    #subTot8 = (vr_uni / 3) * rcavip_copacred_coopadct
    #subTot9 = (vr_uni / 3) * rcavip_cooptr_copacen # sirve para Coopetrol también
    #subTot10 = (vr_uni / 3) * rcavip_cooptr_coopadct # sirve para Coopetrol también
    #subTot11 = (vr_uni / 3) * rcavip_copacen_coopadct
    #subTot12 = (vr_uni / 4) * rcavip_copacred_cooptr_copacen  # sirve para Coopetrol también
    #subTot13 = (vr_uni / 4) * rcavip_copacred_cooptr_coopadct  # sirve para Coopetrol también
    #subTot14 = (vr_uni / 4) * rcavip_copacred_copacen_coopadct
    #subTot15 = (vr_uni / 4) * rcavip_cooptr_copacen_coopadct  # sirve para Coopetrol también
    #subTot16 = (vr_uni / 5) * rcavip_copacred_cooptr_copacen_coopadct  # sirve para Coopetrol también

    #subTotCavip = subTot1 + subTot2 + subTot3 + subTot4 + subTot5 + subTot6 + subTot7 + subTot8 + subTot9 + subTot10
    #subTotCavip = subTotCavip + subTot11 + subTot12 + subTot13 + subTot14 + subTot15 + subTot16

    subTot1=0
    subTot3=0
    subTot6=0
    subTot9=0 
    subTot10=0 
    subTot12=0
    subTot13=0
    subTot15=0
    subTot16=0
    subTot2=0
    subTot7=0
    subTot8 = 0
    subTot5=0
    subTot14=0
    subTot11=0
    subTot4=0
    subTotCavip = 0

    # COOPETROL :

    subTot17 = vr_uni * Stot_Coop
    subTot18 = (vr_uni / 2) * rcoop_copacred
    subTot19 = (vr_uni / 2) * rcoop_copacen
    subTot20 = (vr_uni / 2) * rcoop_coopadct
    subTot21 = (vr_uni / 3) * rcoop_copacred_copacen
    subTot22 = (vr_uni / 3) * rcoop_copacred_coopadct
    subTot23 = (vr_uni / 3) * rcoop_copacen_coopadct  
    subTot24 = (vr_uni / 4) * rcoop_copacred_copacen_coopadct
    
    subTotCoop = subTot17 + subTot3 + subTot18 + subTot19 + subTot20 + subTot21 + subTot6 + subTot9 + subTot10 + subTot22
    subTotCoop = subTotCoop + subTot23 + subTot12 + subTot13 + subTot15 + subTot24 + subTot16

    # COPACREDITO :    

    subTot25 = vr_uni * Stot_Copac
    subTot26 = subTot2
    subTot27 = (vr_uni / 2) * rcopac_cooptr
    subTot28 = (vr_uni / 2) * rcopac_copacen
    subTot29 = (vr_uni / 2) * rcopac_coopadct
    subTot30 = subTot6
    subTot31 = subTot7
    subTot32 = subTot8    
    subTot33 = (vr_uni / 3) * rcopac_cooptr_copacen
    subTot34 = (vr_uni / 3) * rcopac_cooptr_coopadct
    subTot35 = (vr_uni / 3) * rcopac_copacen_coopadct    
    #subTot36 = (vr_uni / 4) * rcopac_caviptr_cooptr_copacen
    #subTot37 = (vr_uni / 4) * rcopac_caviptr_cooptr_coopadct
    subTot38 = subTot14
    subTot39 = (vr_uni / 4) * rcopac_cooptr_copacen_coopadct
    #subTot40 = (vr_uni / 5) * rcopac_caviptr_cooptr_copacen_coopadct

    subTotCopac = subTot25 + subTot26 + subTot27 + subTot28 + subTot29 + subTot30 + subTot31 + subTot32 + subTot33
    #subTotCopac = subTotCopac + subTot34 + subTot35 + subTot36 + subTot37 + subTot38 + subTot39 + subTot40
    subTotCopac = subTotCopac + subTot34 + subTot35 + subTot38 + subTot39

    # Precios Discriminados COOPADUCTOS :

    subTot41 = vr_uni * Stot_Coopdc
    subTot42 = subTot5   # rcoopdc_caviptr  (No olvidar documentar ésta línea para no quedar loco con los subtotales)
    subTot43 = subTot20  # rcoop_coopadct
    subTot44 = subTot29  # rcopac_coopadct
    subTot45 = (vr_uni / 2) * rcoopdc_copacen  #  rcoopdc_copacen
    subTot46 = subTot10 # rcavip_cooptr_coopadct
    subTot47 = subTot11 # rcavip_copacen_coopadct
    subTot48 = subTot8  # rcoopdc_caviptr_copacred
    subTot49 = subTot23 # rcoopdc_cooptr_copacen
    subTot50 = subTot34 # rcoopdc_cooptr_copacred
    subTot51 = subTot35 # rcoopdc_copacen_copacred
    subTot52 = subTot15 # rcoopdc_caviptr_cooptr_copacen
    #subTot53 = subTot37 # rcoopdc_caviptr_cooptr_copacred
    subTot54 = subTot14 # rcoopdc_caviptr_copacen_copacred
    subTot55 = subTot39 # rcoopdc_cooptr_copacen_copacred
    subTot56 = subTot16 # rcoopdc_caviptr_cooptr_copacen_copacred

    subTotCoopad = subTot41 + subTot42 + subTot43 + subTot44 + subTot45 + subTot46 + subTot47 + subTot48 + subTot49
    #subTotCoopad = subTotCoopad + subTot50 + subTot51 + subTot52 + subTot53 + subTot54 + subTot55 + subTot56
    subTotCoopad = subTotCoopad + subTot50 + subTot51 + subTot52 + subTot54 + subTot55 + subTot56
    
    # Precios Discriminados COPACENTRO :

    subTot57 = vr_uni * Stot_Coptro
    subTot58 = subTot4  # rcpctro_caviptr = rcavip_copacen
    subTot59 = subTot19 # rcpctro_cooptr = rcoop_copacen
    subTot60 = subTot28 # rcpctro_copacred = rcopac_copacen
    subTot61 = subTot45 # rcpctro_coopadct = rcoopdc_copacen
    subTot62 = subTot9 # rcpctro_caviptr_cooptr = rcavip_cooptr_copacen
    subTot63 = subTot7 # rcpctro_caviptr_copacred = rcavip_copacred_copacen
    subTot64 = subTot11 # rcpctro_caviptr_coopadct = rcavip_copacen_coopadct
    subTot65 = subTot21 # rcpctro_cooptr_copacred = rcoop_copacred_copacen
    subTot66 = subTot23 # rcpctro_cooptr_coopadct = rcoop_copacen_coopadct
    subTot67 = subTot35 # rcpctro_copacred_coopadct = rcopac_copacen_coopadct
    subTot68 = subTot12 # rcpctro_caviptr_cooptr_copacred = rcavip_copacred_cooptr_copacen
    subTot69 = subTot15 # rcpctro_caviptr_cooptr_coopadct = rcavip_cooptr_copacen_coopadct
    subTot70 = subTot14 # rcpctro_caviptr_copacred_coopadct = rcavip_copacred_copacen_coopadct
    subTot71 = subTot24 # rcpctro_cooptr_copacred_coopadct = rcoop_copacred_copacen_coopadct
    subTot72 = subTot16 # rcpctro_caviptr_cooptr_copacred_coopadct = rcavip_copacred_cooptr_copacen_coopadct

    subTotCoptro = subTot57 + subTot58 + subTot59 + subTot60 + subTot61 + subTot62 + subTot63 + subTot64 + subTot72
    subTotCoptro = subTotCoptro + subTot65 + subTot66 + subTot67 + subTot68 + subTot69 + subTot70 + subTot71

# Resumen de las variables hacia la pagina html son pa'l html = Ph

    #return render_template('detalle.html', Phrcavip_cooptr=rcavip_cooptr, Phrcavip_copacred=rcavip_copacred,
    return render_template('detalle.html', ValUni=vr_uni, FecUni=fch_uni, PhsubTot1 = subTot1, PhsubTot2 = subTot2, PhsubTot3 = subTot3,
    #Phrcavip_coopadct=rcavip_coopadct, Phrcavip_copacen=rcavip_copacen, Phrcavip_copacred_cooptr=rcavip_copacred_cooptr,
    #Phrcavip_copacred_copacen=rcavip_copacred_copacen, Phrcavip_copacred_coopadct=rcavip_copacred_coopadct,
    #Phrcavip_cooptr_copacen=rcavip_cooptr_copacen, Phrcavip_cooptr_coopadct=rcavip_cooptr_coopadct,    
    #Phrcavip_copacen_coopadct=rcavip_copacen_coopadct, Phrcavip_copacred_cooptr_copacen=rcavip_copacred_cooptr_copacen,    
    #Phrcavip_copacred_cooptr_coopadct=rcavip_copacred_cooptr_coopadct, Phrcavip_copacred_copacen_coopadct=rcavip_copacred_copacen_coopadct,    
    #Phrcavip_cooptr_copacen_coopadct=rcavip_cooptr_copacen_coopadct, Phrcavip_copacred_cooptr_copacen_coopadct=rcavip_copacred_cooptr_copacen_coopadct,    
    #ValUni=vr_uni, FecUni=fch_uni, Phtot_cavip=tot_cavip, PhStot_Cavip=Stot_Cavip, PhsubTot1 = subTot1, PhsubTot2 = subTot2, PhsubTot3 = subTot3,
    PhsubTot4 = subTot4, PhsubTot5 = subTot5, PhsubTot6 = subTot6, PhsubTot7 = subTot7, PhsubTot8 = subTot8, PhsubTot9 = subTot9, PhsubTot10 = subTot10,
    PhsubTot11 = subTot11, PhsubTot12 = subTot12, PhsubTot13 = subTot13, PhsubTot14 = subTot14, PhsubTot15 = subTot15, PhsubTot16 = subTot16,
    PhsubTotCavip = subTotCavip, Phrcoop_copacred=rcoop_copacred, Phrcoop_coopadct = rcoop_coopadct,
    #Phrcoop_caviptr=rcoop_caviptr, Phrcoop_copacred=rcoop_copacred, Phrcoop_coopadct = rcoop_coopadct,
    Phrcoop_copacen=rcoop_copacen, Phrcoop_copacen_coopadct = rcoop_copacen_coopadct, 
    #Phrcoop_copacen=rcoop_copacen, Phrcoop_caviptr_copacred = rcoop_caviptr_copacred, Phrcoop_caviptr_copacen = rcoop_caviptr_copacen,
    #Phrcoop_caviptr_coopadct = rcoop_caviptr_coopadct, Phrcoop_copacen_coopadct = rcoop_copacen_coopadct,
    Phrcoop_copacred_copacen = rcoop_copacred_copacen, Phrcoop_copacred_coopadct = rcoop_copacred_coopadct, 
    #Phrcoop_caviptr_copacred_copacen = rcoop_caviptr_copacred_copacen, Phrcoop_caviptr_copacred_coopadct = rcoop_caviptr_copacred_coopadct, 
    #Phrcoop_caviptr_copacred_coopadct = rcoop_caviptr_copacred_coopadct, 
    #Phrcoop_caviptr_copacen_coopadct = rcoop_caviptr_copacen_coopadct, Phrcoop_copacred_copacen_coopadct = rcoop_copacred_copacen_coopadct,
    Phrcoop_copacred_copacen_coopadct = rcoop_copacred_copacen_coopadct,
    #Phrcoop_caviptr_copacred_copacen_coopadct = rcoop_caviptr_copacred_copacen_coopadct, Phtot_coop = tot_coop, PhStot_Coop=Stot_Coop,
    Phtot_coop = tot_coop, PhStot_Coop=Stot_Coop, PhsubTot23=subTot23, PhsubTot24=subTot24,    
    PhsubTot18=subTot18, PhsubTot19=subTot19, PhsubTot20=subTot20, PhsubTot21=subTot21, PhsubTot22=subTot22, PhsubTotCoop = subTotCoop,
    

    #Phrcopac_caviptr=rcopac_caviptr, Phrcopac_cooptr=rcopac_cooptr, Phrcopac_copacen=rcopac_copacen,
    Phrcopac_cooptr=rcopac_cooptr, Phrcopac_copacen=rcopac_copacen,
    #Phrcopac_coopadct=rcopac_coopadct, Phrcopac_caviptr_cooptr=rcopac_caviptr_cooptr, Phrcopac_caviptr_copacen=rcopac_caviptr_copacen,
    Phrcopac_coopadct=rcopac_coopadct,
    #Phrcopac_caviptr_coopadct=rcopac_caviptr_coopadct, Phrcopac_cooptr_copacen=rcopac_cooptr_copacen,
    Phrcopac_cooptr_copacen=rcopac_cooptr_copacen,
    Phrcopac_cooptr_coopadct=rcopac_cooptr_coopadct, Phrcopac_copacen_coopadct=rcopac_copacen_coopadct,
    #Phrcopac_caviptr_cooptr_copacen=rcopac_caviptr_cooptr_copacen, Phrcopac_caviptr_cooptr_coopadct=rcopac_caviptr_cooptr_coopadct,    
    #Phrcopac_caviptr_copacen_coopadct=rcopac_caviptr_copacen_coopadct, Phrcopac_cooptr_copacen_coopadct=rcopac_cooptr_copacen_coopadct,
    Phrcopac_cooptr_copacen_coopadct=rcopac_cooptr_copacen_coopadct,
    #Phrcopac_caviptr_cooptr_copacen_coopadct=rcopac_caviptr_cooptr_copacen_coopadct, Phtot_copac=tot_copac, PhStot_Copac=Stot_Copac,
    Phtot_copac=tot_copac, PhStot_Copac=Stot_Copac,    
    PhsubTot25=subTot25, PhsubTot26=subTot26, PhsubTot27=subTot27, PhsubTot28=subTot28, PhsubTot29=subTot29, PhsubTot30=subTot30,
    PhsubTot31=subTot31, PhsubTot32=subTot32, PhsubTot33=subTot33, PhsubTot34=subTot34, PhsubTot35=subTot35,
    #PhsubTot31=subTot31, PhsubTot32=subTot32, PhsubTot33=subTot33, PhsubTot34=subTot34, PhsubTot35=subTot35, PhsubTot36=subTot36,
    #PhsubTot37=subTot37, PhsubTot38=subTot38, PhsubTot39=subTot39, PhsubTot40=subTot40, PhsubTotCopac = subTotCopac,
    PhsubTot38=subTot38, PhsubTot39=subTot39, PhsubTotCopac = subTotCopac,    
    #Phrcoopdc_caviptr=rcoopdc_caviptr, Phrcoopdc_cooptr=rcoopdc_cooptr, Phrcoopdc_copacen=rcoopdc_copacen, Phrcoopdc_copacred=rcoopdc_copacred,
    Phrcoopdc_cooptr=rcoopdc_cooptr, Phrcoopdc_copacen=rcoopdc_copacen, Phrcoopdc_copacred=rcoopdc_copacred,
    #Phrcoopdc_caviptr=rcoopdc_caviptr, Phrcoopdc_cooptr=rcoopdc_cooptr, Phrcoopdc_copacen=rcoopdc_copacen, Phrcoopdc_copacred=rcoopdc_copacred,    
    #Phrcoopdc_caviptr_cooptr=rcoopdc_caviptr_cooptr, Phrcoopdc_caviptr_copacen=rcoopdc_caviptr_copacen, Phrcoopdc_caviptr_copacred=rcoopdc_caviptr_copacred,    

    Phrcoopdc_cooptr_copacen=rcoopdc_cooptr_copacen, Phrcoopdc_cooptr_copacred=rcoopdc_cooptr_copacred, Phrcoopdc_copacen_copacred=rcoopdc_copacen_copacred,
    #Phrcoopdc_caviptr_cooptr_copacen = rcoopdc_caviptr_cooptr_copacen, Phrcoopdc_caviptr_cooptr_copacred=rcoopdc_caviptr_cooptr_copacred,    
    #Phrcoopdc_caviptr_copacen_copacred=rcoopdc_caviptr_copacen_copacred, Phrcoopdc_cooptr_copacen_copacred=rcoopdc_cooptr_copacen_copacred,
    Phrcoopdc_cooptr_copacen_copacred=rcoopdc_cooptr_copacen_copacred,    
    #Phrcoopdc_caviptr_cooptr_copacen_copacred=rcoopdc_caviptr_cooptr_copacen_copacred, Phtot_coopdc=tot_coopdc, PhStot_Coopdc=Stot_Coopdc,
    Phtot_coopdc=tot_coopdc, PhStot_Coopdc=Stot_Coopdc,
    PhsubTot41=subTot41, PhsubTot42=subTot42, PhsubTot43=subTot43, PhsubTot44=subTot44, PhsubTot45=subTot45, PhsubTot46=subTot46,
    PhsubTot47=subTot47, PhsubTot48=subTot48, PhsubTot49=subTot49, PhsubTot50 = subTot50, PhsubTot51=subTot51, PhsubTot52=subTot52,
    #PhsubTot53=subTot53, PhsubTot54=subTot54, PhsubTot55=subTot55, PhsubTot56=subTot56, PhsubTotCoopad=subTotCoopad,
    PhsubTot54=subTot54, PhsubTot55=subTot55, PhsubTot56=subTot56, PhsubTotCoopad=subTotCoopad,
    
    #Phrcpctro_caviptr=rcpctro_caviptr, Phrcpctro_cooptr=rcpctro_cooptr, Phrcpctro_copacred=rcpctro_copacred, Phrcpctro_coopadct=rcpctro_coopadct,
    Phrcpctro_cooptr=rcpctro_cooptr, Phrcpctro_copacred=rcpctro_copacred, Phrcpctro_coopadct=rcpctro_coopadct,
    #Phrcpctro_caviptr_cooptr=rcpctro_caviptr_cooptr, Phrcpctro_caviptr_copacred=rcpctro_caviptr_copacred, Phrcpctro_caviptr_coopadct=rcpctro_caviptr_coopadct,     
    Phrcpctro_cooptr_copacred=rcpctro_cooptr_copacred, Phrcpctro_cooptr_coopadct=rcpctro_cooptr_coopadct, Phrcpctro_copacred_coopadct=rcpctro_copacred_coopadct,
    #Phrcpctro_caviptr_cooptr_copacred=rcpctro_caviptr_cooptr_copacred, Phrcpctro_caviptr_cooptr_coopadct=rcpctro_caviptr_cooptr_coopadct,    
    #Phrcpctro_caviptr_copacred_coopadct=rcpctro_caviptr_copacred_coopadct, Phrcpctro_cooptr_copacred_coopadct=rcpctro_cooptr_copacred_coopadct,
    Phrcpctro_cooptr_copacred_coopadct=rcpctro_cooptr_copacred_coopadct, Phtot_coptro=tot_coptro, PhStot_Coptro=Stot_Coptro,
    #Phrcpctro_caviptr_cooptr_copacred_coopadct=rcpctro_caviptr_cooptr_copacred_coopadct, Phtot_coptro=tot_coptro, PhStot_Coptro=Stot_Coptro,    
    PhsubTot57=subTot57, PhsubTot58=subTot58, PhsubTot59=subTot59, PhsubTot60=subTot60, PhsubTot61=subTot61, PhsubTot62=subTot62, PhsubTot63=subTot63,
    PhsubTot64=subTot64, PhsubTot65=subTot65, PhsubTot66=subTot66, PhsubTot67=subTot67, PhsubTot68=subTot68, PhsubTot69=subTot69, PhsubTot70=subTot70, PhsubTot71=subTot71,
    PhsubTot72=subTot72, PhsubTotCoptro=subTotCoptro)
 
#COTIZADOR
@app.route('/cotizador')
def cotizador():    
    #cur = mysql.connection.cursor()
    #cur.execute('SELECT * FROM archivos_coop')
    #data = cur.fetchall()        

    #return render_template('cruces.html', cont=data, cruc=datas)

    # Query general para los parentescos :
    curparent = mysql.connection.cursor()
    curparent.execute('SELECT * FROM parentescos order by nom_parent')
    dataparent = curparent.fetchall()

    return render_template('cotizador.html', losfami=dataparent)

@app.route('/exit')
def exit():    
    exit
    return render_template('index.html')

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        culoeperro = request.form['fullname']        
        phone = request.form['phone']
        email = request.form['email']        
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (fullname_con, telefono_con, email_con) VALUES (%s, %s, %s)',
        (culoeperro, phone, email))
        mysql.connection.commit()
        flash('Contacto agregado')
        return redirect(url_for('Index'))        

@app.route('/edit/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id_con = %s', (id))
    data = cur.fetchall()
    return render_template('edit-contact.html', contact = data[0])    

@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        culoeperro = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute(""" 
                UPDATE contacts 
                SET fullname_con = %s, 
                telefono_con = %s,
                email_con = %s                
            WHERE id_con = %s
        """, (culoeperro, phone, email, id ))
        mysql.connection.commit()
        flash('Contacto actualizado')
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id_con = {0}'.format(id))
    mysql.connection.commit()
    flash('Contacto eliminado satisfactoriamente')
    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(port=3000,debug=True)