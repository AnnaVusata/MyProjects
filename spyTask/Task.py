import spyre.server
import pandas as pd

name='vhi/vhi_{}.csv'
df = pd.DataFrame()
for i in range(1, 26):
    temp = pd.read_csv(name.format(i), sep='[, ]+', engine='python')
    temp['Province'] = i
    df = df.append(temp, ignore_index=True)

class MyApp(spyre.server.App):
    title = "Analysis"
    inputs = [           
                {
                    "type":'dropdown',
                    "label": 'Province',
                    "options": [{"label": "Vinnytska", "value":1},
                           {"label": "Volinska", "value":2},
                           {"label": "Dnipropetrovska", "value":3},
                           {"label": "Donetska", "value": 4},
                           {"label": "Zhytomyrska", "value": 5},
                           {"label": "Zakarpattya", "value": 6},
                           {"label": "Zaporizka", "value": 7},
                           {"label": "Ivano-Frankivska", "value": 8},
                           {"label": "Kyivska", "value": 9},
                           {"label": "Kyrovohradska", "value": 10},
                           {"label": "Luganska", "value": 11},
                           {"label": "Lvivska", "value": 12},
                           {"label": "Mykolaivska", "value": 13},
                           {"label": "Odeska", "value": 14},
                           {"label": "Poltavska", "value": 15},
                           {"label": "Rivnenska", "value": 16},
                           {"label": "Sumska", "value": 17},
                           {"label": "Ternopilska", "value": 18},
                           {"label": "Kharkyvska", "value": 19},
                           {"label": "Khersonska", "value": 20},
                           {"label": "Khmelnitska", "value": 21},
                           {"label": "Cherkaska", "value": 22},
                           {"label": "Chernivetska", "value": 23},
                           {"label": "Chernihivska", "value": 24},
                           {"label": "Crimean", "value": 25}],
                    "key": 'province',
                    "action_id": "update_data"
                },
                {
                   "type": 'dropdown',
                   "label": 'Year',
                   "options": [{'label': str(i), 'value': i} for i in range(1982, 2020)],
                   'key': 'year',
                   'value': '1982'
                },
                {
                    "type" : 'text',
                    "key" : 'FirstWeek',
                    "label" : 'FirstWeek',
                    "value": 1
                },
                {
                    "type" : 'text',
                    "key" : 'LastWeek',
                    "label" : 'LastWeek',
                    "value": 52  
                },
                    
            ]

    outputs = [{"type": "table",
                "id": "getInfo",
                'control_id': 'press_me',
                'tab': 'Table1'},

               {'type': 'plot',
                'id': 'getPlot1',
                'control_id': 'press_me',
                'tab': 'Plot1'},

                {"type": "table",
                "id": "getMean",
                'control_id': 'press_me',
                'tab': 'Table2'},

               {'type': 'plot',
                'id': 'getPlot2',
                'control_id': 'press_me',
                'tab': 'Plot2'},
                ]

    controls = [{"type": 'button',
                 'id': 'press_me',
                 'label': 'Press Me'}]

    tabs = ["Table1", "Plot1","Table2", "Plot2"]

    def getInfo(self, params):
        year = int(params['year'])
        FirstWeek = int(params['FirstWeek'])       
        LastWeek = int(params['LastWeek']) 
        pr =int(params['province'])
        f = df[(df['year'] == year) & (df['Province'] == pr) & (df['week'] >= FirstWeek) & (df['week'] <= LastWeek)] [['year', 'week', 'VHI', 'TCI', 'VCI']]
        print(f)
        return f

    def getPlot1(self, params):
        df = self.getInfo(params)
        f = df[['VCI', 'TCI', 'VHI']]
        return f.set_index(df['week']).plot()
        

    def getMean(self, params):
        year = int(params['year'])
        pr =int(params['province'])
        result = pd.DataFrame(columns =['year', 'Mean','Province'])
        for i in range(1, 13):
            monthes = df[(df['week'] > 4*(i-1)) & (df['week'] <= 4*i)]
            Meann = monthes[(df['year']==year) & (df['Province']==pr)][['VHI']].mean()
            Mean = int(Meann) 
            new_line = {'year':year,'Month':i, 'Mean':Mean,'Province':pr}
            result = result.append(new_line, ignore_index=True) 

        print(result)
        return result

    def getPlot2(self, params):
        df = self.getMean(params)
        f = df[['Mean']]
        return f.set_index(df['Month']).plot()


app = MyApp()
app.launch(port=4030)