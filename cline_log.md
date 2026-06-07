# Darba žurnāls

## Solis 1 — Datu ielāde un priekšskatījums
**Prompts:** "Create a file app.py in the project root. This is a Streamlit
app for a chocolate sales dashboard. For now, it should only do three things:
set page config, load CSV from data/chocolate_sales.csv with a cached
load_data() function, and display the first 10 rows plus the total row count.
Also create requirements.txt with streamlit and pandas."

**Rezultāts:** Cline izveidoja app.py ar lapas konfigurāciju, kešotu datu
ielādes funkciju load_data() un datu priekšskatījumu (pirmās 10 rindas +
kopējais rindu skaits). Izveidots arī requirements.txt.

## Solis 2 — Interaktīvie filtri
**Prompts:** "Update app.py to add two interactive filters in the Streamlit
sidebar: a date range filter (two date inputs defaulting to min/max dates)
and a Country category filter (multiselect). Convert the Date column to
datetime. Create a filtered_data DataFrame and update the preview table and
row count to use it."

**Rezultāts:** Cline pievienoja sānjoslu ar diviem filtriem — datuma
diapazona filtru un valstu (Country) izvēles filtru. Date kolonna pārvērsta
par datetime tipu. Izveidots filtered_data, un datu priekšskatījums tagad
rāda filtrētos datus.

**Papildinājums:** Pēc palaišanas radās ValueError — CSV datumi bija formātā
diena/mēnesis/gads. Labots, pievienojot dayfirst=True pie pd.to_datetime().

## Solis 3 — Vizualizācijas
**Prompts:** "Update app.py to add three Plotly charts using filtered_data:
a line chart of revenue over time (grouped by month), a horizontal bar chart
of top 10 products by revenue, and a pie chart of revenue share by country.
Display each with st.plotly_chart and a subheader. Add plotly to
requirements.txt."

**Rezultāts:** Cline pievienoja trīs Plotly grafikus — līniju grafiku
(ieņēmumi pa mēnešiem), horizontālu stabiņu diagrammu (top 10 produkti) un
pīrāga diagrammu (ieņēmumu sadalījums pa valstīm). Visi grafiki izmanto
filtrētos datus. Pievienots plotly requirements.txt failam.

**Papildinājums:** Grafiki nestrādāja — TypeError ar nlargest. Iemesls: Amount
kolonna CSV failā bija teksts ($ zīmes un komati). Cline salaboja load_data()
funkciju, iztīrot $ un komatus un pārvēršot Amount par skaitli ar
pd.to_numeric().

## Solis 4 — Datu kopas maiņa
**Prompts:** "We are switching the dashboard to a new dataset (coffee
sales at data/index_1.csv). Update load_data() to read the new file, convert
the date column, and rename columns (date->Date, money->Amount,
coffee_name->Product) plus add a Category column, so the rest of the app
keeps working unchanged. Update the dashboard title to 'Coffee Sales
Dashboard'."

**Iemesls:** Sākotnējā šokolādes pārdošanas datu kopa pēc pārbaudes izrādījās
nederīga — dati bija mākslīgi dublēti (katra mēneša darījumu skaits identiski
atkārtojās visos trīs gados: janvāris vienmēr 61, februāris 37 utt.). Uz
šādiem datiem nav iespējams atbilstoši veikt laika tendenču analīzi vai
prognozēšanu. Tāpēc datu kopa tika nomainīta uz kafijas pārdošanas
datiem (index_1.csv) ar 13 nepārtrauktiem mēnešiem un dabīgi svārstīgiem
datiem.

**Rezultāts:** Cline pārslēdza aplikāciju uz kafijas datu kopu.
load_data() funkcija tagad nolasa jauno failu un pārsauc kolonnas, tāpēc
filtri, grafiki un prognoze turpina strādāt bez izmaiņām. Nomainīts arī
dashboard nosaukums.

**Papildinājums 1:** Pēc datu kopas nomaiņas filtrs un pīrāga grafiks joprojām
lietoja nosaukumu "Country", kura jaunajā failā nav. Cline pielāgoja
sānjoslas filtru un pīrāga grafiku, lai tie lieto "Category" kolonnu.
Sakārtota load_data() funkcija un noņemta DEBUG rinda.

**Papildinājums 2:** Pēc palaišanas radās AttributeError — load_data() funkcija
datuma kolonnu apstrādāja divreiz nepareizā secībā, kā rezultātā Date kolonnā
nonāca teksts datumu vietā. Labots, sakārtojot funkciju pareizā secībā:
vispirms pārsaucot kolonnas, tad pārvēršot Date par datetime tipu.

## Solis 5 — Bonuss: ieņēmumu prognoze
**Prompts:** "Add a simple revenue forecast feature to app.py. Group
filtered_data by month, apply scikit-learn LinearRegression to predict next
month's revenue. Display the prediction with st.metric and show the R-squared
score. Handle edge cases for too little data. Add scikit-learn to
requirements.txt."

**Rezultāts:** Cline pievienoja prognozes sekciju, kas ar lineāro regresiju
(scikit-learn) novērtē nākamā mēneša ieņēmumus, balstoties uz mēneša
pārdošanas tendenci. Parādīts gan prognozētais skaitlis (st.metric), gan R²
rādītājs, kas parāda, cik labi taisnā līnija sader ar datiem. Pievienoti
brīdinājumi gadījumiem ar nepietiekamiem datiem. Pievienots scikit-learn
requirements.txt failam.

## Solis 6 — Papildu: MI ģenerēts datu kopsavilkums
**Prompts:** "Add an AI-generated summary section to app.py with a 'Generate
AI Summary' button. Compute key statistics from filtered_data, build a
prompt, send it to the OpenRouter API (free model) using the requests
library and an API key from st.secrets, and display the returned summary.
Use a spinner and wrap the call in try/except for error handling. Add
requests to requirements.txt."

**Rezultāts:** Cline pievienoja MI kopsavilkuma sekciju. Poga aprēķina
galvenos rādītājus no filtrētajiem datiem, nosūta tos OpenRouter API un
parāda modeļa ģenerētu teksta kopsavilkumu. API atslēga tiek lasīta no
Streamlit secrets. Pievienota kļūdu apstrāde gadījumiem, kad API izsaukums
neizdodas.

**Papildinājums 1:** Cline ievietoja MI kopsavilkuma sekciju faila sākumā, kā
rezultātā radās kļūda "filtered_data is not defined" (kods lietoja mainīgo,
kas tiek izveidots tikai zemāk). Sekcija pārvietota uz faila beigām, lai tā
izpildītos pēc datu filtrēšanas.

**Papildinājums 2:** MI kopsavilkums atgrieza 404 kļūdu — Cline norādītais bezmaksas
modeļa nosaukums vairs nebija pieejams OpenRouter platformā. Labots, nomainot
modeli uz "openrouter/free" — automātisku maršrutētāju, kas pats izvēlas
pieejamu bezmaksas modeli, tāpēc kods nav atkarīgs no konkrēta modeļa
nosaukuma.

## Solis 7 — Projekta struktūras sakārtošana
**Prompts:** "Refactor app.py to use a utils package. Move the load_data()
function into a new file utils/data_loader.py (importing streamlit and
pandas there), create utils/__init__.py, and import load_data into app.py
from the utils package. The app must work exactly the same."

**Rezultāts:** Cline pārstrukturēja projektu — datu ielādes funkcija load_data()
pārvietota uz atsevišķu failu utils/data_loader.py, izveidots utils pakotnes
fails. app.py tagad importē funkciju no utils, kas padara galveno failu
tīrāku un atbilst standarta projekta struktūrai.
