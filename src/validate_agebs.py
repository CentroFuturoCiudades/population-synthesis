import numpy as np
import pandas as pd
from itertools import combinations, product

pob_sets = {
    'POBTOT': set(range(131)),
    'P_0A2': set(range(0, 3)),
    'P_3YMAS': set(range(3, 131)),
    'P_5YMAS': set(range(5, 131)),
    'P_12YMAS': set(range(12, 131)),
    'P_15YMAS': set(range(15, 131)),
    'P_18YMAS': set(range(18, 131)),
    'P_3A5': set(range(3, 6)),
    'P_6A11': set(range(6, 12)),
    'P_8A14': set(range(8, 15)),
    'P_12A14': set(range(12, 15)),
    'P_15A17': set(range(15, 18)),
    'P_18A24': set(range(18, 25)),
    'P_15A49': set(range(15, 50)),
    'P_60YMAS': set(range(60, 131)),
    'POB0_14': set(range(0, 15)),
    'POB15_64': set(range(15, 65)),
    'POB65_MAS': set(range(65, 131))
}


def validate_ageb(a, show=True):
    
    if show:
        print(f"::AGEB:: ENTIDAD={a['ENTIDAD']} MUN={a['MUN']} LOC={a['LOC']} AGEB={a['AGEB']}")
    
    keys = list(pob_sets.keys())
    valid = True
    
    def get_m(c):
        if c == 'POBTOT':
            c_m = 'POBMAS'
            return c_m
        if c.startswith('P_'):
            c_m = c + '_M'
            return c_m
        if c == 'P_15A49':
            return None
        return None
    
    def get_f(c):
        if c == 'POBTOT':
            c_m = 'POBFEM'
            return c_m
        if c.startswith('P_'):
            c_m = c + '_F'
            return c_m
        return None
    
    # Validate M and F add to total
    for c in keys:
        if c not in a.keys():
            continue
        c_m = get_m(c)
        c_f = get_f(c)
        if c_m is None or c_f is None:
            continue
        test = a[c] == a[c_m] + a[c_f]
        if not test:
            valid = False
            if show:
                print(f'    {c} == {c_m} + {c_f} :: {test} :: dif: {a[c] - a[c_m] - a[c_f]}')
            
            
    # Create a valid single group of sets and populations
    one_sets = {}
    one_pobs = {}
    one_sets_f = {}
    one_pobs_f = {}
    one_sets_m = {}
    one_pobs_m = {}
    for c in keys:
        s = pob_sets[c]
        if c in a.keys():
            one_sets[f'{c}'] = s
            one_pobs[f'{c}'] =  a[c]
        c_f = get_f(c)
        if c_f in a.keys():
            one_sets_f[f'{c_f}'] = s
            one_pobs_f[f'{c_f}'] =  a[c_f] 
        c_m = get_m(c)
        if c_m in a.keys():
            one_sets_m[f'{c_m}'] = s
            one_pobs_m[f'{c_m}'] =  a[c_m] 
                
    # Test two and three set joins against single supersets
    # Find all combinations of two disjoint sets
    two_sets = {}
    two_pobs = {}
    two_sets_f = {}
    two_pobs_f = {}
    two_sets_m = {}
    two_pobs_m = {}
    for c1, c2 in combinations(keys, 2):
        s1 = pob_sets[c1]
        s2 = pob_sets[c2]
        if s1.isdisjoint(s2) and c1 in a.keys() and c2 in a.keys():
            two_sets[f'{c1} + {c2}'] = s1.union(s2)
            two_pobs[f'{c1} + {c2}'] =  a[c1] + a[c2]
            
        c1f = get_f(c1)
        c2f = get_f(c2)
        if s1.isdisjoint(s2) and c1f in a.keys() and c2f in a.keys():
            two_sets_f[f'{c1f} + {c2f}'] = s1.union(s2)
            two_pobs_f[f'{c1f} + {c2f}'] =  a[c1f] + a[c2f]
            
        c1m = get_m(c1)
        c2m = get_m(c2)
        if s1.isdisjoint(s2) and c1m in a.keys() and c2m in a.keys():
            two_sets_m[f'{c1m} + {c2m}'] = s1.union(s2)
            two_pobs_m[f'{c1m} + {c2m}'] =  a[c1m] + a[c2m]

    three_sets = {}
    three_pobs = {}
    three_sets_f = {}
    three_pobs_f = {}
    three_sets_m = {}
    three_pobs_m = {}
    for c12, c3 in product(two_sets.keys(), keys):
        s12 = two_sets[c12]
        s3 = pob_sets[c3]
        if s12.isdisjoint(s3) and c3 in a.keys():
            three_sets[f'{c12} + {c3}'] = s12.union(s3)
            three_pobs[f'{c12} + {c3}'] = two_pobs[c12] + a[c3]
            
    for c12, c3 in product(two_sets_f.keys(), keys):
        c3f = get_f(c3)
        s12 = two_sets_f[c12]
        s3 = pob_sets[c3]
        if s12.isdisjoint(s3) and c3f in a.keys():
            three_sets_f[f'{c12} + {c3f}'] = s12.union(s3)
            three_pobs_f[f'{c12} + {c3f}'] = two_pobs_f[c12] + a[c3f]
            
    for c12, c3 in product(two_sets_m.keys(), keys):
        c3m = get_m(c3)
        s12 = two_sets_m[c12]
        s3 = pob_sets[c3]
        if s12.isdisjoint(s3) and c3m in a.keys():
            three_sets_m[f'{c12} + {c3m}'] = s12.union(s3)
            three_pobs_m[f'{c12} + {c3m}'] = two_pobs_m[c12] + a[c3m]
        
            
   
    def validate_sets(sets1, pobs1, sets2, pobs2, show=False):
        v = True
        for c1, c2 in product(sets1.keys(), sets2.keys()):
            s1 = sets1[c1]
            s2 = sets2[c2]
            p1 = pobs1[c1]
            p2 = pobs2[c2]
            if c1 == c2:
                continue
            if s1 == s2:
                # Equality must hold
                test = p1 == p2
                if not test:
                    v = False
                    if show:
                        print(f'    {c1} == {c2} :: {test} :: dif: {p1 - p2}')
                continue
            if len(s1) >= len(s2):
                smax = s1
                pmax = p1
                cmax = c1
                smin = s2
                pmin = p2
                cmin = c2
            else:
                smax = s2
                pmax = p2
                cmax = c2
                smin = s1
                pmin = p1
                cmin = c1
            if smin.issubset(smax):
                # Then pop of c1 must be less or equal than pop of c2
                test = pmin <= pmax
                if not test:
                    v = False
                    if show:
                        print(f'    {cmin} <= {cmax} :: {test} :: dif:{pmax-pmin}')
        return v
    
    valid = validate_sets(one_sets, one_pobs, one_sets, one_pobs, show) and valid
    valid = validate_sets(one_sets, one_pobs, two_sets, two_pobs, show) and valid
    valid = validate_sets(one_sets, one_pobs, three_sets, three_pobs, show) and valid
    valid = validate_sets(two_sets, two_pobs, three_sets, three_pobs, show) and valid
    
    valid = validate_sets(one_sets_f, one_pobs_f, one_sets_f, one_pobs_f, show) and valid
    valid = validate_sets(one_sets_f, one_pobs_f, two_sets_f, two_pobs_f, show) and valid
    valid = validate_sets(one_sets_f, one_pobs_f, three_sets_f, three_pobs_f, show) and valid
    valid = validate_sets(two_sets_f, two_pobs_f, three_sets_f, three_pobs_f, show) and valid
    
    valid = validate_sets(one_sets_m, one_pobs_m, one_sets_m, one_pobs_m, show) and valid
    valid = validate_sets(one_sets_m, one_pobs_m, two_sets_m, two_pobs_m, show) and valid
    valid = validate_sets(one_sets_m, one_pobs_m, three_sets_m, three_pobs_m, show) and valid
    valid = validate_sets(two_sets_m, two_pobs_m, three_sets_m, three_pobs_m, show) and valid
    
    if show:
        print('-----------------------------------------------------------------')
        print()
    
    return valid
    

if __name__ == '__main__':
    # Load census data
    df_censo = pd.read_csv('./data/census_ageb_manz/RESAGEBURB_19CSV20.csv', na_values=['*', 'N/D'], low_memory=False)

    # Filter for agebs
    df_entidad = df_censo.query('ENTIDAD != 0 & MUN == 0 & LOC == 0 & AGEB == "0000" & MZA == 0')
    df_mun = df_censo.query('ENTIDAD != 0 & MUN != 0 & LOC == 0 & AGEB == "0000" & MZA == 0')
    df_loc = df_censo.query('ENTIDAD != 0 & MUN != 0 & LOC != 0 & AGEB == "0000" & MZA == 0')
    df_agebs = df_censo.query('ENTIDAD != 0 & MUN != 0 & LOC != 0 & AGEB != "0000" & MZA == 0')

    # Eliminar AGEBS sin población
    df_agebs = df_agebs[df_agebs.POBTOT > 0]
    
    id_columns = ['ENTIDAD', 'MUN', 'LOC', 'AGEB']

    pob_columns = (
        ['POBTOT', 'POBFEM', 'POBMAS']
        + [c for c in df_agebs.columns if c.startswith('P_')]
        + ['POB0_14', 'POB15_64', 'POB65_MAS'])
    df_agebs_pob = df_agebs[id_columns + pob_columns].dropna()
    
    valid_agebs = df_agebs_pob.apply(validate_ageb, axis=1)