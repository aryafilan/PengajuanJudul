from flask import Flask, render_template, request
import pandas as pd
import numpy as np

app = Flask(__name__)
app.debug=True

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        judul = request.form['text'].strip()
        
        if judul.strip()=="":
          print(judul)
          return render_template('home.html', analisis=False)
        
        df = pd.read_excel('file/data.xlsx')
        df['Kemiripan'] = df['Judul'].apply(lambda x: Jarak_Levenshtein_Kata(judul, x))
        df['Skor'] = df['Judul'].apply(lambda x: skor(judul, x))
        df = df.sort_values(by=['Kemiripan'], ascending=False)
        df["No."] = np.arange(1, len(df)+1)
        kolom = df.columns.tolist()
        df=df[kolom[-1:] + kolom[:-1]]
        df=df[(df['Kemiripan']>0) | (df['Skor']>0)]
        table = df.to_html(classes='table table-striped', index=False)
        return render_template('home.html', tabel=table, judul=judul, analisis=True)
    else:
      return render_template('home.html')

Kecualikan = ['pada', 'di', 'ke', 'dalam', 'menggunakan', 'yang']
def Jarak_Levenshtein_Kata(s, t, rasio = True):
  s=str(s).lower().split(" ")
  t=str(t).lower().split(" ")
  
  for S in s:
    if S in Kecualikan:
      s.remove(S)
  for T in t:
    if T in Kecualikan:
      t.remove(T)
      
  if s==[]:
    return 0
  
  # Buat matriks nol
  baris = len(s)+1
  kolom = len(t)+1
  jarak = np.zeros((baris,kolom),dtype = int)

  # Inisiasi nilai kolom dan baris
  for i in range(1, baris):
      for k in range(1,kolom):
          jarak[i][0] = i
          jarak[0][k] = k

  for kol in range(1, kolom):
      for bar in range(1, baris):
          if s[bar-1] == t[kol-1]:
              cost = 0 # nol jika sama
          else:
              if rasio == True:
                  cost = 2
              else:
                  cost = 1
          jarak[bar][kol] = min(jarak[bar-1][kol] + 1,      # remove
                                jarak[bar][kol-1] + 1,       # insert
                                jarak[bar-1][kol-1] + cost)  # replace
  if rasio == True:
      # Rasio Levenshtein
      Rasio = ((len(s)+len(t)) - jarak[bar][kol]) / (len(s)+len(t))
      return Rasio
  else:
      return "Jarak dua string tersebut adalah {}.".format(jarak[bar][kol])

def skor(S,T):
  S=str(S).lower().split(" ")
  T=str(T).lower().split(" ")
  
  for s in S:
    if s in Kecualikan:
      S.remove(s)
  for t in T:
    if t in Kecualikan:
      T.remove(t)
  if S==[]:
    return 0
  
  skor=0
  for s in S:
    if s in T:
      skor+=1
  return skor

if __name__=='__main__':
  app.run(debug=True)