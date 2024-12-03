# Tehisintellekt-ChatGPT-API
### **a. Kuidas rakendust käivitada**
1. Veenduge, et [Docker](https://www.docker.com/products/docker-desktop/) on paigaldatud.
2. Ehitage Docker image:<br>
`docker-compose build`
3. Looge `.env` fail näidise `.env.template` järgi, ning kleepige sinna API võti.
4. Käivitage rakendus Docker Compose abil:<br>
`docker-compose up -d`
5. Rakendus on saadaval aadressil: http://127.0.0.1:8000
6. Testide käivitamiseks:<br>
`docker-compose exec fastapi_app pytest`

### **b. Rakenduse tööpõhimõte**
Rakendus kasutab OpenAI GPT mudelit, et vastata küsimustele ettevõtte veebilehelt kogutud sisu põhjal. API-l on kaks endpointi:
1. **/source_info (GET)**: Tagastab veebilehelt kogutud andmed. 
2. **/ask (POST)**: Võtab vastu kasutaja küsimuse ja tagastab asjakohase vastuse, mille ChatGPT genereerib kogutud andmete põhjal.
Rakendus kasutab FastAPI raamistikku ning integreerub OpenAI API-ga vastuste genereerimiseks. BeautifulSoup-i kasutatakse veebilehe sisu kogumiseks, requests tegeleb HTTP päringutega ning regex-i abil puhastatakse kogutud teksti veidi.

### **c. Kasutatud teegid**
- **openai**: See teek teeb OpenAI-ga suhtlemise lihtsaks.
- **pydantic**: Kasutatakse andmete valideerimiseks, ja selle rakenduse puhul GPT vastuse mudeli struktureerimiseks.
- **BeautifulSoup**: Lihtne teek veebi scrape-miseks ja HTML-i sisu töötlemiseks.
- **requests**: Populaarne HTTP teek, mis pakub lihtsat viisi veebipäringute tegemiseks.
- **pytest**: Kerge ja paindlik testimisraamistik, aitab hõlpsasti teste luua.
- **python-dotenv**: Võimaldab mugavalt ja turvaliselt laadida API-võtme .env failist, hoides sellest koodist väljaspool, et vältida võtme lekkimist.

### **d. Täiendused, et rakendus oleks production ready**
Oletades, et production ready rakendus on pidevalt töös, võiks veebilehe crawl-imine olla dünaamilisem, uuendades pages_data andmeid regulaarselt näiteks mingi kindla aja tagant. Hetkel on andmed staatilised rakenduse käivitamise ajal loetud andmete põhjal. Veel võiks täiendada:
- **Logimine**: Rakendada struktureeritud logimine, et jälgida arakenduse tööd ja vigu.
- **Vigade käsitlemine**: Parandada veakäsitlust, lisades mitmekesisemaid HTTP response erinevatele exceptionitele.
- **Turvalisus**: Rakendada turvalisuse tavasid, nagu rate limiting, sisendi valideerimine ja kaitset injection rünnakute vastu. 
- **Testimine**: Rohkem ühikteste, et katta rohkem äärejuhtumeid. Testis paksid hõlmama ka jõudlust ning kõiki eelmainitud aspekte (logimine, veakäsitlus, turvalisus).

### **e. Kuidas ehitada üles CI/CD pipeline sellele rakendusele**
CI/CD pipeline tagab, et muudatused koodibaasis saavad automaatselt testitud, integrereitud ja deploy-tud. 

1. **Versioonihaldus:** Kasutada GitHubi versioonihalduseks ja käivitada CI/CD töövood iga commit-i või pull request-i puhul.
2. **Testimine:** Seadistada automatiseeritud ühiktestid GitHub Actionsiga. 
3. **Docker Image-i ehitamine** Kasutada CI pipeline'i, et ehitada ja laadida Docker Image konteinerite registrisse, näiteks Docker Hubi või Azure Container Registry-sse.
4. **Deploymine:** Kasutada CD tööriistu nagu GitHub Actions, et deployda uusim Docker Image testkeskkonda lõplikuks kontrolliks. Pärast kinnitamist viia muudatused üle production keskkonda.

### **f. Kuidas püstitada rakendus Azure pilvekeskkonnas**
Kuigi mul pole otsest kogemust Azure'iga, siis minu uurimise ja arusaamise põhjal, läheneksin sellele niimoodi:
1. Ressursigrupp ja konteineri register  
- Luua ressursigrupp, et hallata kõiki vajalike ressursse (App Service, Container registry).
- Luua Azure Container Registry, et üles laadida rakenduse Docker Image.
2. Azure App Service
- Kasutada Azure App Service'i, mis toetab konteineripõhiseid rakendusi.
- Konfigureerida App Service, et see tõmbaks Docker Image konteineri registrist.
