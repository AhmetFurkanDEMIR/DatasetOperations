from flask import render_template, Flask, flash, request
import os
from datetime import datetime
from werkzeug.utils import secure_filename
import pandas as pd
import webbrowser
import operations

# pandas dataframe (data)
global CSVFile

# siteye giren kullaniclari ayirmak icin tutugum uniq deger
global dt_string

# veri uzerinde ki islemler
global deger 

deger= ["Mean", "Median", "Mode", "Frequency", "Interquartile range value (IQR)", "Outliers", "Five number summary", "Box Chart", "Variance and standard deviation"]
degerColumn = ["Not", "%30", "%40", "%50", "%60", "%70", "%80", "%90", "%95", "%98"]
degerLine = ["Not", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "15+"]
degerDoldurma = ["Not", "Mean", "Mode" , "Median"]

# kullanicilari ayirmak icin giriş zamanlarini tuttum
now = datetime.now()
dt_string = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')

# Flask app
app = Flask(__name__)
app.config['UPLOAD_EXTENSIONS'] = ['.csv']
app.config['UPLOAD_PATH'] = 'static/uploads'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# main page
@app.route("/",methods = ['GET', 'POST'])
def main():

    return render_template("index.html", rss=degerColumn, rssa=degerLine, rssaa=degerDoldurma)


# veri seti ve yapilacak doldurma silme yontemlerini kullanicidan aldigim sayfa
@app.route("/dataset",methods = ['GET', 'POST'])
def DatasetOpen():

    if request.method == "POST":

        # Veri setini server 'a upload ettim
        global CSVFile
        CSVFile = request.files['fileCSV']
        CSVFileName = secure_filename(CSVFile.filename)

        # kullanicinin eksik doldurma sorunu icin kontroller
        if CSVFileName == "" or CSVFileName == " ":

            flash("Please select a Data Set (.csv file).")
            return render_template("index.html", rss=degerColumn, rssa=degerLine, rssaa=degerDoldurma)

        elif len(CSVFileName.split(".")) == 2:

            if CSVFileName.split(".")[1]!="csv":

                flash("Please make sure that the dataset you selected is a .csv file.")
                return render_template("index.html", rss=degerColumn, rssa=degerLine, rssaa=degerDoldurma)

        try:

            CSVFile.save(os.path.join(app.config['UPLOAD_PATH'], "{}.csv".format(dt_string)))
            CSVFile = pd.read_csv(os.path.join(app.config['UPLOAD_PATH'], "{}.csv".format(dt_string)))
            os.system("rm {}".format(os.path.join(app.config['UPLOAD_PATH'], "{}.csv".format(dt_string))))

        except:

            flash("Incorrect dataset, please make sure your dataset is OK (you can check your dataset by opening it with LibreOffice).")
            return render_template("index.html", rss=degerColumn, rssa=degerLine, rssaa=degerDoldurma)

        # sutun bazli silme, satir bazli silme ve doldurma yontemleri
        columnOperation = request.form["column"]
        rawOperation = request.form["row"]
        methodsOperation = request.form["methods"]
        CSVFile = operations.DatasetOperations(CSVFile, columnOperation, rawOperation, methodsOperation)

        # veri setinin tam halini ayri bir sayfa da gosterdim
        tabName = "http://localhost:5000/{}".format(dt_string)
        webbrowser.open_new_tab(tabName)

        return render_template("/dataset.html", rss=deger)

    else:

        return render_template("/dataset.html", rss=deger)


# kullanicinin veri seti uzerinde yapacagi islemler burdan alinir ve bu sayfada ekrana bastirilir
@app.route("/datasetFinal",methods = ['GET', 'POST'])
def DatasetFinal():

    if request.method == "POST":

        global CSVFile
        global deger

        # yapilacak islem
        operationHTML = request.form["operations"]

        # eger resim var ise html de gosterilir
        img = "None"

        # tablo var ise html de gosterilir
        tableFlag = "None"
        dicta = {}        

        if str(operationHTML) == "Mean":

            dicta, CSVFile, deger = operations.Mean(dicta, CSVFile, deger)
            tableFlag = "True"
            

        elif str(operationHTML) == "Median":

            dicta, CSVFile, deger = operations.Median(dicta, CSVFile, deger)
            tableFlag = "True"


        elif str(operationHTML) == "Mode":

            dicta, CSVFile, deger = operations.Mode(dicta, CSVFile, deger)
            tableFlag = "True"

        elif str(operationHTML) == "Frequency":

            dicta, img, CSVFile, deger = operations.Frequency(dicta, CSVFile, deger, dt_string)
            tableFlag = "True"

        elif str(operationHTML) == "Interquartile range value (IQR)":

            dicta, CSVFile, deger = operations.IQR(dicta, CSVFile, deger)
            tableFlag = "True"


        elif str(operationHTML) == "Outliers":

            dicta, CSVFile, deger = operations.Outliers(dicta, CSVFile, deger)
            tableFlag = "True"

        elif str(operationHTML) == "Five number summary":

            dicta, CSVFile, deger = operations.FiveNumber(dicta, CSVFile, deger)
            tableFlag = "True"

        elif str(operationHTML) == "Variance and standard deviation":

            dicta, CSVFile, deger = operations.VarianceStandardDeviation(dicta, CSVFile, deger)
            tableFlag = "True"

        elif str(operationHTML) == "Box Chart":

            img, CSVFile, deger = operations.BoxChart(CSVFile, deger, dt_string)
            tableFlag = "None"


        df = pd.DataFrame(dicta)

        tables=[df.to_html(classes='table table-striped text-center', justify='center')]

        return render_template("/datasetOperation.html",tables=tables, rss=deger, img=img, tableFlag=tableFlag)

    else:

        return render_template("/dataset.html", rss=deger)



# veriyi ayri bir sayfa da gorsellestirmek
@app.route("/{}".format(dt_string))
def viewData():

    image = open("static/images/demiraiPNG.txt", "r", encoding="UTF-8")
    image = image.read()

    html = """


<!DOCTYPE html>

<html lang="en">
<head>

    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
    <title>demir.ai - Dataset</title>

</head>
<body>

    <nav class="navbar navbar-expand-md navbar-dark bg-dark mb-4">
    <a class="navbar-brand" href="/">Home</a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarCollapse">
      <ul class="navbar-nav mr-auto"> 
      </ul>
      <ul class="navbar-nav ml-auto">
        <li class="nav-item active">

            <a class="nav-link" href="/About">About App<span class="sr-only">(current)</span></a>

        </li>
      </ul>
    </div>
  </nav>

    <div class = "container">


    <div class = "text-center">

        <p><font face="tahoma" size="5" color="darkslategray">
        <b>Dataset Review</b></font></p>

        <pre>&nbsp;</pre>

        {}

    </div>
    </div>

    <pre>&nbsp;</pre>


    <script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>

</body>
</html>

<footer class="bg-dark text-center text-white">
  <!-- Grid container -->
  <div class="container p-4 pb-0">
    
    <div align="center"><img src="{}" ></div>

  </div>
  <!-- Grid container -->

  <!-- Copyright -->
  <div class="text-center p-3" style="background-color: rgba(0, 0, 0, 0.2);">
    © 2021 Copyright:
    <a class="text-white" href="https://www.ahmetfurkandemir.com/">ahmetfurkandemir.com</a>
  </div>
  <!-- Copyright -->
</footer>

""".format(CSVFile.to_html(header="true", table_id="table",classes='table table-striped text-center', justify='center'),image)


    return html

# hakkimda
@app.route("/About")
def About():

    return render_template("/about.html")


if __name__ == "__main__":

    app.run(debug=True, host='localhost')