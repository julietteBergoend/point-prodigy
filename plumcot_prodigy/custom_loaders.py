from plumcot_prodigy.forced_alignment import ForcedAlignment
import os
import json

def load_files(series, episode, path):
    """Load mkv and aligned files of the current episode,
       Return mkv path, aligned path and sentences of the current episode
    """
    path = "/vol/work1/bergoend/pyannote-db-plumcot/Plumcot/data/"
    forced_alignment = ForcedAlignment()
    
    # path to mkv
    if os.path.isfile(f"/vol/work3/lefevre/dvd_extracted/{series}/{episode}.mkv") : 
        mkv = f"/vol/work3/lefevre/dvd_extracted/{series}/{episode}.mkv"
    elif os.path.isfile(f"/vol/work1/maurice/dvd_extracted/{series}/{episode}.mkv") :
        mkv = f"/vol/work1/maurice/dvd_extracted/{series}/{episode}.mkv"
    else:
        mkv = ""
        print("No mkv file for", episode)
        
    # path to forced alignment        
    if os.path.isfile(f"{episode}.aligned"):
        aligned = f"{episode}.aligned"
        transcript = forced_alignment(aligned)      
        sentences = list(transcript.sents)
    else:
        aligned = ""
        sentences = ""
        print("No aligned file for", episode)

    return mkv, aligned, sentences  
    
def load_episodes(path): 
    """Load shows' episodes,
       Return episode list
    """

    # gather all episodes of all shows together
    all_episodes_series = ""
   
    # shows' names
    with open(os.path.join(path, "series.txt")) as series_file :
        series = series_file.read()
    #all_series = [serie.split(",")[0] for serie in series.split('\n') if serie != '']
    all_series = ['TheBigBangTheory']
    
    # shows' paths
    all_series_paths = [os.path.join(path, name) for name in all_series]
    
    # read episode.txt of each show
    for serie_name in all_series_paths:
        with open(os.path.join(serie_name,"episodes.txt")) as file:  
            episodes_file = file.read() 
            all_episodes_series += episodes_file
    
    # final list of all episodes (season x)
    #episodes_list = [episode.split(',')[0] for episode in all_episodes_series.split('\n') if 'Season01.' in episode]
    episodes_list = ['TheBigBangTheory.Season01.Episode07.aligned' ]

    return episodes_list

def load_credits(episode, series, path):
    
    path = "/vol/work1/bergoend/pyannote-db-plumcot/Plumcot/data/"
    with open(os.path.join(path, f"{series}/credits.txt")) as f_c:
        credits = f_c.read()

    # path to characters
    with open(os.path.join(path,f"{series}/characters.txt")) as f_ch:
          characters = f_ch.read()                  
    characters_list = [char.split(',')[0] for char in characters.split('\n') if char != '']

    # credits per episodes
    credits_dict = {ep.split(',')[0] : ep.split(',')[1:] for ep in credits.split('\n')}
    final_dict = {}
    for ep, credit in credits_dict.items():
        final_dict[ep] = [ch for ch, cr in zip(characters_list, credit) if cr == "1"]   

    # credits for the current episode
    episode_characters = final_dict[episode]
    
    return episode_characters
    
def load_photo(characters, serie_uri, path):  
    """Load photos for the show's characters
    """
    directory = "/vol/work1/bergoend/pyannote-db-plumcot"
    path = "/vol/work1/bergoend/pyannote-db-plumcot/Plumcot/data/"
    
    # open json file corresponding to the current show
    with open(os.path.join(path, f"{serie_uri}/images/images.json")) as f:
        data = json.load(f)
        
    # dictionary character : url to the character's picture
    char_pictures = {}
    # dictionaries for characters
    characters_dic = data['characters']
    
    # find centroid for each character in the current episode
    for character in characters : 
        #print(character)
        for name, val in characters_dic.items():
            
            # characters with a centroid
            if character == name and val['count'] != 0:
                try:
                    if val['centroid'] :
                        char_pictures[name] = val['centroid']
                        #print('centroid ',character)
                        
                # characters without centroid
                except KeyError:
                    char_pictures[name] = os.path.join(directory, val['paths'][0])
                    #print('photo ',character)
                    
            # characters without photo
            elif character == name and val['count'] == 0:
                char_pictures[name] = name
                #print('name ',character)
                
               
    return char_pictures 