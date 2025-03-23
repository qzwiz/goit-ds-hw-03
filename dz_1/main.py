from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId


client = MongoClient(
    "mongodb+srv://darkwiz:pososed222999@cluster0.0h6op.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    server_api=ServerApi("1"),
)

db = client.dz1

try:
    result_one = db.cat.insert_one(
        {
            "name": "barsik",
            "age": 3,
            "features": ["ходить в капці", "дає себе гладити", "рудий"],
        }
    )
    print("Inserted ID:", result_one.inserted_id)
except Exception as e:
    print("Error inserting document:", e)


print(result_one.inserted_id)

find_one = db.cat.find_one({"_id": ObjectId("60d24b783733b1ae668d4a77")})
print(find_one)


##################################################        READ       #######################
def read_all_cats():
    read_all = list(db.cat.find())
    if read_all:
        for doc in read_all:
            print(doc)
    


def find_cat_by_name():
    name = input("find cat: ")
    cat = db.cat.find_one({"name": name})

    if cat:
        print(cat)
    else:
        print("netu takogo kota")


read_all_cats()
find_cat_by_name()

##################################################        UPDATE       #######################
def update_cat():
    name = input("Cat`s name: ")
    cat = db.cat.find_one({"name": name})

    if cat:
        new_age = input("New cat`s age: ")
        db.cat.update_one({"name": name}, {"$set": {"age": new_age}})
        print(f"Cat {name} updated to {new_age}")
    else:
        print("netu takogo kota")   

def update_new_feature():
    name = input("Cat`s name: ")
    cat = db.cat.find_one({"name": name})

    if cat:
        new_feature = input("New cat`s feature: ")
        db.cat.update_one({"name": name}, {"$push": {"features": new_feature}})
        print(f"Cat {name} updated with {new_feature}")
    else:    
        print("netu takogo kota")

update_cat()
j = input("Show all cats? y/n: ")
if j == "y":
    read_all_cats()
else:
    print("ok, next")

d = input("Update new feature? y/n: ")
if d == "y":
    update_new_feature()
else:
    print("ok, next")

##################################################        DELETE       #######################
def delete_cat():
    name = input("какое имя удалить: ")
    cat = db.cat.find_one({"name": name})

    if cat: 
        db.cat.delete_one({"name": name})
        print(f"Cat {name} deleted")
    else:
        print("netu takogo kota")


def delete_all_cats():
    db.cat.delete_many({})
    print("All cats deleted")

f = input("Delete cat? y/n: ")
if f == "y":
    delete_cat()
else:
    print(read_all_cats())


g = input("Delete all cats? y/n: ")
if g == "y":
    delete_all_cats()
else:
    print(read_all_cats())

