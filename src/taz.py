import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt


def load_marco_geo(marco_geo_path, df_mun, df_loc, df_agebs):
    mg_agebs = gpd.read_file(marco_geo_path, layer='19a')
    mg_agebs = mg_agebs.drop(columns=['CVE_ENT'])

    mg_loc = gpd.read_file(marco_geo_path, layer='19l')
    mg_loc = mg_loc.drop(columns=['CVE_ENT', 'NOMGEO', 'AMBITO'])

    mg_loc_pr = gpd.read_file(marco_geo_path, layer='19lpr')
    mg_loc_pr = mg_loc_pr.drop(
        columns=['CVE_ENT', 'NOMGEO', 'PLANO', 'CVE_MZA', 'CVE_AGEB']
    )

    mg_agebs[
        ['CVE_MUN', 'CVE_LOC']
    ] = mg_agebs[['CVE_MUN', 'CVE_LOC']].astype(int)
    mg_loc[
        ['CVE_MUN', 'CVE_LOC']
    ] = mg_loc[['CVE_MUN', 'CVE_LOC']].astype(int)
    mg_loc_pr[
        ['CVE_MUN', 'CVE_LOC']
    ] = mg_loc_pr[['CVE_MUN', 'CVE_LOC']].astype(int)

    mg_agebs = mg_agebs.rename(
        columns={
            'CVE_MUN': 'MUN',
            'CVE_LOC': 'LOC',
            'CVE_AGEB': 'AGEB'}
    )
    mg_agebs = mg_agebs.set_index(['MUN', 'LOC', 'AGEB']).sort_index()
    mg_loc = mg_loc.rename(columns={'CVE_MUN': 'MUN', 'CVE_LOC': 'LOC'})
    mg_loc = mg_loc.set_index(['MUN', 'LOC']).sort_index()
    mg_loc_pr = mg_loc_pr.rename(columns={'CVE_MUN': 'MUN', 'CVE_LOC': 'LOC'})
    mg_loc_pr = mg_loc_pr.set_index(['MUN', 'LOC']).sort_index()
    mg_loc_pr['CVEGEO'] = mg_loc_pr.CVEGEO.str[:9]

    # Point localities need to. be converted to polygons
    # as to allow for overlay operations in the whole geometries
    mg_loc_pr['geometry'] = mg_loc_pr.geometry.buffer(100)

    # Merge polygon and point localities, for total localities
    # Filter out empty localities
    mg_loc = mg_loc.join(mg_loc_pr, rsuffix='_pr', how='outer')
    mg_loc = mg_loc.loc[df_loc.index]
    mg_loc['CVEGEO'] = mg_loc.CVEGEO.mask(
        mg_loc.CVEGEO.isna(), mg_loc.CVEGEO_pr
    )
    mg_loc['geometry'] = mg_loc.geometry.mask(
        mg_loc.geometry.isna(), mg_loc.geometry_pr
    )
    mg_loc = mg_loc.drop(columns=['CVEGEO_pr', 'geometry_pr'])

    # Filter out empty agebs
    mg_agebs = mg_agebs.loc[df_agebs.index]

    # Add population information
    # TODO: Once implementation complete, we should add full census counts
    mg_loc = mg_loc.join(df_loc)  # [['POBTOT', 'TVIVHAB']])
    mg_agebs = mg_agebs.join(df_agebs)  # [['POBTOT', 'TVIVHAB']])
    assert df_loc.shape[0] == mg_loc.shape[0]
    assert mg_agebs.shape[0] == df_agebs.shape[0]

    # Make sure total pop by mun is sum of localities populations
    assert np.all(
        mg_loc.POBTOT.groupby('MUN').sum().values == df_mun.POBTOT.values
    )

    # Make a single gdf with all localities and agebs with population
    # drop localities that are disaggregated into agebs
    mg_loc['AGEB'] = '0000'
    mg_loc_t = mg_loc.reset_index().set_index(
        ['MUN', 'LOC', 'AGEB']
    ).drop(
        mg_agebs.index.droplevel(2).drop_duplicates()
    )
    mg = pd.concat(
        [mg_agebs, mg_loc_t]
    ).sort_index()

    # Assert all population by municipality is taken into account
    assert np.all(
        mg.groupby('MUN').POBTOT.sum().values == df_mun.POBTOT.values
    )

    assert mg.index.is_unique

    return mg


def merge_mg_taz(mun, taz, mg, mun_dict):
    taz_mun = taz[taz.MUNICIPIO == mun].copy()
    mg_mun = mg.loc[mun_dict[mun]].copy()

    mg_mun['mg_AREA'] = mg_mun.area

    overlay = gpd.overlay(
        taz_mun,
        mg_mun.reset_index(),
        keep_geom_type=False
    ).drop(
        columns=['MUNICIPIO', 'ID', 'AREA', 'MACROZONA']
    )

    overlay['intersection_AREA'] = overlay.area

    overlay['ratio'] = overlay.intersection_AREA / overlay.mg_AREA
    overlay['VIV_ratio'] = overlay.ratio * overlay.TVIVHAB

    # Keep only a single mg result
    # an ageb or locality can only be assigned one taz
    overlay = overlay.sort_values(
        'ratio', ascending=False
    ).drop_duplicates(
        subset='CVEGEO', keep='first'
    )
    overlay = overlay.set_index(['LOC', 'AGEB']).sort_index()

    # Filter by ratio to remove false intersections
    overlay_dropped = overlay.query('0 < ratio <= 0.5')
    overlay = overlay.query('ratio > 0.5')

    if '0000' in overlay_dropped.index.get_level_values(1):
        overlay_dropped = overlay_dropped.drop('0000', level=1)

    # Add unassigned mg geometries
    mg_unass = mg_mun.drop(overlay.index)
    # print(mun, len(overlay_dropped))
    print(mun, overlay_dropped.query('ratio > 0.01').ratio.sort_values(ascending=False))
    # print(mun, overlay_dropped.ratio.sort_values(ascending=True).values[:5])
    # print(mun,
    #       overlay_dropped.ratio.sort_values(ascending=True).values[:5]
    #       * overlay_dropped.sort_values('ratio', ascending=True).TVIVHAB.values[:5])

    mg_unass['ZONA'] = -10
    mg_unass['ratio'] = 0
    mg_unass.loc[overlay_dropped.index, 'ratio'] = overlay_dropped.ratio

    overlay = pd.concat([overlay, mg_unass]).loc[mg_mun.index]

    assert np.all(overlay.index == mg_mun.index)

    overlay['geometry'] = mg_mun.geometry

    return overlay, overlay_dropped


def plot_taz_mg(mg_gdf, taz_gdf, title,
                display=True, savepath=None,
                ax=None):

    mg_gdf = mg_gdf.query('ratio > 0')

    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(20, 15))

    mg_gdf.plot(
        column='ZONA',
        edgecolor='none',
        categorical=False,
        cmap='prism',
        ax=ax)

    taz_gdf.plot(
        linewidth=3,
        color='none',
        edgecolor='black',
        ax=ax,
    )

    mg_gdf.plot(
        color='none',
        edgecolor='grey',
        ax=ax)

    ax.set_title(title)
    ax.axis('off')

    if ax is not None:
        if not display:
            plt.close()
        if savepath is not None:
            fig.savefig(savepath)


def plot_taz_mg_unass(mg_gdf, taz_gdf, title,
                      display=True, savepath=None, ax=None):

    mg_gdf = mg_gdf.query('ratio > 0')

    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(20, 15))

    mg_gdf = mg_gdf.query('ZONA < 0')

    taz_gdf.plot(
        color='lightblue',
        edgecolor='none',
        ax=ax,
        alpha=0.5,
    )

    mg_gdf.plot(
        # color='red',
        column='ratio',
        edgecolor='none',
        categorical=False,
        ax=ax,
        legend=True
    )

    taz_gdf.plot(
        linewidth=2,
        color='none',
        edgecolor='black',
        ax=ax,
    )

    mg_gdf.plot(
        color='none',
        edgecolor='grey',
        ax=ax)

    ax.set_title(title)
    ax.axis('off')

    if ax is not None:
        if not display:
            plt.close()
        if savepath is not None:
            fig.savefig(savepath)


def plot_taz_empty_mg(mg_gdf, taz_gdf, title,
                      display=True, savepath=None, ax=None):

    mg_gdf = mg_gdf.query('ratio > 0')

    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(20, 15))

    taz_gdf = taz_gdf[~taz_gdf.ZONA.isin(mg_gdf.ZONA.unique())]

    mg_gdf.plot(
        column='ZONA',
        edgecolor='none',
        categorical=False,
        cmap='prism',
        ax=ax)

    taz_gdf.plot(
        linewidth=3,
        color='none',
        edgecolor='black',
        ax=ax,
    )

    mg_gdf.plot(
        color='none',
        edgecolor='grey',
        ax=ax)

    ax.set_title(title)
    ax.axis('off')

    if ax is not None:
        if not display:
            plt.close()
        if savepath is not None:
            fig.savefig(savepath)


def plot_taz_codes(taz_gdf, title,
                   display=True, savepath=None, ax=None):
    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(20, 15))

    taz_gdf = taz_gdf.copy()

    taz_gdf.plot(
        linewidth=3,
        color='none',
        edgecolor='black',
        ax=ax,
    )

    taz_gdf['points'] = taz_gdf.representative_point()
    for idx, row in taz_gdf.iterrows():
        plt.annotate(text=row['ZONA'], xy=row['points'].coords[0],
                     horizontalalignment='center', color='red')

    ax.set_title(title)
    ax.axis('off')

    if ax is not None:
        if not display:
            plt.close()
        if savepath is not None:
            fig.savefig(savepath)


def plot_chull(taz_gdf, title,
               display=True, savepath=None, ax=None):
    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(20, 15))

    taz_gdf.plot(
        linewidth=1,
        color='lightblue',
        edgecolor='black',
        ax=ax,
    )

    taz_gdf[taz_gdf.geom_type == 'MultiPolygon'].plot(
        linewidth=1,
        column='ZONA',
        edgecolor='black',
        ax=ax,
        categorical=True
    )

    taz_gdf[taz_gdf.geom_type == 'MultiPolygon'].convex_hull.plot(
        linewidth=1,
        edgecolor='red',
        color='none',
        ax=ax,
    )
    ax.axis('off')
    if ax is not None:
        if not display:
            plt.close()
        if savepath is not None:
            fig.savefig(savepath)
