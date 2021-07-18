import urllib.parse

import requests

GOOD_RESPONSE_STATUS = 200
anilist_url = 'https://graphql.anilist.co'


class BadRequest(Exception):
    # status_code != GOOD_RESPONSE_STATUS
    pass


class NotFound(Exception):
    pass


class InvalidURL(Exception):
    pass


class AnimeFinder:
    # trace.moe-api
    @staticmethod
    def find_anilist_id(image_or_url, source_type):
        if source_type == 'url':
            if requests.get(image_or_url).status_code == GOOD_RESPONSE_STATUS:
                response = requests.get(
                    "https://api.trace.moe/search?cutBorders&url={}".format(
                        urllib.parse.quote_plus(image_or_url)))
            else:
                raise InvalidURL
        else:
            response = requests.post("https://api.trace.moe/search?cutBorders",
                                     files={'image': image_or_url})
        if response.status_code != GOOD_RESPONSE_STATUS:
            raise BadRequest
        if not response.json()['result'] or response.json()[
                'result'][0]['similarity'] < 0.9:
            raise NotFound
        return response.json()['result'][0]['anilist']

    # AniList Api v2
    @staticmethod
    def anilist_data_getter(anilist_id):
        # Under Media type in what to get
        query = '''
        query ($id: Int) {
          Media (id: $id, type: ANIME) {
            title {
              romaji
              english
            }
            description(asHtml: true)
            seasonYear
            coverImage {
                extraLarge
            }
            siteUrl
          }
        }
        '''

        variables = {
            'id': anilist_id
        }

        response = requests.post(
            anilist_url,
            json={
                'query': query,
                'variables': variables})
        if response.status_code != GOOD_RESPONSE_STATUS:
            raise BadRequest
        return response.json()['data']['Media']

    def __call__(self, image_or_url, source_type):
        anilist_id = self.find_anilist_id(image_or_url, source_type)
        return self.anilist_data_getter(anilist_id)
