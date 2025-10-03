import os
import pymongo
from pymongo.errors import OperationFailure
from pymongo.mongo_client import MongoClient
from pymongo import errors
import hashlib
import json

def get_collection(bot_name, mongo_uri):
    # Enable TLS for MongoDB connection
    client = MongoClient(
        mongo_uri,
        tls=True,
        tlsAllowInvalidCertificates=False,
        serverSelectionTimeoutMS=30000
    )

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except errors.OperationFailure as e:
        raise ValueError(f"Failed to connect to MongoDB: {e}")

    # Generate a unique collection name using the bot token
    collection_name = hashlib.md5(bot_name.encode()).hexdigest()
    db = client['Luminant']
    return db[collection_name]

def save_name(collection, name):
    with open("name.txt", "w") as file:
        file.write(name)
    existing_name = collection.find_one()
    if existing_name:
        collection.update_one({}, {"$set": {"name": name}})
    else:
        collection.insert_one({"name": name})

def load_name(collection):
    try:
        with open("name.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        pass
    result = collection.find_one()
    if result:
        return result.get("name")
    else:
        return None

def save_accept_logs(collection, accept_logs):
    with open("accept_logs.txt", "w") as file:
        file.write(str(accept_logs))
    existing_logs = collection.find_one({"accept_logs": {"$exists": True}})
    if existing_logs:
        collection.update_one({}, {"$set": {"accept_logs": accept_logs}})
    else:
        collection.insert_one({"accept_logs": accept_logs})

def load_accept_logs(collection):
    try:
        with open("accept_logs.txt", "r") as file:
            return int(file.read().strip())
    except FileNotFoundError:
        pass
    result = collection.find_one({"accept_logs": {"$exists": True}})
    if result:
        return result.get("accept_logs")
    else:
        return 0

def save_authorized_users(collection, authorized_users):
    with open("authorized_users.txt", "w") as file:
        for user_id in authorized_users:
            file.write(str(user_id) + "\n")
    existing_users = collection.find_one({"type": "authorized_users"})
    if existing_users:
        collection.update_one({"type": "authorized_users"}, {"$set": {"value": authorized_users}})
    else:
        collection.insert_one({"type": "authorized_users", "value": authorized_users})

def load_authorized_users(collection):
    try:
        with open("authorized_users.txt", "r") as file:
            return [int(user_id) for user_id in file.read().splitlines()]
    except (FileNotFoundError, ValueError):
        pass
    result = collection.find_one({"type": "authorized_users"})
    if result:
        return result.get("value", [])
    else:
        return []

def save_allowed_channel_ids(collection, allowed_channel_ids):
    with open("allowed_channel_ids.txt", "w") as file:
        for channel_id in allowed_channel_ids:
            file.write(str(channel_id) + "\n")
    existing_channels = collection.find_one({"type": "allowed_channel_ids"})
    if existing_channels:
        collection.update_one({"type": "allowed_channel_ids"}, {"$set": {"value": allowed_channel_ids}})
    else:
        collection.insert_one({"type": "allowed_channel_ids", "value": allowed_channel_ids})

def load_allowed_channel_ids(collection):
    try:
        with open("allowed_channel_ids.txt", "r") as file:
            return [int(channel_id) for channel_id in file.read().splitlines()]
    except (FileNotFoundError, ValueError):
        pass
    result = collection.find_one({"type": "allowed_channel_ids"})
    if result:
        return result.get("value", [])
    else:
        return []

def save_log_channel_id(collection, log_channel_id):
    with open("log_channel_id.txt", "w") as file:
        file.write(str(log_channel_id))
    existing_log_channel = collection.find_one({"type": "log_channel_id"})
    if existing_log_channel:
        collection.update_one({"type": "log_channel_id"}, {"$set": {"value": log_channel_id}})
    else:
        collection.insert_one({"type": "log_channel_id", "value": log_channel_id})

def load_log_channel_id(collection):
    try:
        with open("log_channel_id.txt", "r") as file:
            return int(file.read().strip())
    except (FileNotFoundError, ValueError):
        pass
    result = collection.find_one({"type": "log_channel_id"})
    if result:
        return result.get("value", -1)
    else:
        return -1

#===================== SAVING AND LOADING BOT RUNNING TIME ===========================

def save_bot_running_time(collection, time_to_add):
    current_time = collection.find_one({"type": "bot_running_time"})
    if current_time:
        total_time = current_time['time'] + time_to_add
        collection.update_one({"type": "bot_running_time"}, {"$set": {"time": total_time}})
    else:
        total_time = time_to_add
        collection.insert_one({"type": "bot_running_time", "time": total_time})
    return total_time

def load_bot_running_time(collection):
    current_time = collection.find_one({"type": "bot_running_time"})
    return current_time['time'] if current_time else 0

def reset_bot_running_time(collection, new_time=0):
    collection.update_one({"type": "bot_running_time"}, {"$set": {"time": new_time}}, upsert=True)

def save_max_running_time(collection, max_time):
    collection.update_one({"type": "max_running_time"}, {"$set": {"time": max_time}}, upsert=True)

def load_max_running_time(collection):
    current_time = collection.find_one({"type": "max_running_time"})
    return current_time['time'] if current_time else 800 * 3600

#============ QUEUE FILE SAVING AND LOADING ================

def save_queue_file(collection, file_queue):
    collection.delete_many({})
    if file_queue:
        collection.insert_one({"type": "file_queue", "file_queue_data": file_queue})

def load_queue_file(collection):
    result = collection.find_one({"type": "file_queue"})
    return result['file_queue_data'] if result else []
