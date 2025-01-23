import json
import os
from bs4 import BeautifulSoup
import csv
from collections import defaultdict
import pandas as pd
from . import utils

def get_place_refs_df():
    """
    Returns a dataframe of place references by author and text.
    Pulls data from a pre-made .csv file.
    """
    df = pd.read_csv(r'CATK/src/CATK/data/classical_place_refs.csv')
    return _add_pleiades_ids(df)


def _parse_topos_place_refs_from_all_files(data=r'CATK\src\CATK\data\topos_text_htms'):

    def _convert_dict_to_long(df):
        main_list = []
        for source in df.keys():
            if ',' in source:
                list_author = source.split(',')[0]
                text = source.split(',')[1].strip()        
            elif source == 'anonymous':
                meta = source.split(' ', 1)
                list_author = meta[0].strip()
                text = meta[2].strip()
            for ref in df[source]:
                    main_list.append([list_author, text, ref])
        return main_list
    raw_data_file = utils.unzip_gz(data)
    directory = os.fsencode(data)
    topos_places = defaultdict(list)
    print("Locating place references throughout the Classical canon. Please be patient.")
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        # print(filename)
        if filename.endswith(".htm") or filename.endswith(".html"):
            # print("here!")
            name = 'CATK/src/CATK/data/topos_text_htms/' + filename
            text = open(name, "r", encoding="utf8").read()
            soup = BeautifulSoup(text, 'html.parser')
            title = soup.find('meta', property='dc:title', itemprop='name', lang='en').get_text("|")
            elements = title.split("|")
            for element in elements:
                if len(element) > 1:
                    short_title = element
                    # print(short_title)
                    break
            place_refs = soup.find_all('a', {"class": "place"})
            for ref in place_refs:
                link = ref['about'].split("/")[-1]
                topos_places[short_title].append(link)
        else:
            continue
    print("Parsed " + str(len(topos_places)) + " documents.")
    print("Converting data to long format...")
    long_data = _convert_dict_to_long(topos_places)

    return pd.DataFrame(long_data, columns=[['author', 'text', 'place_ref']])


def _add_pleiades_ids(topos_place_refs_dataframe):
    """
    Swap all IDs to Pleiades IDs if possible

    Parameters
    ----------
    topos_df : dataframe
        a dataframe with data from the Topos Text Gazeteer

    topos_places : dictionary
        a dictionary with key=texts and value=list of Topos Text IDs

    Returns
    -------
    dictionary
        dictionary with key=texts and value=list of Pleiades IDs, where possible

    Notes
    -----
    This method reports how many IDs were unable to be switched. In the case that there is no
    corresponding Pleiades ID for a given Topos Text ID, the Topos Text ID is retained in the dictionary.
    """
    def _topos_pleiades_ids(df, key_selector='topos'):

        topos_pleiades_ids = {}
        pleiades_topos_ids = {}
        
        for location in range(len(df['features'])):
            pleiades_link = None
            pleiades_id = None
            if 'links' in df['features'][location]:
                if df['features'][location]['links'][0]:
                    pleiades_link = df['features'][location]['links'][0]['identifier']
            topos_link = df['features'][location]['@id']
            if pleiades_link and 'pleiades' in pleiades_link:
                pleiades_id = pleiades_link.split("/")[-1]
            topos_id = topos_link.split("/")[-1]
            topos_pleiades_ids[topos_id] = pleiades_id
            if pleiades_id:
                pleiades_topos_ids[pleiades_id] = topos_id
        if key_selector == 'topos':
            return topos_pleiades_ids
        else:
            return pleiades_topos_ids
    

    def _from_json_get_topos_df(file_name="CATK/src/CATK/data/ToposTextGazetteer.jsonld"):
        """
        Loads the Topos Text Gazeteer JSON file into a DataFrame.

        Args:
            file_name (str): name of the Topos Text JSON file

        Returns:
            dataframe: A dataframe with data from the Topos Text Gazeteer
        """
        file = open(file_name, "r+", encoding="utf8")
        df = json.load(file)
        return df


    ids = _topos_pleiades_ids(_from_json_get_topos_df())

    def swap_id(topos_ID):
        if topos_ID in ids.keys():
            return ids[topos_ID]
        else:
            return '0' # does not have a pleiades equivalent

    topos_place_refs_dataframe['pleiades_id'] = topos_place_refs_dataframe['place_ref'].apply(swap_id)
    return topos_place_refs_dataframe
