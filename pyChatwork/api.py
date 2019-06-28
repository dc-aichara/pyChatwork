import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

class Chatwork(object):

    __API_URL_BASE = 'https://api.chatwork.com/v2'

    def __init__(self, api_token, api_base_url = __API_URL_BASE):
        """
        Initiate with base url and api token
        :param api_token:
        :param api_base_url:
        """
        self.api_base_url = api_base_url
        self.api_key = api_token
        self.endpoint = api_base_url
        self.headers = {'X-ChatWorkToken': self.api_key}
        self.request_timeout = 120
        self.session = requests.Session()
        retries = Retry(total=5, backoff_factor=0.5, status_forcelist=[502, 503, 504])
        self.session.mount('http://', HTTPAdapter(max_retries=retries))


    def get_me(self):
        """
        Get your account information.
        :return: your account information
        """
        try:
            get_url = '{}/me'.format(self.endpoint)
            response = requests.get(get_url,headers =self.headers)
            return response.json()
        except Exception as ex:
            print('Get me error - {}'.format(ex))

    def get_my_status(self):
        """
        Get the number of: unread messages, unread To messages, and unfinished tasks.
        :return: the number of: unread messages, unread To messages, and unfinished tasks
        """
        try:
            get_url = '{}/my/status'.format(self.endpoint)
            response = requests.get(get_url,headers =self.headers)
            return response.json()
        except Exception as ex:
            print('Get my status error - {}'.format(ex))

    def get_my_tasks(self):
        """
        Get list of all your unfinished tasks.
        :return: list of task if there is any other a json error
        """
        try:
            get_url = '{}/my/tasks?'.format(self.endpoint)
            response = requests.get(get_url,headers =self.headers)
            return response.json()
        except Exception as ex:
            print('Get my tasks error - {}'.format(ex))

    def get_contacts(self):
        """
        Get the list of your contacts.
        :return: list of your contacts
        """
        try:
            get_url = '{}/contacts'.format(self.endpoint)
            response = requests.get(get_url,headers =self.headers)
            return response.json()
        except Exception as ex:
            print('Get contacts error - {}'.format(ex))

    def get_rooms(self):
        """
        Get the list of all chats on your account.
        :return: list of all rooms
        """
        try:
            get_url = '{}/rooms'.format(self.endpoint)
            response = requests.get(get_url, headers=self.headers)
            return response.content, response.json()
        except Exception as ex:
            print('Get rooms error - {}'.format(ex))

    def send_message(self, room_id, message):
        """
        send message to a chat.
        :param room_id: Target chat's room id
        :param message: Your message
        :return: response 200 if it was successful
        """
        try:
            post_message_url = '{}/rooms/{}/messages'.format(self.endpoint, room_id, message)
            params = { 'body': message }
            response =  requests.post(post_message_url,
                                 headers=self.headers,
                                 params=params)
            return response
        except Exception as ex:
            print('Send message error - {}'.format(ex))

    def send_file(self, room_id, file_path, file_name,  message):
        """
        Send a file with message  to a chat.
        :param room_id: Target chat's room id
        :param file_path: file path
        :param file_name: Your file name
        :param message: Your message
        :return: response 200 if it was successful
        """
        try:
            post_message_url = '{}/rooms/{}/files'.format(self.endpoint, room_id)
            files = {'file': (file_name, open(file_path, 'rb')),'message': (None, message),}
            response = requests.post(post_message_url,
                                 headers=self.headers,
                                 files=files)
            return response
        except Exception as ex:
            print('Send file error - {}'.format(ex))

    def get_rooms_by_id(self, room_id):
        """
        Get chat name, icon, and Type (my, direct, or group)
        :param room_id: Target chat's room id
        :return: returns room id's details
        """
        try:
            get_url = '{}/rooms/{}'.format(self.endpoint, room_id)
            response = requests.get(get_url, headers=self.headers)
            return response.json()
        except Exception as ex:
            print('Get rooms by id error - {}'.format(ex))

    def delete_rooms_by_id(self, room_id, action):
        """
        Leave or delete a group chat.
        :param room_id: Target chat's room id
        :param action: leave or delete
        :return: none
        """
        data ={}
        data['action_type'] = action
        try:
            get_url = '{}/rooms/{}'.format(self.endpoint, room_id)
            response = requests.delete(get_url, data=data, headers=self.headers)
            return response
        except Exception as ex:
            print('Get rooms by id error - {}'.format(ex))

    def get_rooms_memebers(self, room_id):
        """
        Change associated members of group chat at once.
        :param room_id: Target chat's room id
        :return: returns all members information
        """
        try:
            get_url = '{}/rooms/{}/members'.format(self.endpoint, room_id)
            response = requests.get(get_url, headers=self.headers)
            return response.json()
        except Exception as ex:
            print('Get rooms members error - {}'.format(ex))

    def get_rooms_messages(self, room_id):
        """
        Get all messages associated with the specified chat (returns up to 100 entries).
        :param room_id: Target chat's room id
        :return: returns last 100 entries
        """
        try:
            get_url = '{}/rooms/{}/messages'.format(self.endpoint, room_id)
            response = requests.get(get_url, headers=self.headers)
            return response.json()
        except Exception as ex:
            print('Get rooms messages error - {}'.format(ex))

    def get_rooms_message_information(self, room_id, message_id):
        """
        Get information about the specified message.
        :param room_id: Target chat's room id
        :param message_id: message id of message which information is needed
        :return: returns information of specific message
        """
        try:
            get_url = '{}/rooms/{}/messages/{}'.format(self.endpoint, room_id, message_id)
            response = requests.get(get_url, headers=self.headers)
            return response.json()
        except Exception as ex:
            print('Get rooms message information error - {}'.format(ex))

    def add_rooms_task(self, room_id, task_name, time_limit, account_ids):
        """
         Add a new task to the chat.
        :param room_id: Target room id / chat id
        :param task_name: Task name (str)
        :param time_limit: time limit (integer) * Use Unix time as input
        :param account_ids: list of account ids (integer)
        :return: list of task ids
        """
        data = {}
        data['body'] = task_name
        data['limit'] = time_limit
        data['to_ids'] = account_ids

        try:
            get_url = '{}/rooms/{}/tasks'.format(self.endpoint, room_id)
            response = requests.post(get_url, data=data, headers=self.headers)
            return response.json()
        except Exception as ex:
            print('Add rooms task error - {}'.format(ex))

    def get_rooms_task_information(self, room_id, task_id):
        """
        Get information about the specified task.
        :param room_id: Target chat's room id
        :param task_id: Task id which information is needed
        :return: returns task information
        """
        try:
            get_url = '{}/rooms/{}/tasks/{}'.format(self.endpoint, room_id, task_id)
            response = requests.get(get_url, headers=self.headers)
            return response.json()
        except Exception as ex:
            print('Add rooms task information error - {}'.format(ex))

    def get_rooms_files(self, room_id):
        """
        Get the list of files associated with the specified chat.
        :param room_id: Target chat's room id
        :return: returns up to 100 entries of files
        """
        try:
            get_url = '{}/rooms/{}/files'.format(self.endpoint, room_id)
            response = requests.get(get_url, headers=self.headers)
            return response.json()
        except Exception as ex:
            print('Get rooms files error - {}'.format(ex))

    def get_rooms_file_information(self, room_id, file_id):
        """
        Get information about the specified file.
        :param room_id: Target chat's room id
        :param file_id: file id which information is needed
        :return: returns files information with a file download link
        """
        try:
            get_url = '{}/rooms/{}/files/{}?create_download_url=1'.format(self.endpoint, room_id, file_id)
            response = requests.get(get_url, headers=self.headers)
            return response.json()
        except Exception as ex:
            print('Get rooms file information error - {}'.format(ex))

    def create_new_room(self,description, memebers_memeber_ids, icon_preset, members_readonly_ids, members_admin_ids, name):
        """
        Create a new group chat
        :param description: Group description
        :param memebers_memeber_ids: member ids of group members
        :param icon_preset: group icon
                            [group, check, document, meeting, event, project, business, study,
                             security, star, idea, heart, magcup, beer, music, sports, travel]
        :param members_readonly_ids: read only ids
        :param members_admin_ids: admin ids
        :param name: Group name
        :return: response code
        """
        data = {}
        data['description'] = description
        data['memebers_memeber_ids'] = memebers_memeber_ids
        data['icon_preset'] = icon_preset
        data['members_readonly_ids'] = members_readonly_ids
        data['members_admin_ids'] = members_admin_ids
        data['name'] = name
        try:
            get_url = '{}/rooms'.format(self.endpoint)
            response = requests.post(get_url, data=data, headers=self.headers)
            return response
        except Exception as ex:
            print('Create chat group error -{}'.format(ex))

    def get_incoming_requests(self):
        """
        You can get the list of contact approval request you received.
        :return: return list of of contact approval request
        """
        try:
            get_url = '{}/incoming_requests'.format(self.endpoint)
            response = requests.get(get_url, headers=self.headers)
            return response.json()
        except Exception as ex:
            print('Get incoming requests error - {}'.format(ex))

    def approve_incoming_requests(self, request_id):
        """
        You can approve a contact approval request you received.
        :param request_id: Request id to be approved
        :return: request ids information
        """
        try:
            get_url = '{}/incoming_requests/{}'.format(self.endpoint, request_id)
            response = requests.put(get_url, headers=self.headers)
            return response.json()
        except Exception as ex:
            print('Approve  incoming requests error - {}'.format(ex))

    def delete_incoming_requests(self, request_id):
        """
        You can delete a contact approval request you received.
        :param request_id: Request id to be deleted
        :return: none
        """
        try:
            get_url = '{}/incoming_requests/{}'.format(self.endpoint, request_id)
            response = requests.delete(get_url, headers=self.headers)
            return response.json()
        except Exception as ex:
            print('Delete  incoming requests error - {}'.format(ex))

