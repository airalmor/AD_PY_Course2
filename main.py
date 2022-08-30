
import requests
import time
from tokens import acces_token  # импортирует значение токена
from pprint import pprint

TOKEN_VK = acces_token  # токен для запросов
age_from = 18  # значения из предпочтений пользователя
age_to = 60  # значения из предпочтений пользователя
sex = 1  # значения из предпочтений пользователя соответствует женскому полу
status = 2  # значения из предпочтений пользователя соответсвует статусу "не замужем"
city_id = 1


class Vk_user:

    def __init__(self, token):
        self.token = token

    def city_finder(self, name_city):
        token = TOKEN_VK
        URL = 'https://api.vk.com/method/database.getCities'
        params = {'access_token': token, 'v': '5.131', 'q': name_city, 'country_id': 1}
        city_info = requests.get(URL, params=params).json()
        return pprint(city_info)

    def get_user_info(self, vk_name):

        #выбрали по заданным параметрам пользователей
        #получили json с пользователями

        token = TOKEN_VK
        URL = 'https://api.vk.com/method/users.search'
        params = {

            # 'offset':200,
            'count': 100,
            'id': 710444639,  # здесь передается id пользователя, от кого запрашивается
            'access_token': token,  # токен пользователя
            'fields': ['photo_200'],
            'city': 1,
            'sex': sex,
            'status': status,
            'age_from': age_from,
            'age_to': age_to,
            'has_photo': 1,  # убирает пользователй без фото
            'is_closed': False,  # бесполезно, не работает
            'can_access_closed': False,
            'v': '5.131'
        }
        vk_info = requests.get(URL, params=params).json()['response']['items']

        return vk_info

    def get_user_pfotos(self, user_id):
        json_list = []
        likes_url_dict = {}
        like_list = []
        URL = 'https://api.vk.com/method/photos.get'
        params = {
            'access_token': TOKEN_VK,
            'album_id': 'profile',
            'v': '5.131',
            'owner_id': user_id,
            'extended': '1'
        }
        data = requests.get(URL, params=params).json()['response']['items']
        # return data

        likes_dict = {}
        for photo in data:
            photo_url = photo['sizes'][-1]['url']
            likes_dict[photo['likes']['count']] = photo_url

        sorted_likes_dict=list(sorted(likes_dict.items()))
        sorted_likes_dict.reverse()
        return print(sorted_likes_dict[0:3])


    def cleaning_from_mistakes(self,dirty_list):
        clean_list=[]
        for i in dirty_list:
            if i['is_closed'] == False:
                if i['can_access_closed'] == True:
                    clean_list.append(i)
        return clean_list


if __name__ == '__main__':
    vk = Vk_user(token=TOKEN_VK)
    all_list = vk.get_user_info(TOKEN_VK)
    cclean_list = vk.cleaning_from_mistakes(all_list)

    for a in cclean_list:
        print(a['id'],a['first_name'],a['last_name'], ' *******************************')
        vk.get_user_pfotos(a['id'])
        time.sleep(0.2)


