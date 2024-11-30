import requests


data = {
    'title': 'Title',
    'body': 'Body',
    'userId': 1
}

createResponse = requests.post('https://jsonplaceholder.typicode.com/posts', json=data)

if createResponse.status_code == 201:
    print("Post created:", createResponse.json())
else:
    print("Failed to create post:", createResponse.status_code)
    exit()


createdPostId = createResponse.json()['id']
print(createdPostId)
updated_data = {
    'title': 'Updated Title',
    'body': 'Updated Body',
    'userId': 1,
    'id': createdPostId
}

createdPostUrl = f'https://jsonplaceholder.typicode.com/posts/{createdPostId}'
updateResponse = requests.put(createdPostUrl, json=updated_data)

if updateResponse.status_code == 200:
    print("Post updated: ", updateResponse.json())
else:
    print("Failed to update post:", updateResponse.status_code)
    print(updateResponse.text)

response = requests.delete(createdPostUrl)

if response.status_code == 200:
    print("Post deleted")
else:
    print("Failed to delete post:", response.status_code)


response = requests.get('https://jsonplaceholder.typicode.com/posts')

if response.status_code == 200:
    filteredByTitles = [post for post in response.json() if len(post['title'].split()) > 6][:6]
    for post in filteredByTitles:
        print(post)

    print()
    filteredByBody = [post for post in response.json() if post['body'].count('\n') > 2][:3]
    for post in filteredByBody:
        print(post)
else:
    print(f'Something went wrong Code: {response.status_code}')
