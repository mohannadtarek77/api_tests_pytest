import requests
import pytest
from assertpy.assertpy import assert_that,soft_assertions
import random
import json
import jsonpath_ng

from json import dumps
from config import BASE_URI
from utils.print_helpers import pretty_print
from uuid import uuid4

from json import dumps, loads
from uuid import uuid4

from jsonpath_ng import parse
from utils.file_reader import read_file

def test_read_all_has_kent():
    response=requests.get(BASE_URI)
    peopleNames=response.json
    pretty_print(peopleNames)

    with soft_assertions():
        assert_that(response.status_code).is_equal_to(200)
        # first_names=[people['fname'] for people in peopleNames]
        # gives me a list of all of the first names 
        
        assert_that(peopleNames).extracting('fname').is_not_empty().contains('Kent')
# Get
def get_all_users():
    response=requests.get(BASE_URI)
    peopleNames=response.json()
    return peopleNames,response

# Post
def test_new_person_can_be_added():
    unique_last_name=create_new_unique_user()
    # f'User format: make string interpolation substitue bits of string to make it more readable

    payload =dumps({
        'fname':'New',
        'lname':unique_last_name
    })
    # dumps makes the serlization, which converts from python dictionary to json object

    headers={
        'Content-Type':'application/json',
        'Accept':'application/json'
    }

    response=requests.post(url=BASE_URI,data=payload,headers=headers)
    assert_that(response.status_code).is_equal_to(200)

    peopleNames=requests.get().json()
    new_users= search_users_by_last_name(peopleNames,unique_last_name)
    assert_that(new_users).is_not_empty()

    def search_users_by_last_name(peopleNames,unique_last_name):
        return [person for person in peopleNames if person['lname']==unique_last_name]
    
    def create_new_unique_user():
        return f'User {str(uuid4())}'
    # use uuid4 to get a unique string or use time stamps


    # Delete
    def test_person_can_deleted():
        new_user_last_name=create_new_unique_user()
        peopleNames=get_all_users()

        new_user, _=search_users_by_last_name(peopleNames,new_user_last_name)[0]

        print(new_user)
        person_to_be_deleted=new_user['person_id']
        url=f'{BASE_URI}'/{person_to_be_deleted}
        response=requests.delete(url)
        assert_that(response.status_code).is_equal_to(200)
    
    # Update
    def test_person_name_updated():
        response=requests.get('google/api/v1/search_bar')
        payloadPut =dumps({
        'fname':'New',
        'lname':'tarek'
        })

        headersPut = {'Content-Type': 'application/json', 'Authorization': 'Bearer your_access_token'}

        # Put request
        response=requests.put(url=BASE_URI,data=payloadPut,headers=headersPut)
        assert_that(response.status_code).is_equal_to(200)
        
        peopleNames=get_all_users
        new_users= search_users_by_last_name(peopleNames,'tarek')
        assert_that(new_users).is_not_empty()


    @pytest.fixture
    def create_data():
        payload = read_file('create_person.json')

        random_no = random.randint(0, 1000)
        last_name = f'Olabini{random_no}'

        payload['lname'] = last_name
        yield payload

    def test_person_can_be_added_with_a_json_template(create_data):
        create_new_unique_user(create_data)

        response = requests.get(BASE_URI)
        peoples = loads(response.text)

     
        jsonpath_expr = parse("$.[*].lname")
        result = [match.value for match in jsonpath_expr.find(peoples)]
        # Get all last names for any object in the root array
        # Here $ = root, [*] represents any element in the array

        expected_last_name = create_data['lname']
        assert_that(result).contains(expected_last_name)