import streamlit as st
import pandas as pd
import base64
import pip
pip.main(["install","selenium"])
#pip.main(["import","selenium"])
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import locale
import time
from datetime import datetime

# Establecer la configuración regional a una que utilice el inglés
locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')

st.title('Scraping Web')

# Agrega un espacio para que el usuario ingrese la dirección web
url = st.text_input('Ingrese la dirección web que desea raspar', 'https://fucn.instructure.com/courses')

curso = st.text_input('Ingrese el nombre y codigo del curso', 'ALGEBRA LINEAL-B2A_27106012-3134')

# Agrega un selector de fecha para la fecha de corte
y = st.date_input('Fecha de inicio del bloque: ', value=datetime(2023, 9, 25))

x = st.date_input('Fecha de corte para generar la alerta de inactividad:', value=datetime(2023, 11, 14))#value=datetime.now())#st.text_input('Fecha de corte para generar la alerta: ', 'dd-m-yyyy-hh-mm')

# Agrega un espacio para que el usuario ingrese el código
user_email = st.text_input('correo electrónico ucn', '@ucn.edu.co')

# Agrega un espacio para que el usuario ingrese el código
user_code = st.text_input('Ingrese la contraseña de acceso', '', type='password')

if st.button('Raspar datos'):
    # Aquí puedes colocar el código para raspar datos de la dirección web ingresadas

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')

    # Crea el controlador de Chrome
    driver = webdriver.Chrome(options=chrome_options)

    # Abre la URL ingresada por el usuario
    driver.get(url)

    driver.maximize_window()

    main_page = driver.current_window_handle

    #user = 'mfsegurag@ucn.edu.co'
    #key =  1037586447

    time.sleep(5)

    try:
        ## Casillas para ingreso de credenciales
        input_user = driver.find_element(By.XPATH, '//input[@name="pseudonym_session[unique_id]"]')
        input_pass = driver.find_element("xpath",'//input[@name="pseudonym_session[password]"]')
        ## Se envian las credenciales
        input_user.send_keys(user_email)
        input_pass.send_keys(user_code)
        ## Boton de login
        boton = driver.find_element("xpath",'//*[@id="login_form"]/div[3]/div[2]/input')
        ## click on a button
        boton.click()

        ## Fecha de inicio del Bloque
        ## Pasamos la fecha al formato adecuado
        fecha_inicio = y#datetime.strptime(y,'%d-%b-%Y-%H-%M')
        ## Definimos la fecha de corte para el último ingreso, ejemplo de formato: '02-may-2022-00-00'
        ## Pasamos la fecha al formato adecuado
        fecha_corte = x#datetime.strptime(x,'%d-%b-%Y-%H-%M')
        ## Definimos el dataFrame de almacenamiento temporal de los reportados
        df_i = pd.DataFrame(columns=['Nombre',
                                     'Email',
                                     'Usuario',
                                     'SIS',
                                     'Curso',
                                     'Fecha_reporte',
                                     'Último_acceso',
                                     'Actividad_total'
                                    ])
        ## Inicia recorrido por los diferentes cursos
        #curso = 'Curso Prueba MAYCOL FELIPE SEGURA GARCIA'
        ## Entramos al curso
        #//*[@id="nav-tray-portal"]/span/span/div/div/div/div/div/ul[1]/li[1]/a
        Tabla_cursos = driver.find_element("xpath",f'//tbody//tr/td/a[@title="{curso}"]')
        Tabla_cursos.click()
        ## Tiempo de espera
        time.sleep(2)
        ## Entramos a la sección personas
        boton_users = driver.find_element("xpath",'//nav//ul[@id="section-tabs"]//li/a[@class="people"]')
        boton_users.click()
        ## Tiempo de espera
        time.sleep(5)
        ## Hacemos scroll para que se cargue todo el codigo de la plataforma
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        ## Almacenamos el codigo de la pagina que contiene los datos de interes
        #matches = driver.find_elements_by_css_selector('tr')
        matches = driver.find_elements(By.CSS_SELECTOR, 'tr')
        ## Seleccionamos el texto y lo almacenamos en una lista. Cada elemento de la lista corresponde con
        ## la data de un estudiante
        all_matches = [match.text for match in matches]   
        # Organizamos la información en DataFrame
        Nombre = []
        Email = []
        Usuario = []
        SIS = []
        Curso = []
        Fecha_reporte = []
        Último_acceso = []
        Actividad_total = []
        #Observacion = []
        for i in range(1,len(all_matches)):
            #l = all_matches[i]
            ## Separamos los datos de cada estudiante en lista con el string '\n'
            #l=l.split('\n')
            #try:
            Nombre.append(matches[i].find_elements(By.CSS_SELECTOR,'td')[1].text)
            email = matches[i].find_elements(By.CSS_SELECTOR,'td')[2].text
            # Seleccionamos email 
            Email.append(email)
            # extraemos el usuario del Email
            Usuario.append(email[:email.find('@')])
            # Seleccionamos el nombre del curso
            Curso.append(matches[i].find_elements(By.CSS_SELECTOR,'td')[4].text)
            # Fecha del reporte
            Fecha_reporte.append(datetime.today())
            # Extraemos solo numeros
            SIS.append(matches[i].find_elements(By.CSS_SELECTOR,'td')[3].text)
            if len(matches[i].find_elements(By.CSS_SELECTOR,'td')[6].text) != 0:
                Último_acceso.append(matches[i].find_elements(By.CSS_SELECTOR,'td')[6].text)
            else:
                Último_acceso.append('25 de sep en 23:59')

            if len(matches[i].find_elements(By.CSS_SELECTOR,'td')[7].text) != 0:
                Actividad_total.append(matches[i].find_elements(By.CSS_SELECTOR,'td')[7].text)
            else:
                Actividad_total.append(0)
        
        # Creamos Data Frame   
        df = pd.DataFrame({'Nombre': Nombre,'Email': Email, 'Usuario': Usuario, 'SIS': SIS, 'Curso': Curso,
                           'Fecha_reporte': Fecha_reporte, 'Último_acceso':Último_acceso,
                           'Actividad_total':Actividad_total#,
                           #'Observacion': Observacion
                          })
        
        def ajustar_formato_fecha(fecha_str):
            # Dividir la cadena de fecha y hora
            fecha_hora = fecha_str.split('-')

            # Asegurar que la hora tenga dos dígitos
            fecha_hora[-2] = fecha_hora[-2].zfill(2)

            # Unir de nuevo la cadena de fecha y hora
            fecha_ajustada = '-'.join(fecha_hora)

            return fecha_ajustada
        
        #try:
        # Adecuamos string de fecha a formato adecuado para su transformación 
        df['Último_acceso'] = df['Último_acceso'].apply(lambda x: 
                                            x.replace('en ','2023 '))
        df['Último_acceso'] = df['Último_acceso'].apply(lambda x: 
                                            x.replace('de ',''))
        df['Último_acceso'] = df['Último_acceso'].apply(lambda x: 
                                            x.replace(' ','-'))
        df['Último_acceso'] = df['Último_acceso'].apply(lambda x: 
                                            x.replace(':','-'))
        df['Último_acceso'] = df['Último_acceso'].apply(lambda x: 
                                            x.replace('mayo','may'))
        df['Último_acceso'] = df['Último_acceso'].apply(lambda x: 
                                            x.replace('abr','apr'))
        df['Último_acceso'] = df['Último_acceso'].apply(lambda x: 
                                            x.replace('ago','aug'))
        df['Último_acceso'] = df['Último_acceso'].apply(lambda x: 
                                            x.replace('nov','nov'))
        # Imprime los valores antes y después de la conversión
        #st.write("Valores antes de la conversión:")
        #st.write(df['Último_acceso'])
        # Pasamos a formato de fecha
        df['Último_acceso'] = df['Último_acceso'].apply(ajustar_formato_fecha)
        df['Último_acceso'] =  df['Último_acceso'].apply(lambda x: datetime.strptime(x,'%d-%b-%Y-%H-%M'))
        #st.write("Valores después de la conversión:")
        #st.write(df['Último_acceso'])
       
        #except:
        #    pass
        #st.write(f'Hasta acá ok {datetime.today()}')

        driver.quit()
        df['Inactividad'] = [(df.Fecha_reporte[i]-df.Último_acceso[i]).days for i in range(df.shape[0])]
        
        df_inactivos = df.loc[df.Último_acceso < pd.to_datetime(fecha_corte),:]
        df_inactivos.info()
        st.write(df_inactivos)
    except Exception as e:
        st.error(f"Error al encontrar el elemento: {e}")

    time.sleep(2)

    # Cierra el controlador al final del raspado
    #driver.quit()

    # Ejemplo de cómo imprimir la dirección web ingresada
    st.write(f'Ha ingresado la siguiente dirección web: {url}')