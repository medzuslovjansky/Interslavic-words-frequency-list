import slovnik 
import pandas as pd

slovnik_loaded = slovnik.load_slovnik(obnoviti=False)    
slovnik = slovnik.prepare_slovnik(slovnik_loaded['words']) 

    
import wordfreq_copy as wordfreq

def freq_of_row(cell, lang):
    if isinstance( cell, set or list ) or isinstance( cell, list ): 
        return max( list( map(lambda z: wordfreq.zipf_frequency( z, lang ), cell) ) )
    if isinstance( cell, str ): 
        return wordfreq.zipf_frequency( cell, lang )

LANGS = "isv en ru uk be pl cs sk bg mk sr hr sl de nl eo".split(' ')
LANGS_2 = LANGS[1:13]

lang_scores = dict({
            'en': 0.5, 
            'ru': 1, 
            'be': 0.5, 
            'uk': 0.5, 
            'pl': 1, 
            'cs': 0.5, 
            'sk': 0.5, 
            'bg': 0.5,
            'mk': 0.5, 
            'sr': 0.5,
            'hr': 0.5,
            'sl': 0.5, 
            })


for lang in LANGS_2:
    slovnik[f'freq ({lang})'] = slovnik[lang].apply(lambda x: freq_of_row(x, lang) )

for i, row in slovnik.iterrows():
    accumulate = 0
    for lang in LANGS_2:
        lang_key = f'freq ({lang})'
        accumulate += lang_scores[lang]*row[lang_key]
    slovnik['frequency'][i] = accumulate/len(LANGS_2)

## udaliti vse kolony kromě medžuslovjanskoj:
# for lang in LANGS_2:
#     slovnik = slovnik.drop( f'freq ({lang})', axis=1 )

slovnik = slovnik.sort_values("frequency", ascending=False)

with pd.ExcelWriter("freq_all_langs.xlsx") as writer:
    slovnik.to_excel(writer)
    
