with open("wisdom_hub.html", encoding="utf-8") as f:
    content = f.read()
    start = content.find("id: 4")
    if start != -1:
        print("wisdom_hub.html Article 4:")
        print(content[start:start+1000])

with open("server.py", encoding="utf-8") as f:
    content = f.read()
    start = content.find("The Sacred Geometry of Nagara Nirmana")
    if start != -1:
        print("server.py Article 4:")
        print(content[start-100:start+1000])
