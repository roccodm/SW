import os

records={}


cmd = os.popen ("git log --before='2022-05-01 00:00' --after='2022-03-31 23:59' --author-date-order --pretty=format:'%H|%ad|%an|%ae|%s'")
out = cmd.read()
for line in out.splitlines():
    entries = line.split("|")
    records[entries[0]]={}
    records[entries[0]]["date"]=entries[1]
    records[entries[0]]["author"]=entries[2]
    records[entries[0]]["email"]=entries[3]
    records[entries[0]]["description"]=entries[4]

for record in records:
    cmd = os.popen("git show --stat "+record+" |tail -n +7")
    records[record]["stats"]=cmd.read()
    cmd = os.popen("git show -c "+record+" |tail -n +7")
    records[record]["diff"]=cmd.read()

html = """
<html lang="en">
<head>
  <meta charset="utf-8">

  <title>Rendiconto attività lavoro agile</title>
  <meta name="description" content="Rendiconto analitico attività svolte in regime di smart working">
  <meta name="author" content="Rocco De Marco">
  <style type="text/css">
  BODY {font-family: sans-serif; font-size: 12pt;}

  .header {border: solid black 1px; background: #eee;}
  .riepilogo .commit {}
  .titolo {font-size: 24pt; font-weight: bold;}  
  
  
  </style>
</head>

<body>



"""

print (html)

print ("<div class='riepilogo'><div class='titolo'>Riepilogo sintetico</div>")
for record in reversed(records):
    print ("<div class='header'>")
    print ("<div class='commit'>Commit: <b>"+record+"</b></div>")
    print ("<div class='data'> Data: "+records[record]["date"]+"</div>")
    print ("<div class='author'> Autore: "+records[record]["author"]+"</div>")
    print ("<div class='email'> Email: "+records[record]["email"]+"</div>")
    print ("<div class='description'> Descrizione: "+records[record]["description"]+"</div></div>")
    
    print ("<div class='stats'><pre>")
    print (records[record]["stats"])
    print ("</pre></div></div>")

print ("<div class='dettaglio'><div class='titolo'>Dettaglio attività svolta</div>")
for record in reversed(records):
    print ("<div class='header'>")
    print ("<div class='commit'>Commit: <b>"+record+"</b></div>")
    print ("<div class='data'> Data: "+records[record]["date"]+"</div>")
    print ("<div class='author'> Autore: "+records[record]["author"]+"</div>")
    print ("<div class='email'> Email: "+records[record]["email"]+"</div>")
    print ("<div class='description'> Descrizione modifica: "+records[record]["description"]+"</div></div>")
    
    print ("<div class='diff'><pre>")
    print (records[record]["diff"])
    print ("</pre></div></div>")

    

