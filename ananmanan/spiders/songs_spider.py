import scrapy
import string
import functools
import json

class SongsSpider(scrapy.Spider):
    name = "songs"

    def start_requests(self):
        base_url = 'http://www.ananmanan.lk/free-sinhala-mp3/songs/songs-by-{}/{}'
        urls = []
        for letter in list(string.ascii_lowercase):
            for page_number in range(100):
                urls.append(base_url.format(letter,page_number))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        songs = []
        for i in range(3,33):
            song_page_href_rel = response.css("#content > div:nth-child({}) > a::attr(href)".format(i)).extract_first()
            song_page_href='http://www.ananmanan.lk/free-sinhala-mp3/'
            href_blocks = song_page_href_rel.split("/")
            # for i in range(2,len(song_page_href)):
            #     song_page_href +=href_blocks[i] + "/"
            song_page_href = song_page_href+functools.reduce(lambda x,y:x+"/"+y,href_blocks[2:])
            print(song_page_href)
            yield scrapy.Request(url=song_page_href,callback=self.songPageParse)

    def songPageParse(self,response):
        song_title = response.css("#content > div.songdetailsgp > div:nth-child(2)::text").extract_first()
        song_artist = response.css("#content > div.songdetailsgp > div:nth-child(5) > a::text").extract_first()
        song_lyrics = response.css("#content > div.songdetailsgp > div:nth-child(7)::text").extract_first()
        song_music = response.css("#content > div.songdetailsgp > div:nth-child(9)::text").extract_first()
        song_added_date = response.css("#content > div.songdetailsgp > div.stats > strong:nth-child(1)::text").extract_first()
        song_downloads = response.css("#content > div.songdetailsgp > div.stats > strong:nth-child(2)::text").extract_first()
        song_listens = response.css("#content > div.songdetailsgp > div.stats > strong:nth-child(3)::text").extract_first()
        song_mobile_download_path = response.css("#content > div.songdetailsgp > div.downloadiconsgp > div:nth-child(1) > a::attr(href)").extract_first()
        song_mp3_download_path = response.css("#content > div.songdetailsgp > div.downloadiconsgp > div:nth-child(2) > a::attr(href)").extract_first()
        song_zip_download_path = response.css("#content > div.songdetailsgp > div.downloadiconsgp > div:nth-child(3) > a::attr(href)").extract_first()
        song_online_listen_path = response.css("#content > div.songdetailsgp > div.downloadiconsgp > div:nth-child(4) > a::attr(href)").extract_first()
        # content > div.songdetailsgp > div.stats > strong:nth-child(1)

        song_page_href = 'http://www.ananmanan.lk/free-sinhala-mp3/'
        href_blocks = song_mobile_download_path.split("/")
        song_mobile_download_path = song_page_href + functools.reduce(lambda x, y: x + "/" + y, href_blocks[2:])

        href_blocks = song_zip_download_path.split("/")
        song_zip_download_path = song_page_href + functools.reduce(lambda x, y: x + "/" + y, href_blocks[2:])

        href_blocks = song_online_listen_path.split("/")
        song_online_listen_path = song_page_href + functools.reduce(lambda x, y: x + "/" + y, href_blocks[2:])

        song={'title'   :   song_title,
              'artist'  :   song_artist,
              'lyrics'  :   song_lyrics,
              'music'   :   song_music,
              'added_date': song_added_date,
              'downloads' : song_downloads,
              'listens' :   song_listens,
              'mobile_download_path': song_mobile_download_path,
              'mp3_download_path':  song_mp3_download_path,
              'zip_download_path'   :   song_zip_download_path,
              'online_listen_path'  :   song_online_listen_path,
              'song_page'   : response.url,
              }
        print(song)

        data_file = open("songs_by_alphabet.json", "a+")
        data_file.write(json.dumps(song, indent=2, sort_keys=True))
        data_file.write(",\n")
        data_file.close()