import urllib.request
import json

try:
    response = urllib.request.urlopen("http://127.0.0.1:8080/api/public/articles")
    data = json.loads(response.read().decode("utf-8"))
    print(f"Status: Success! Articles returned: {len(data)}")
    for a in data:
        print(f"Title: {a['title']}")
        # print first 150 chars of content
        print(f"  Content: {a['content'][:150]}...")
except Exception as e:
    print(f"Error fetching articles: {e}")
