Napovedovanje oglasov za prikaz uporabnikom, s ciljem povečati CTR (click-through ratio)

Leon Premk, Mario Balukčič, Domen Rok Brunček

1.4.2019

Na sejmu podjetij na FRI-ju smo se povezali s firmo iProm, ki so nam zagotovili podatke o uporabnikih in oglasih,
ki jih prikazujejo. Zaradi GDPR-ja so vsi uporabniki predstavljeni z enoličnimi ID-ji. Zaupali so nam, da na dan
dobijo 100GB podatkov, kar bi bil za nas problem, saj bi za procesiranje potrebovali vrhunsko strojno opremo. Iz
njihovih podatkov so nam zato dali reprezentativni vzorec, s katerim lahko delamo. Kljub temu je podatkov za
procesiranje preveč, zato smo jih moral razredčiti in odstraniti atribute, ki nam ne pomagajo. Prav tako smo izločili
vse uporabnike, ki še nikoli niso kliknili na oglas, saj je velika verjetnost, da nikoli tudi ne bodo, za to pa obstajajo
razlogi, kot je npr. ad blocker.

Naš glavni cilj je napovedati katere oglase prikazati uporabniku, da bi zagotovili čim večji CTR. 

Uporabnike bomo predstavili, kot vektorje, katerih komponente so njihovi interesi, na podlagi katerih bomo uporabnike
razdelili v gruče. Glavni atributi, s katerimi bomo delali so SiteCategory, UserID, AdID, MasterSiteID, AdIndustry, 
Views, Clicks. Na vprašanje katero metodo za gručenje bomo uporabili bomo odgovorili s testiranjem. S prečnim preverjanjem
bomo za različne metode gručenja preverili, katera nas bo privedla do najvišjega CTR-ja. 

Naš cilj je CTR čim bolj približati 1%, torej 1 klik na 100 prikazov oglasov, kar so nam na podjetju zaupali, da je 
precej optimalna rešitev naše naloge. 

</br>Format

Podatki so razdeljeni na več datotek glede na datum. Stolpci z vrednostnimi so ločeni s tabulatorjem.

Atributi

1 Date - datum v formatu <leto>-<mesec>-<dan>
  
2 DayOfWeek - dan v tednu od 0=ponedeljek do 6=nedelja

3 TimeFrame - časovni izsek dneva - dan je razdeljen na 6 kosov po 4 ure, vrednost je indeks od 0 do 5

4 UserID - ID uporabnika

5 SiteID - ID obiskane spletne strani

6 CampaignID - ID akcije kateri pripada oglas

7 AdID - ID oglasa

8 ZoneID - ID cone v kateri se je oglas prikazal

9 MasterSiteID - ID medija

10 SiteCategory - ID kategorije spletne strani, ni definiran za vse

11 AdIndustry - ID panoge oglasa/akcije, ni definiran za vse

12 Requests - število poslanih zahtevkov za prikaz oglasa

13 Views - število, ki predstavlja koliko krat je uporabnik videl oglas (vsaj 50% površine oglasa v vidnem polju za vsaj 1 sekundo)

14 Clicks - število, ki predstavlja koliko krat je uporabnik kliknil na oglas

</br>Panoge oglasa/akcije

Vrednosti stolpca »AdIndustry«.

0 *Manjkajoč podatek

1 Avtomobilizem

2 Kozmetika

3 Zdravje

4 Dom

5 Gospodinjstvo

6 Hrana&Pijaca

7 Moda

8 Informacijska tehnologija

9 Zabava&prosti cas

10 Telekomunikacije

11 Finance

12 Izobraževanje

13 Storitve

14 Turizem

15 Ostalo

16 Nepremičnine

17 Trgovina

18 Šport

21 Test

22 Test

</br>Kategorije spletne strani

Vrednosti stolpca »SiteCategory«.

0 *Manjkajoč podatek

1 Arts & Entertainment

2 Avtomobilizem

3 Business

4 Mlade družine

5 Zdravje

6 Kulinarika

7 Hobbies & Interests

8 Dom in Vrt

9 Novice

10 Sports

11 Style & Fashion

12 Technology & Computing

13 Travel

14 Nepremičnine

15 Careers

16 Education

17 Law Govt & Politics

18 Personal Finance

19 Society

20 Science

21 Pets

22 Shopping

23 Religion and Spirituality

24 Uncategorized

25 Non Standard Content

26 Illegal Content

1000 Aktivni športniki

1001 Šport

1002 Mladi in Najmlajši

1003 Gospodarstvo in Posel

1004 Lifestyle/Trendi

1005 iTech & Mobile & Foto

1006 Turizem

1007 Prosti čas

1008 Test

1009 Test

1010 zavarovalnistvo
