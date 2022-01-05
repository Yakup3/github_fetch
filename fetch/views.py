from django.shortcuts import render
import requests
from fetch.models import Candidate
import re

# Create your views here.
def home(request):
    return render(request, 'home.html')

def response(request):
    
    # keyword user entered
    keyword = request.POST['keyword']
    # to store later use
    string_keyword = keyword
    # to modify to url and if entered randomly
    keyword = re.split(r'[`\-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?]', keyword)
    s = '+'
    keyword = s.join(keyword)

    arr = []
    total_count = 0
    page = 0

    # getting first page to get total count
    response = requests.get("https://api.github.com/search/repositories?q="+keyword+"&page=1&per_page=100").json()

    arr = response['items']
    dic = {}
    total_count = response['total_count']

    # copy the fetched data into dictionary and control if it already exist
    for i in arr:
        if i['id'] not in dic:
            dic[i['id']] = i

    # fetches data until length of dictionary reaches total count
    while len(dic) < total_count:
        
        # fetching data from each page
        response = requests.get("https://api.github.com/search/repositories?q="+keyword+"&page="+str(page)+"&per_page=100")

        if response.status_code != 200:
            break

        result = response.json()
        arr = result['items']

        # copy the feched data into dictionary and control if it already exist
        for i in arr:
            if i['id'] not in dic:
                dic[i['id']] = i

        page += 1

    # to get the values in dictionary
    new_arr = dic.values()

    # to save data into postgresql
    for i in new_arr:
        
        # getting needed information
        repo_name = i['full_name']
        repo_url = i['html_url']

        # if repos does not have description it saves as 'there is not description'
        if i['description'] == None:
            description = 'there is not description'
        else:
            description = i['description']
        repo_id = i['id']
        
        # to get the data if it already exist in database
        exist = Candidate.objects.filter(repo_id=repo_id)

        # check not to save if it already exist in database
        if exist.exists() == False:
            ins = Candidate(repo_name=repo_name, repo_url=repo_url, description=description, keyword=string_keyword, repo_id=repo_id)
            ins.save()

    # returns if there is not any data fetched
    if total_count == 0:
        return render(request, 'response.html', {'response': 0, 'result': len(new_arr), 'keyword': string_keyword})

    # returns fetched data
    return render(request, 'response.html', {'response': new_arr, 'result': len(new_arr), 'keyword': string_keyword})