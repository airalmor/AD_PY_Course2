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

        # выбрали по заданным параметрам пользователей
        # получили json с пользователями

        token = TOKEN_VK
        URL = 'https://api.vk.com/method/users.search'
        params = {

            # 'offset':200,
            'count': 3,
            'id': 710444639,  # здесь передается id пользователя, от кого запрашивается
            'access_token': token,  # токен пользователя
            # 'fields': ['id'],
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

    def get_user_pfotos_by_user_id(self, user_id):

        # получаем 3 id самых популярных фото

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

        likes_dict = {}
        for photo in data:
            photo_id = photo['id']
            photo_url = photo['sizes'][-1]['url']

            likes_dict[photo['likes']['count']] = photo_id

        sorted_likes_dict = list(sorted(likes_dict.items()))
        sorted_likes_dict.reverse()
        final_income = dict(sorted_likes_dict[0:3])
        final_income_2 = list(final_income.values())
        return final_income_2

    def cleaning_from_mistakes(self, dirty_list):
        clean_list = []
        for i in dirty_list:
            if i['is_closed'] == False:
                if i['can_access_closed'] == True:
                    clean_list.append(i)
        return clean_list

    def get_user_photo_by_photoid(self):
        pass

    def go_main(self):
        all_list = vk.get_user_info(TOKEN_VK)
        cclean_list = vk.cleaning_from_mistakes(all_list)
        ready_to_send = {}
        for a in cclean_list:
            photo_to_send_list = []
            time.sleep(0.2)
            for x in vk.get_user_pfotos_by_user_id(a['id']):
                photo_to_send = f"photo{a['id']}_{x}"
                photo_to_send_list.append(photo_to_send)
            ready_to_send[a['id']] = photo_to_send_list
        print(ready_to_send)
        return ready_to_send
        # получили словарб со значениями для messages.send

if __name__ == '__main__':
    vk = Vk_user(token=TOKEN_VK)
    vk.go_main()
