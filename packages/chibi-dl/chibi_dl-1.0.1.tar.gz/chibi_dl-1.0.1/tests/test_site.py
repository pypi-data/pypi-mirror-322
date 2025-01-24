import itertools
import datetime
from unittest import TestCase, skip

from chibi.file import Chibi_path
from chibi.file.temp import Chibi_temp_path
from vcr_unittest import VCRTestCase
from chibi.atlas import Chibi_atlas, Atlas

from chibi_dl import Site


class Animeflv( Site ):
    url = 'https://www3.animeflv.net/'

    def parse_info( self ):
        episodes = self.soup.select_one( '.ListEpisodios' )
        info = Atlas( {} )
        info.last_episodes = []
        for episode in episodes.select( 'li' ):
            number = episode.select_one( '.Capi' ).text
            number = number.replace( 'Episode', '' ).strip()
            title = episode.select_one( '.Title' ).text
            link = episode.select_one( 'a' ).get( 'href' )
            link = self.build_url( self.url + link )
            info.last_episodes.append( {
                'number': number,
                'title': title,
                'link': link,
            } )

        return info


class Test_animeflv( VCRTestCase ):
    def setUp( self ):
        super().setUp()
        self.site = Animeflv()

    def test_when_init_the_site_should_no_open_the_browser( self ):
        self.assertFalse( self.site.is_browser_open )

    def test_info_should_return_last_chapter( self ):
        info = self.site.info
        self.assertTrue( info )

    def test_info_have_last_episodes( self ):
        info = self.site.info
        self.assertTrue( info.last_episodes )

    def test_url_in_last_episodes_should_be_absolute( self ):
        info = self.site.info
        for episode in info.last_episodes:
            self.assertIn( 'https://www3.animeflv.net', episode.link )
