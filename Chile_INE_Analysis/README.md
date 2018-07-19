<h1> Analisis de la situacion laboral en Chile</h1>
<h2> Concepto y critérios de medicón</h2>
El siguiente esquema conceptual, muestra las grandes categorías en que se clasifica la población, para fines del análisis de la condición laboral. La Nueva Encuesta Nacional de Empleo se aplica a todas las personas de 15 años o más, las cuales constituyen la población en edad de trabajar (PET) en Chile. Las personas a quienes se aplica el cuestionario, pueden quedar clasificadas como ocupadas, desocupadas o inactivas, categorías mutuamente excluyentes.
<img src="ine_concepto.png">
<h2> Dataset</h2>
El dataset utilizado en este trabajo será primariamente dados (raw data) obtenidos desde la base de datos de la "Encuesta Nacional de Empleo (ENE)", desarrollada por el INE (Instituto Nacional de Estatisticas - Chile):
<p>
  http://www.ine.cl/estadisticas/laborales/ene/base-de-datos
  </p>
Los Datos originales están en formato proprietário SPSS (.SAV)
<h3> Conversión</h3>
La base de datos deberá ser convertida al formato libre .CSV para, a partir de entonces ser trabajada en el projeto utilizando Python.
<br>
Para la conversion de los datos se utilisará la libreria en "R" "Foreign", la cual possue la función "read.spss" para leitura y conversion de los datos a .csv, como muestra el ejemplo abajo:
<pre>
library(foreign)
fileNameIn = "ENE_2018_01_DEF.sav"
fileNameout = "ENE_2018_01_DEF.csv"
write.table (read.spss (fileNameIn), file = fileNameout, quote = FALSE, sep = ",")
</pre>
El Jupyter Notebook utilizado para la conversion puede ser encontrado abajo:
https://github.com/Mjrovai/Python4DS/blob/master/Chile_INE_Analysis/Coverting%20SAV%20to%20CSV%20using%20R.ipynb
<h2>Librerias</h2>
<h3> Principales librerias Python a seren utilizadas en el trabajo:</h3>
<pre>
Pandas
NumPy
MatPlotLib
</pre>
