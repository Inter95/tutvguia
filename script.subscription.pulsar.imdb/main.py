# coding: utf-8
from tools import *

# option
option = settings.dialog.select(settings.string(32100), # Choose Category
                                [settings.string(32150),  #Genre
                                 settings.string(32151),  #Language
                                 settings.string(32101),  #List
                                 settings.string(32110),  #Watchlist
                                 settings.string(32152),  # Popular and Oscar Winner
                                 settings.string(32153),  # TOP 250
                                 settings.string(32154),  # Keywords
                                 settings.string(32016),  # SETTINGS
                                 settings.string(32017),  # -HELP
                                 settings.string(32018)  # Exit
                                 ])

if option == 0:
    genre = {'Action': 'http://www.imdb.com/genre/action/?ref_=gnr_mn_ac_mp',
             'Action Comedy': 'http://www.imdb.com/search/title?count=100&genres=action,comedy&num_votes=10000,&title_type=feature&ref_=gnr_mn_ac_1',
             'Action Crime': 'http://www.imdb.com/search/title?count=100&genres=action,crime&num_votes=10000,&title_type=feature&ref_=gnr_mn_ac_2',
             'Action Thriller': 'http://www.imdb.com/search/title?count=100&genres=action,thriller&num_votes=10000,&title_type=feature&ref_=gnr_mn_ac_3',
             'Animation': 'http://www.imdb.com/genre/animation/?ref_=gnr_mn_an_mp',
             'Animation Adventure': 'http://www.imdb.com/search/title?count=100&genres=animation,adventure&num_votes=10000,&title_type=feature&ref_=gnr_mn_an_1',
             'Animation Comedy': 'http://www.imdb.com/search/title?count=100&genres=animation,comedy&num_votes=10000,&title_type=feature&ref_=gnr_mn_an_2',
             'Animation Family': 'http://www.imdb.com/search/title?count=100&genres=animation,family&num_votes=10000,&title_type=feature&ref_=gnr_mn_an_3',
             'Animation Fantasy': 'http://www.imdb.com/search/title?count=100&genres=animation,fantasy&num_votes=10000,&title_type=feature&ref_=gnr_mn_an_4',
             'Comedy': 'http://www.imdb.com/genre/comedy/?ref_=gnr_mn_co_mp',
             'Comedy Action': 'http://www.imdb.com/search/title?count=100&genres=comedy,action&num_votes=10000,&title_type=feature&ref_=gnr_mn_co_1',
             'Comedy Horror': 'http://www.imdb.com/search/title?count=100&genres=comedy,horror&num_votes=10000,&title_type=feature&ref_=gnr_mn_co_2',
             'Comedy Romance': 'http://www.imdb.com/search/title?count=100&genres=comedy,romance&num_votes=10000,&title_type=feature&ref_=gnr_mn_co_3',
             'Documentary': 'http://www.imdb.com/genre/documentary/?ref_=gnr_mn_do_mp',
             'Documentary Biography': 'http://www.imdb.com/search/title?count=100&genres=documentary,biography&num_votes=1000,&title_type=documentary&ref_=gnr_mn_do_1',
             'Documentary Comedy': 'http://www.imdb.com/search/title?count=100&genres=documentary,comedy&num_votes=1000,&title_type=documentary&ref_=gnr_mn_do_2',
             'Documentary Crime': 'http://www.imdb.com/search/title?count=100&genres=documentary,crime&num_votes=1000,&title_type=documentary&ref_=gnr_mn_do_3',
             'Documentary History': 'http://www.imdb.com/search/title?count=100&genres=documentary,history&num_votes=1000,&title_type=documentary&ref_=gnr_mn_do_4',
             'Family': 'http://www.imdb.com/genre/family/?ref_=gnr_mn_fm_mp',
             'Family Adventure': 'http://www.imdb.com/search/title?count=100&genres=family,adventure&num_votes=10000,&title_type=feature&ref_=gnr_mn_fm_1',
             'Family Comedy': 'http://www.imdb.com/search/title?count=100&genres=family,comedy&num_votes=10000,&title_type=feature&ref_=gnr_mn_fm_2',
             'Family Fantasy': 'http://www.imdb.com/search/title?count=100&genres=family,fantasy&num_votes=10000,&title_type=feature&ref_=gnr_mn_fm_3',
             'Family Romance': 'http://www.imdb.com/search/title?count=100&genres=family,romance&num_votes=10000,&title_type=feature&ref_=gnr_mn_fm_4',
             'Film-Noir': 'http://www.imdb.com/genre/film_noir/?ref_=gnr_mn_fn_mp',
             'Film-Noir Crime': 'http://www.imdb.com/search/title?count=100&genres=film_noir,crime&num_votes=10000,&title_type=feature&ref_=gnr_mn_fn_1',
             'Film-Noir Mystery': 'http://www.imdb.com/search/title?count=100&genres=film_noir,mystery&num_votes=10000,&title_type=feature&ref_=gnr_mn_fn_2',
             'Film-Noir Romance': 'http://www.imdb.com/search/title?count=100&genres=film_noir,romance&num_votes=10000,&title_type=feature&ref_=gnr_mn_fn_3',
             'Film-Noir Thriller': 'http://www.imdb.com/search/title?count=100&genres=film_noir,thriller&num_votes=10000,&title_type=feature&ref_=gnr_mn_fn_4',
             'Horror': 'http://www.imdb.com/genre/horror/?ref_=gnr_mn_ho_mp',
             'Horror Comedy': 'http://www.imdb.com/search/title?count=100&genres=horror,comedy&num_votes=10000,&title_type=feature&ref_=gnr_mn_ho_1',
             'Horror Drama': 'http://www.imdb.com/search/title?count=100&genres=horror,drama&num_votes=10000,&title_type=feature&ref_=gnr_mn_ho_2',
             'Horror Sci-fi': 'http://www.imdb.com/search/title?count=100&genres=horror,sci_fi&num_votes=10000,&title_type=feature&ref_=gnr_mn_ho_3',
             'Musical': 'http://www.imdb.com/genre/musical/?ref_=gnr_mn_ml_mp',
             'Musical Comedy': 'http://www.imdb.com/search/title?count=100&genres=musical,comedy&num_votes=10000,&title_type=feature&ref_=gnr_mn_ml_1',
             'Musical History': 'http://www.imdb.com/search/title?count=100&genres=musical,history&num_votes=10000,&title_type=feature&ref_=gnr_mn_ml_2',
             'Musical Romance': 'http://www.imdb.com/search/title?count=100&genres=musical,romance&num_votes=10000,&title_type=feature&ref_=gnr_mn_ml_3',
             'Romance': 'http://www.imdb.com/genre/romance/?ref_=gnr_mn_ro_mp',
             'Romance Comedy': 'http://www.imdb.com/search/title?count=100&genres=romance,comedy&num_votes=10000,&title_type=feature&ref_=gnr_mn_ro_1',
             'Romance Crime': 'http://www.imdb.com/search/title?count=100&genres=romance,crime&num_votes=10000,&title_type=feature&ref_=gnr_mn_ro_2',
             'Romance History': 'http://www.imdb.com/search/title?count=100&genres=romance,history&num_votes=10000,&title_type=feature&ref_=gnr_mn_ro_3',
             'Romance Thriller': 'http://www.imdb.com/search/title?count=100&genres=romance,thriller&num_votes=10000,&title_type=feature&ref_=gnr_mn_ro_4',
             'Sport': 'http://www.imdb.com/genre/sport/?ref_=gnr_mn_sp_mp',
             'Sport Biography': 'http://www.imdb.com/search/title?count=100&genres=sport,biography&num_votes=10000,&title_type=feature&ref_=gnr_mn_sp_1',
             'Sport Comedy': 'http://www.imdb.com/search/title?count=100&genres=sport,comedy&num_votes=10000,&title_type=feature&ref_=gnr_mn_sp_2',
             'Sport Documentary': 'http://www.imdb.com/search/title?count=100&genres=sport,documentary&num_votes=1000,&title_type=documentary&ref_=gnr_mn_sp_3',
             'War': 'http://www.imdb.com/genre/war/?ref_=gnr_mn_wa_mp',
             'War Action': 'http://www.imdb.com/search/title?count=100&genres=war,action&num_votes=10000,&title_type=feature&ref_=gnr_mn_wa_1',
             'War Biography': 'http://www.imdb.com/search/title?count=100&genres=war,biography&num_votes=10000,&title_type=feature&ref_=gnr_mn_wa_2',
             'War Comedy': 'http://www.imdb.com/search/title?count=100&genres=war,comedy&num_votes=10000,&title_type=feature&ref_=gnr_mn_wa_3',
             'War Documentary': 'http://www.imdb.com/search/title?count=100&genres=war,documentary&num_votes=1000,&title_type=documentary&ref_=gnr_mn_wa_4',
             'Adventure': 'http://www.imdb.com/genre/adventure/?ref_=gnr_mn_ad_mp',
             'Adventure Biography': 'http://www.imdb.com/search/title?count=100&genres=adventure,biography&num_votes=10000,&title_type=feature&ref_=gnr_mn_ad_1',
             'Adventure Thriller': 'http://www.imdb.com/search/title?count=100&genres=adventure,thriller&num_votes=10000,&title_type=feature&ref_=gnr_mn_ad_2',
             'Adventure War': 'http://www.imdb.com/search/title?count=100&genres=adventure,war&num_votes=10000,&title_type=feature&ref_=gnr_mn_ad_3',
             'Biography': 'http://www.imdb.com/genre/biography/?ref_=gnr_mn_bi_mp',
             'Biography Crime': 'http://www.imdb.com/search/title?count=100&genres=biography,crime&num_votes=10000,&title_type=feature&ref_=gnr_mn_bi_1',
             'Biography Mystery': 'http://www.imdb.com/search/title?count=100&genres=biography,mystery&num_votes=5000,&title_type=feature&ref_=gnr_mn_bi_2',
             'Biography Sport': 'http://www.imdb.com/search/title?count=100&genres=biography,sport&num_votes=10000,&title_type=feature&ref_=gnr_mn_bi_3',
             'Crime': 'http://www.imdb.com/genre/crime/?ref_=gnr_mn_cr_mp',
             'Crime Drama': 'http://www.imdb.com/search/title?count=100&genres=crime,drama&num_votes=10000,&title_type=feature&ref_=gnr_mn_cr_1',
             'Crime Mystery': 'http://www.imdb.com/search/title?count=100&genres=crime,mystery&num_votes=10000,&title_type=feature&ref_=gnr_mn_cr_2',
             'Crime Romance': 'http://www.imdb.com/search/title?count=100&genres=crime,romance&num_votes=10000,&title_type=feature&ref_=gnr_mn_cr_3',
             'Drama': 'http://www.imdb.com/genre/drama/?ref_=gnr_mn_dr_mp',
             'Drama Romance': 'http://www.imdb.com/search/title?count=100&genres=drama,romance&num_votes=10000,&title_type=feature&ref_=gnr_mn_dr_1',
             'Drama Film-Noir': 'http://www.imdb.com/search/title?count=100&genres=drama,film_noir&num_votes=10000,&title_type=feature&ref_=gnr_mn_dr_2',
             'Drama Musical': 'http://www.imdb.com/search/title?count=100&genres=drama,musical&num_votes=10000,&title_type=feature&ref_=gnr_mn_dr_3',
             'Drama War': 'http://www.imdb.com/search/title?count=100&genres=drama,war&num_votes=10000,&title_type=feature&ref_=gnr_mn_dr_4',
             'Fantasy': 'http://www.imdb.com/genre/fantasy/?ref_=gnr_mn_fa_mp',
             'Fantasy Adventure': 'http://www.imdb.com/search/title?count=100&genres=fantasy,adventure&num_votes=10000,&title_type=feature&ref_=gnr_mn_fa_1',
             'Fantasy Comedy': 'http://www.imdb.com/search/title?count=100&genres=fantasy,comedy&num_votes=10000,&title_type=feature&ref_=gnr_mn_fa_2',
             'Fantasy Drama': 'http://www.imdb.com/search/title?count=100&genres=fantasy,drama&num_votes=10000,&title_type=feature&ref_=gnr_mn_fa_3',
             'Fantasy Romance': 'http://www.imdb.com/search/title?count=100&genres=fantasy,romance&num_votes=10000,&title_type=feature&ref_=gnr_mn_fa_4',
             'History': 'http://www.imdb.com/genre/history/?ref_=gnr_mn_hi_mp',
             'History Adventure': 'http://www.imdb.com/search/title?count=100&genres=history,adventure&num_votes=10000,&title_type=feature&ref_=gnr_mn_hi_1',
             'History Biography': 'http://www.imdb.com/search/title?count=100&genres=history,biography&num_votes=10000,&title_type=feature&ref_=gnr_mn_hi_2',
             'History Drama': 'http://www.imdb.com/search/title?count=100&genres=history,drama&num_votes=10000,&title_type=feature&ref_=gnr_mn_hi_3',
             'History War': 'http://www.imdb.com/search/title?count=100&genres=history,war&num_votes=10000,&title_type=feature&ref_=gnr_mn_hi_4',
             'Music': 'http://www.imdb.com/genre/music/?ref_=gnr_mn_mu_mp',
             'Music Biography': 'http://www.imdb.com/search/title?count=100&genres=music,biography&num_votes=10000,&title_type=feature&ref_=gnr_mn_mu_1',
             'Music Documentary': 'http://www.imdb.com/search/title?count=100&genres=documentary,music&num_votes=750,&title_type=documentary&ref_=gnr_mn_mu_2',
             'Music Drama': 'http://www.imdb.com/search/title?count=100&genres=music,drama&num_votes=10000,&title_type=feature&ref_=gnr_mn_mu_3',
             'Mystery': 'http://www.imdb.com/genre/mystery/?ref_=gnr_mn_my_mp',
             'Mystery Adventure': 'http://www.imdb.com/search/title?count=100&genres=mystery,adventure&num_votes=10000,&title_type=feature&ref_=gnr_mn_my_1',
             'Mystery Comedy': 'http://www.imdb.com/search/title?count=100&genres=mystery,comedy&num_votes=10000,&title_type=feature&ref_=gnr_mn_my_2',
             'Mystery Thriller': 'http://www.imdb.com/search/title?count=100&genres=mystery,thriller&num_votes=10000,&title_type=feature&ref_=gnr_mn_my_3',
             'Sci-fi': 'http://www.imdb.com/genre/sci_fi/?ref_=gnr_mn_sf_mp',
             'Sci-fi Animation': 'http://www.imdb.com/search/title?count=100&genres=sci_fi,animation&num_votes=10000,&title_type=feature&ref_=gnr_mn_sf_1',
             'Sci-fi Comedy': 'http://www.imdb.com/search/title?count=100&genres=sci_fi,comedy&num_votes=10000,&title_type=feature&ref_=gnr_mn_sf_2',
             'Sci-fi Family': 'http://www.imdb.com/search/title?count=100&genres=sci_fi,family&num_votes=10000,&title_type=feature&ref_=gnr_mn_sf_3',
             'Sci-fi Horror': 'http://www.imdb.com/search/title?count=100&genres=sci_fi,horror&num_votes=10000,&title_type=feature&ref_=gnr_mn_sf_4',
             'Thriller': 'http://www.imdb.com/genre/thriller/?ref_=gnr_mn_th_mp',
             'Thriller Comedy': 'http://www.imdb.com/search/title?count=100&genres=thriller,comedy&num_votes=10000,&title_type=feature&ref_=gnr_mn_th_1',
             'Thriller Crime': 'http://www.imdb.com/search/title?count=100&genres=thriller,crime&num_votes=10000,&title_type=feature&ref_=gnr_mn_th_2',
             'Thriller Horror': 'http://www.imdb.com/search/title?count=100&genres=thriller,horror&num_votes=10000,&title_type=feature&ref_=gnr_mn_th_3',
             'Thriller Mystery': 'http://www.imdb.com/search/title?count=100&genres=thriller,mystery&num_votes=10000,&title_type=feature&ref_=gnr_mn_th_4',
             'Western': 'http://www.imdb.com/genre/western/?ref_=gnr_mn_we_mp',
             'Western Action': 'http://www.imdb.com/search/title?count=100&genres=western,action&num_votes=10000,&title_type=feature&ref_=gnr_mn_we_1',
             'Western Adventure': 'http://www.imdb.com/search/title?count=100&genres=western,adventure&num_votes=10000,&title_type=feature&ref_=gnr_mn_we_2',
             'Western Comedy': 'http://www.imdb.com/search/title?count=100&genres=western,comedy&num_votes=10000,&title_type=feature&ref_=gnr_mn_we_3',
             }
    options = genre.keys()
    options.sort()
    ret = settings.dialog.select(settings.string(32010), options + ['CANCEL'])
    if ret < len(options):
        urlSearch = genre[options[ret]]
        listing = []
        ID = []  # IMDB_ID or thetvdb ID
        settings.notification(settings.string(32044))
        settings.log(urlSearch)
        response = browser.get(urlSearch)
        if response.status_code == requests.codes.ok:
            data = response.text
            for line in re.findall('<span class="wlb_wrapper"(.*?)</div>', data, re.S):
                items = re.search('/title/(.*?)/(.*?)>(.*?)<', line)
                year = re.search('<span class="year_type">(.*?)<', line)
                ID.append(items.group(1))
                listing.append(items.group(3) + ' ' + year.group(1))
            subscription(listing, ID, 'MOVIE', settings.movieFolder)
        else:
            settings.log(">>>>>>>HTTP %s<<<<<<<" % response.status_code)
            settings.notification(message="HTTP %s" % response.status_code, force=True)

elif option == 1:  # language
    language = {'Arabic': 'ar', 'Bulgarian': 'bg', 'Chinese': 'zh', 'Croatian': 'hr',
                'Dutch': 'nl', 'English': 'en', 'Finnish': 'fi', 'French': 'fr',
                'German': 'de', 'Greek': 'el', 'Hebrew': 'he', 'Hindi': 'hi',
                'Hungarian': 'hu', 'Icelandic': 'is', 'Italian': 'it', 'Japanese': 'ja',
                'Korean': 'ko', 'Norwegian': 'no', 'Persian': 'fa', 'Polish': 'pl',
                'Portuguese': 'pt', 'Punjabi': 'pa', 'Romanian': 'ro', 'Russian': 'ru',
                'Spanish': 'es', 'Swedish': 'sv', 'Turkish': 'tr', 'Ukrainian': 'uk',
                }
    options = language.keys()
    options.sort()
    ret = settings.dialog.select('Choose a language', options + ['CANCEL'])
    if ret < len(options):
        urlSearch = 'http://www.imdb.com/search/title?languages=%s|1&sort=moviemeter,asc&start=1&title_type=feature' % \
                    language[options[ret]]
        listing = []
        ID = []  # IMDB_ID or thetvdb ID
        settings.notification(settings.string(32044))
        settings.log(urlSearch)
        response = browser.get(urlSearch)
        if response.status_code == requests.codes.ok:
            data = response.text
            for line in re.findall('<span class="wlb_wrapper"(.*?)</div>', data, re.S):
                items = re.search('/title/(.*?)/(.*?)>(.*?)<', line)
                year = re.search('<span class="year_type">(.*?)<', line)
                ID.append(items.group(1))
                listing.append(items.group(3) + ' ' + year.group(1))
            subscription(listing, ID, 'MOVIE', settings.movieFolder, message=options[ret])
        else:
            settings.log(">>>>>>>HTTP %s<<<<<<<" % response.status_code)
            settings.notification(message="HTTP %s" % response.status_code, force=True)

elif option == 2:  # list
    default = settings.settings.getSetting('list')
    if default == '': default = 'ls00000000'
    list = settings.dialog.input('IMDB List to add:', default)
    if list != '':
        start = 1
        movieListing = []
        showListing = []
        movieID = []  # IMDB_ID or thetvdb ID
        TV_ID = []  # IMDB_ID or thetvdb ID
        while True:
            urlSearch = "http://www.imdb.com/list/%s/?start=%d&view=detail&sort=listorian:asc" % (list, start)
            settings.notification(settings.string(32044))  # Checking Online
            settings.log(urlSearch)
            response = browser.get(urlSearch)
            if response.status_code == requests.codes.ok:
                data = response.text
                lines = re.findall('<div class="info">(.*?)</div>', data, re.S)
                if len(lines) > 0:
                    for line in re.findall('<div class="info">(.*?)</div>', data, re.S):
                        if 'This title is no longer available' not in line:  # prevent the error with not info
                            items = re.search('/title/(.*?)/(.*?)>(.*?)<', line)
                            year = re.search('<span class="year_type">(.*?)<', line)
                            if 'TV Series' in year.group(1) or 'Mini-Series' in year.group(1):
                                showListing.append(items.group(3))  # without year
                                TV_ID.append(items.group(1))
                            else:
                                movieListing.append(items.group(3) + ' ' + year.group(1))
                                movieID.append(items.group(1))
                    start += 100
                else:
                    break
            else:
                settings.log(">>>>>>>HTTP %s<<<<<<<" % response.status_code)
                settings.notification(message="HTTP %s" % response.status_code, force=True)
                break
        if len(movieListing) > 0:
            subscription(movieListing, movieID, 'MOVIE', settings.movieFolder, message="List")
        if len(showListing) > 0:
            subscription(showListing, [], 'SHOW', settings.showFolder, message="List")

elif option == 3:  # watchlist
    default = settings.settings.getSetting('user')
    if default == '': default = 'ur0000000'
    user = settings.dialog.input('IMDB user code:', default)
    if user != '':
        urlSearch = "http://www.imdb.com/user/%s/watchlist" % user
        settings.notification(settings.string(32044))  # Checking Online
        response = browser.get(urlSearch)
        if response.status_code == requests.codes.ok:
            data = response.text
            list = re.findall('/list/export.list_id=(.*?)&', data)
            if list != []:
                start = 1
                movieListing = []
                showListing = []
                movieID = []  # IMDB_ID or thetvdb ID
                TV_ID = []  # IMDB_ID or thetvdb ID
                while True:
                    urlSearch = "http://www.imdb.com/list/%s/?start=%d&view=detail&sort=listorian:asc" % (
                    list[0], start)
                    settings.notification(settings.string(32044))  # Checking Online
                    settings.log(urlSearch)
                    response = browser.get(urlSearch)
                    if response.status_code == requests.codes.ok:
                        data = response.text
                        lines = re.findall('<div class="info">(.*?)</div>', data, re.S)
                        if len(lines) > 0:
                            for line in re.findall('<div class="info">(.*?)</div>', data, re.S):
                                if 'This title is no longer available' not in line:  # prevent the error with not info
                                    items = re.search('/title/(.*?)/(.*?)>(.*?)<', line)
                                    year = re.search('<span class="year_type">(.*?)<', line)
                                    if 'TV Series' in year.group(1) or 'Mini-Series' in year.group(1):
                                        showListing.append(items.group(3))  # without year
                                        TV_ID.append(items.group(1))
                                    else:
                                        movieListing.append(items.group(3) + ' ' + year.group(1))
                                        movieID.append(items.group(1))
                            start += 100
                        else:
                            break
                    else:
                        settings.log(">>>>>>>HTTP %s<<<<<<<" % response.status_code)
                        settings.notification(message="HTTP %s" % response.status_code, force=True)
                        break
                if len(movieListing) > 0:
                    subscription(movieListing, movieID, 'MOVIE', settings.movieFolder, message="Watchlist")
                if len(showListing) > 0:
                    subscription(showListing, [], 'SHOW', settings.showFolder, message="Watchlist")


elif option == 4:  # popular
    types = {'Feature Films': 'http://www.imdb.com/search/title?count=100&title_type=feature&ref_=nv_ch_mm_1',
             'Feature Films/TV Movies': 'http://www.imdb.com/search/title?count=100&title_type=feature,tv_movie&ref_=nv_ch_mm_1',
             'TV Movies': 'http://www.imdb.com/search/title?count=100&title_type=tv_movie&ref_=nv_ch_mm_1',
             'Oscar Winners': 'http://www.imdb.com/search/title?count=100&groups=oscar_best_picture_winners&sort=year,desc&ref_=nv_ch_osc_3'
             }
    options = types.keys()
    options.sort()
    ret = settings.dialog.select('Choose a language', options + ['CANCEL'])
    if ret < len(options):
        urlSearch = types[options[ret]]
        listing = []
        ID = []  # IMDB_ID or thetvdb ID
        settings.notification(settings.string(32044))  # Checking Online
        settings.log(urlSearch)
        response = browser.get(urlSearch)
        if response.status_code == requests.codes.ok:
            data = response.text
            for line in re.findall('<span class="wlb_wrapper"(.*?)</div>', data, re.S):
                items = re.search('/title/(.*?)/(.*?)>(.*?)<', line)
                year = re.search('<span class="year_type">(.*?)<', line)
                ID.append(items.group(1))
                listing.append(items.group(3) + ' ' + year.group(1))
            subscription(listing, ID, 'MOVIE', settings.movieFolder,
                         message=options[ret])
        else:
            settings.log(">>>>>>>HTTP %s<<<<<<<" % response.status_code)
            settings.notification(message="HTTP %s" % response.status_code, force=True)

elif option == 5:  # TOP 250
    urlSearch = 'http://www.imdb.com/chart/top?ref_=nv_ch_250_4'
    listing = []
    ID = []  # IMDB_ID or thetvdb ID
    settings.notification(settings.string(32044))  # Checking Online
    settings.log(urlSearch)
    response = browser.get(urlSearch)
    if response.status_code == requests.codes.ok:
        data = response.text
        for line in re.findall('<td class="titleColumn">(.*?)</td>', data, re.S):
            items = re.search('/title/(.*?)/(.*?)>(.*?)<', line, re.S)
            year = re.search('class="secondaryInfo">(.*?)<', line)
            ID.append(items.group(1))
            listing.append(items.group(3) + ' ' + year.group(1))
        subscription(listing, ID, 'MOVIE', settings.movieFolder,
                     message="TOP 250")
    else:
        settings.log(">>>>>>>HTTP %s<<<<<<<" % response.status_code)
        settings.notification(message="HTTP %s" % response.status_code, force=True)


elif option == 6:  # Keywords
    keywords = settings.dialog.input('Keywords:').replace(' ', '-')
    year1 = settings.dialog.input('From Year:')
    year2 = settings.dialog.input('To Year:')
    if keywords != '':
        start = 1
        movieListing = []
        showListing = []
        movieID = []  # IMDB_ID or thetvdb ID
        TV_ID = []  # IMDB_ID or thetvdb ID
        while True:
            urlSearch = "http://www.imdb.com/search/title?keywords=%s&sort=moviemeter,asc&start=%s&title_type=feature&year=%s,%s" \
                        % (keywords, start, year1, year2)
            settings.notification(settings.string(32044))  # Checking Online
            settings.log(urlSearch)
            response = browser.get(urlSearch)
            if response.status_code == requests.codes.ok:
                data = response.text
                lines = re.findall('<span class="wlb_wrapper"(.*?)</div>', data, re.S)
                if len(lines) > 0:
                    for line in lines:
                        items = re.search('/title/(.*?)/(.*?)>(.*?)<', line)
                        year = re.search('<span class="year_type">(.*?)<', line)
                        if 'TV Series' in year.group(1) or 'Mini-Series' in year.group(1):
                            showListing.append(items.group(3))  # without year
                            TV_ID.append(items.group(1))
                        else:
                            movieListing.append(items.group(3) + ' ' + year.group(1))
                            movieID.append(items.group(1))
                    start += 50
                else:
                    break
            else:
                settings.log(">>>>>>>HTTP %s<<<<<<<" % response.status_code)
                settings.notification(message="HTTP %s" % response.status_code, force=True)
                break

        if len(movieListing) > 0:
            subscription(movieListing, movieID, 'MOVIE', settings.movieFolder, message=keywords)
        if len(showListing) > 0:
            subscription(showListing, [], 'SHOW', settings.showFolder, message=keywords)

elif option == 7:  # Settings
    settings.settings.openSettings()

elif option == 8:  # Help
    settings.dialog.ok(settings.string(32017), settings.string(32025))

del settings
del browser
