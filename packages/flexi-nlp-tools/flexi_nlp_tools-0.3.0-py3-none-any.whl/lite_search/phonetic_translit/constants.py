"""A list for converting phonetic representation in English to Ukrainian/Russian pronunciation
For clarity, an example word with its phonetic transcription including the commented sound is provided in the comments
The sound representation is based on the ARPAbet symbol set: http://www.speech.cs.cmu.edu/cgi-bin/cmudict"""
PHONEME2UK = {
    'AA': ['а', 'о'],           # odd:      [AA D]
    'AE': ['е', 'а'],           # at:       [AE T]
    'AH': ['а'],                # hut:	    [HH AH T]
    'AO': ['ау', 'оу'],         # ought:    [AO T]
    'AW': ['ау', 'ав'],         # cow:      [K AW]
    'AY': ['аі', 'ай'],         # hide	    [HH AY D]
    'B': ['б'],                 # be	    [B IY]
    'CH': ['ч'],                # cheese	[CH IY Z]
    'D': ['д'],                 # dee	    [D IY]
    'DH': ['з'],                # thee	    [DH IY]
    'EH': ['е', 'а'],           # Ed	    [EH D]
    'ER': ['йо', 'е'],          # hurt	    [HH ER T]
    'EY': ['ей', 'еі'],         # ate	    [EY T]
    'F': ['ф'],                 # fee	    [F IY]
    'G': ['г', 'ґ', 'к'],       # green	    [G R IY N]
    'HH': ['х'],                # he	    [HH IY]
    'IH': ['і'],                # it	    [IH T]
    'IY': ['і'],                # eat		[IY T]
    'JH': ['дж'],               # gee	    [JH IY]
    'K': ['к'],                 # key	    [K IY]
    'L': ['л'],                 # lee	    [L IY]
    'M': ['м'],                 # me	    [M IY]
    'N': ['н'],                 # knee	    [N IY]
    'NG': ['н', 'нг'],          # ping	    [P IH NG]
    'OW': ['оу', 'оа', 'о'],    # oat	    [OW T]
    'OY': ['ой', 'оі'],         # toy	    [T OY]
    'P': ['п'],                 # pee	    [P IY]
    'R': ['р'],                 # read	    [R IY D]
    'S': ['с'],                 # sea	    [S IY]
    'SH': ['ш', 'щ'],           # she	    [SH IY]
    'T': ['т'],                 # tea	    [T IY]
    'TH': ['з', 'с'],           # theta	    [TH EY T AH]
    'UH': ['у'],                # hood	    [HH UH D]
    'UW': ['у', 'ю'],           # two	    [T UW]
    'V': ['в'],                 # vee	    [V IY]
    'W': ['в', 'у'],            # we	    [W IY]
    'Y': ['й'],                 # yield	    [Y IY L D]
    'Z': ['з'],                 # zee		[Z IY]
    'ZH': ['ж'],                # seizure	[S IY ZH ER]
    ' ': [' ']
}


"A list of slavic letter combinations that can be represented with fewer characters"
COMBINEUK = {
    'йа': 'я',
    'йе': 'є',
    'йу': 'ю',
    'шч': 'щ',
}
