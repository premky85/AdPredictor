import pandas as pd
import matplotlib.pyplot as plt
import glob

files = glob.glob("C:\dataMining\*.csv")

def preberi(file: object) -> object:
    df = pd.read_csv(file, header=None, sep='\t', usecols=[3, 13])
    df.columns = ['user', 'clicks']
    df = df.groupby(["user"]).sum().reset_index()
    df = df[df.clicks > 0]
    return pd.Series(df.clicks)


s = preberi(files[0])

for f in files[1:]:
    s = pd.concat([s, preberi(f)])

pltval = s.value_counts(normalize=True)
pltval.plot.bar()
plt.show()

df = pltval.to_frame()
print(df)
#maks = df.loc[df['clicks'].idxmax()].clicks
df = df.sort_values(by=['clicks'], ascending=True)
#df.loc[:,'clicks'] *= 100 # za odstotke

import plotly
import plotly.graph_objs as go

stUSer = [x for x in range(len(df))]

'''
fig = {
    'data': [
  		go.bar ({
  			'x': stUSer,
        	'y': df.clicks,
        	'text': 'Uporabnikovi kliki',
        	'mode': 'markers',
        	'name': '2007'
        })
    ],
    'layout': {
        'xaxis': {'title': 'Uporabniki', 'type': 'linear'},
        'yaxis': {'title': "Kliki"}
    }
}
plotly.offline.plot(fig,auto_open=True)
'''

plotly.offline.plot({
    "data": [go.Bar(x=df.index, y=df.clicks)],
    "layout": go.Layout(title="Odstotek klikov na oglas")
}, auto_open=True)
