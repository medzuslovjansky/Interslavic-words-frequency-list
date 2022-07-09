import pandas as pd
import os, re

brackets_regex1 = re.compile(" \(.*\)")
brackets_regex2 = re.compile(" \[.*\]")

slovnik_link = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRsEDDBEt3VXESqAgoQLUYHvsA5yMyujzGViXiamY7-yYrcORhrkEl5g6JZPorvJrgMk6sjUlFNT4Km/pub?output=xlsx'

def load_slovnik(tabela=slovnik_link, obnoviti=False):

    if os.path.isfile("slovnik_words.pkl") and obnoviti == False:
        print("Found 'slovnik_slovnik.pkl' file, using it")
        dfs = {"words": pd.read_pickle("slovnik_words.pkl")}
        return dfs

    dfs = pd.read_excel(io=tabela, engine='openpyxl', sheet_name=['words'])

    for name in dfs['words'].columns:
        dfs['words'][name] = dfs['words'][name].fillna(' ').astype(str)
    dfs['words'].to_pickle("slovnik_words.pkl")

    return dfs


LANGS = "isv en ru uk be pl cs sk bg mk sr hr sl de nl eo".split(' ')
LANGS_2 = LANGS[1:13]


from collections import defaultdict

transliteration = defaultdict( lambda: lambda x: x)

transliteration['ru'] = lambda x: x.replace("ё", "е")
transliteration['uk'] = lambda x: x.replace('ґ', 'г')
transliteration['be'] = lambda x: x.replace('ґ', 'г')

# Oddaljaje space'y ako li one sut v početku teksta
def despace(s):
    if s and s[0] == ' ':
        return s.replace(' ', '')
    return s

def cell_normalization(cell, jezyk):
    cell = str(cell)
    cell = str.replace( cell, '!', '')
    cell = str.replace( cell, '#', '')
    cell = cell.lower()
    cell = transliteration[jezyk](cell)
    return cell

def symbols_normalization(cell):
    cell = str(cell)
    cell = str.replace( cell, '+', '' )     
    cell = str.replace( cell, '^', '' ) 
    cell = str.replace( cell, '$', '' )  
    cell = str.replace( cell, '?', '' )  
    cell = str.replace( cell, '@', '' )    
    cell = str.replace( cell, '-', '' )
    cell = str.replace( cell, '!', '' )    
    cell = str.replace( cell, '#', '' )
    cell = str.replace( cell, '/', '' )
    cell = str.replace( cell, '\\', '' )                
    return cell


def prepare_slovnik(slovnik, split=False, transliterate = False):
    for lang in LANGS:
        assert slovnik[slovnik[lang].astype(str).apply(lambda x: "((" in sorted(x))].empty
    for lang in LANGS:
        slovnik[lang].str.replace(brackets_regex1, "")
        slovnik[lang].str.replace(brackets_regex2, "")
        slovnik[lang] = slovnik[lang].apply(lambda x: cell_normalization(x, lang))
        slovnik[lang] = slovnik[lang].apply(lambda x: despace(x))   
        if transliterate == True:
            slovnik[lang] = slovnik[lang].apply(transliteration[lang])
        if split == True:
            slovnik[lang + "_set"] = slovnik[lang].str.split(", ").apply(lambda x: x)
    slovnik['isv'] = slovnik['isv'].str.replace("!", "").str.replace("#", "").str.lower()
    return slovnik


def filtr_contain(stroka, sheet):
    return sheet[ sheet.str.contains(stroka) == True]

def iskati(slovo, sheet):
    for stroka in sheet:    
        if slovo in str.split( stroka, ', ' ):
            return True
    return False

def is_in_dict(slovo, sheet):
    result = filtr_contain(slovo, sheet)
    return iskati(slovo, result)

