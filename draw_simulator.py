# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 00:10:19 2025

@author: John M Waugh 
"""

import random
import pandas as pd
import itertools
import time

readIn = pd.read_csv("UEFA_CL.csv")
teams = readIn["Club"]
pot1 = readIn.loc[readIn['Pot'] == 1, ['Club', 'Country']]
pot2 = readIn.loc[readIn['Pot'] == 2, ['Club', 'Country']]
pot3 = readIn.loc[readIn['Pot'] == 3, ['Club', 'Country']]
pot4 = readIn.loc[readIn['Pot'] == 4, ['Club', 'Country']]

pot1 = list(pot1["Club"])
pot2 = list(pot2["Club"])
pot3 = list(pot3["Club"])
pot4 = list(pot4["Club"])

pots = []
pots.extend([pot1, pot2, pot3, pot4])

pot_names = ["pot1", "pot2", "pot3", "pot4"] 

combos = list(itertools.combinations_with_replacement(pots, 2))
names = list(itertools.combinations_with_replacement(pot_names, 2))

def simulate_draw(teams):
    
    global counter
    counter = 0
    matches = len(teams) * 4
   
    global fixtures
    fixtures = {team: {'pot1_h': [], 'pot1_a': [], 'pot2_h': [],
                    'pot2_a': [], 'pot3_h': [], 'pot3_a': [],
                    'pot4_h': [], 'pot4_a': []} for team in teams}
    
    global countries
    countries = {team: {'pot1_h': [], 'pot1_a': [], 'pot2_h': [],
                    'pot2_a': [], 'pot3_h': [], 'pot3_a': [],
                    'pot4_h': [], 'pot4_a': []} for team in teams}
    
    while counter < matches:
    
        for i in range(0, 10):
            pot = combos[i][0]
            potID = names[i][0]
            opp_pot = combos[i][1] 
            oppID = names[i][1]
            
            potH = f"{potID}_h"
            potA = f"{potID}_a"
            oppH = f"{oppID}_h"
            oppA = f"{oppID}_a"
            
            if pot == opp_pot:
                potCount = len(pot)
            else:
                potCount = 0
            
            random.shuffle(pot)
            
            MAX_RETRIES = 162
            attempts = 0
            
            while attempts < MAX_RETRIES and potCount < len(teams) / 2:
                attempts += 1
            
                for team in pot:
                
                    code = readIn[readIn['Club'] == team]['Country']
                    code = list(code)[0]
                    
                    #build list of opponent associations team has already drawn
                    nations = tuple(countries[team].values())
                    nations = list(itertools.chain.from_iterable(nations))
                    #check if team has drawn a team from a nation twice
                    dup = [x for x in nations if nations.count(x) > 1]
                    dup = set(dup)
          
                    if len(fixtures[team][oppH]) < 1 or len(fixtures[team][oppA]) < 1:         
                   
                        possible_home_opponents = [
                            opponent for opponent in opp_pot
                            if opponent != team
                            and list(readIn[readIn['Club'] == opponent]['Country'])[0] != code
                            and list(readIn[readIn['Club'] == opponent]['Country'])[0] not in dup
                            and len(fixtures[opponent][potA]) < 1
                        ]
                        
                        for opponent in possible_home_opponents:
                          nations = tuple(countries[opponent].values())
                          nations = list(itertools.chain.from_iterable(nations))
                          oppDup = [x for x in nations if nations.count(x) > 1]
                          oppDup = tuple(oppDup)
                          oppDup = set(oppDup)
                              
                          if code in oppDup:
                              possible_home_opponents.remove(opponent)
                        
                        possible_away_opponents = [
                            opponent for opponent in opp_pot 
                            if opponent != team
                            and list(readIn[readIn['Club'] == opponent]['Country'])[0] != code
                            and list(readIn[readIn['Club'] == opponent]['Country'])[0] not in dup
                            and len(fixtures[opponent][potH]) < 1
                        ]
                        
                        for opponent in possible_away_opponents:
                               nations = tuple(countries[opponent].values())
                               nations = list(itertools.chain.from_iterable(nations))
                               oppDup = [x for x in nations if nations.count(x) > 1]
                               oppDup = tuple(oppDup)
                               oppDup = set(oppDup)
                               
                               if code in oppDup:
                                   possible_away_opponents.remove(opponent) 
                                       
                        if len(fixtures[team][oppH]) < 1 and possible_home_opponents:
                            opponent = random.choice(possible_home_opponents)
                            oppCodeH = list(readIn[readIn['Club'] == opponent]['Country'])[0]
                            fixtures[team][oppH].append(opponent)
                            fixtures[opponent][potA].append(team)
                            countries[team][oppH].append(oppCodeH)
                            countries[opponent][potA].append(code)
                            potCount += 1
                                    
                        if opponent in possible_away_opponents: 
                            possible_away_opponents.remove(opponent)      
                            
                        #update team dup with home opponent
                        nations = tuple(countries[team].values())
                        nations = list(itertools.chain.from_iterable(nations))
                        dup = [x for x in nations if nations.count(x) > 1]
                        dup = set(dup)
                        
                        for opponent in possible_away_opponents:
                            oppCode1 = list(readIn[readIn['Club'] == opponent]['Country'])[0]
                            
                            if oppCode1 in dup:
                                possible_away_opponents.remove(opponent)
                        
                        if len(fixtures[team][oppA]) < 1 and possible_away_opponents:
                            opponent = random.choice(possible_away_opponents)
                            oppCodeA = list(readIn[readIn['Club'] == opponent]['Country'])[0]
                            fixtures[team][oppA].append(opponent)
                            fixtures[opponent][potH].append(team)
                            countries[team][oppA].append(oppCodeA)
                            countries[opponent][potH].append(code)
                            potCount += 1
                            
                        if potCount == len(teams) / 2:
                            if pot == opp_pot:
                                counter += len(pot)
                            else:
                                counter += len(pot) + len(opp_pot)
                            print("pass: attempt: ", attempts, " ",  potID, " ", oppID, " ", potCount)
                            break
                                
                        if len(possible_home_opponents) == 0 or len(possible_away_opponents) == 0:
                           break
                
                if potCount != len(teams) / 2:
                    print("fail: attempt: ", attempts, " ",  potID, " ", oppID, " ", potCount)
                    if pot == opp_pot:
                        potCount = len(pot)
                    else:
                        potCount = 0
                        
                    for team in pot:
                        fixtures[team][oppH] = []
                        fixtures[team][oppA] = []
                        countries[team][oppH] = []
                        countries[team][oppA] = []
                    for opponent in opp_pot:
                        fixtures[opponent][potH] = []
                        fixtures[opponent][potA] = []
                        countries[opponent][potH] = []
                        countries[opponent][potA] = []
                                        
            print("count: ", counter)
            
            if attempts == MAX_RETRIES:
                counter = 0
                break
    
    if counter == matches:
        print("Draw complete.")
        
    return fixtures 

# Simulate the draw
start_time = time.perf_counter()

fixtures = simulate_draw(teams)
                        
end_time = time.perf_counter()

elapsed_time = end_time - start_time

print(f"Elapsed time: {elapsed_time:.2f} seconds")

fix_df = pd.DataFrame(data=fixtures)
fix_df = (fix_df.T)
fix_df.to_excel('fixtures.xlsx')

codes_df = pd.DataFrame(data=countries)
codes_df = (codes_df.T)
codes_df.to_excel('codes.xlsx')

test_df = str(fix_df)




