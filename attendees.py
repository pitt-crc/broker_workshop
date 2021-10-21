import sys

import pandas as pd

df = pd.read_csv('Broker Workshop Registration.csv')
for idx, row in df.iterrows():
    print(f"""    <tr>
      <th scope="row">{row['First and last name']}</th>
      <td>{row['Host university or professional affiliation']}</td>
      <td>{row['Which broker(s) do you work on as a developer (if any)?']}</td>
    </tr>""")
