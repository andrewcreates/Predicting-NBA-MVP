from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

tables = ['divs_standings_E','divs_standings_W','divs_standings_']
Year=[]
Tm=[]
Wins=[]
Losses=[]
WL=[]

driver = webdriver.Chrome()
for year in range(1950,2020):
    url = "https://www.basketball-reference.com/leagues/NBA_{}.html".format(year)
    driver.get(url)
    driver.implicitly_wait(2)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    for table in tables:
        try:
            conf_table = soup.find(lambda tag: tag.name == 'table' and tag.has_attr('id') and tag['id'] == table)
            teams = conf_table.findAll('a', href=re.compile("/{}.html".format(year)))
            wins = conf_table.findAll(attrs={'data-stat': 'wins'})
            losses = conf_table.findAll(attrs={'data-stat': 'losses'})
            winloss = conf_table.findAll(attrs={'data-stat': 'win_loss_pct'})
            Tm.append(table+' '+str(year))
            for team in teams:
                Tm.append(team.get_text())
            for win in wins:
                Wins.append(win.get_text())
                Year.append(year)
            for loss in losses:
                Losses.append(loss.get_text())
            for wl in winloss:
                WL.append(wl.get_text())
        except (AttributeError, Exception):
            continue

#print(Tm)
#print(Year)
#print(Wins)
#print(Losses)
#print(WL)

driver.quit()

dict = {'Team_Name':Tm, 'Year':Year, 'Wins':Wins, 'Losses':Losses, 'WL%':WL}
df = pd.DataFrame(dict)

df.to_csv('NBA_team_wins.csv')