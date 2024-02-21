import webbrowser
import pandas as pd
from flask import Flask
app = Flask(__name__)
RESULT_PORT=5500

def open_html_file(file_path):
    try:
        webbrowser.open(file_path)
    except Exception as e:
        print(f"Error: {e}")


@app.route('/')
def results():
    try:
        with open('finalreport.html', 'r') as file:
            contents = file.read()
            print("read worked")
            return contents
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return f"An error occurred: {e}"

def run_flask_app():
    app.run(host='0.0.0.0',port=RESULT_PORT)


def showgui():
     start2="""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Number of Users Vs Response Times</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
        }

        header {
            background-color: #333;
            color: #fff;
            text-align: center;
            padding: 1rem;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }

        .image-container {
            text-align: center;
            margin: 20px 0;
        }

        .image-container img {
            max-width: 100%;
        }

        .table-container {
            margin: 0 auto;
            border-collapse: collapse;
            width: 100%;
            max-width: 100%;
        }

        .styled-table {
            border-collapse: collapse;
            font-size: 1.5em;
            font-family: sans-serif;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
        }
        .styled-table thead tr {
            background-color: #009879;
            color: #ffffff;
            text-align: center;
        }
        .styled-table th,
        .styled-table td {
            padding: 12px 15px;
            text-align: center;
        }
        .styled-table tbody tr {
            border-bottom: 1px solid #dddddd;
        }
        
        .styled-table tbody tr:nth-of-type(even) {
            background-color: #f3f3f3;
        }
        
        .styled-table tbody tr:last-of-type {
            border-bottom: 2px solid #009879;
        }
        .styled-table tbody tr.active-row {
            font-weight: bold;
            color: #009879;
        }
    </style>
</head>
<body>
    <header>
        <h1>Consolidated Results</h1>
    </header>
""" 
    # <div class="container">                   
     res="testreport.csv"
     df = pd.read_csv(res)
     toprow=list(df.head())
    #  for row in df.itertuples(index=False):
    #     heading.append(row[0])
    #  print(heading)
     heading="""<h1 style="min-width:100%;text-align: center;">"""+"Final comparison Report"+"</h1>"
     temp=""" <div class="table-container">"""+heading+"""<table class="styled-table" style="min-width: 100%;">
                <thead>
                    <tr>"""
     for top in toprow:
         temp=temp+"<th>"+top+"</th>"
     temp=temp+"""</tr>
                </thead>
                <tbody>"""
     for row in df.itertuples(index=False):
             s="<tr>"
             for it in row:
                 s=s+"<td>"+str(it)+"</td>"
             s=s+"</tr>"
             temp=temp+s
     temp=temp+"""</tbody>
            </table> 
        </div>"""
     start2=start2+temp
    #  </div>
     end2= """
    </body>
    </html>"""         
     start2=start2+end2
    # saving the html file
     file_html = open("finalreport.html", "w")
     file_html.write(start2)
     file_html.close()
     print("file write completed")
     html_file_path = 'finalreport.html'
     run_flask_app()