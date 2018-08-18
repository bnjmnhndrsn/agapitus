from db import Session, Post

session = Session()

p = Post(image_url='test.com')
session.add(p)
session.commit()
print(p.id)