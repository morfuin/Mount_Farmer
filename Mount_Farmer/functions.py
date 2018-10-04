"""
Functions used for site
"""

import config_cosmos_db
import pydocumentdb.document_client as document_client
from wowapi import WowApi

def get_mounts(user, realm):
    mounts = WowApi.get_character_profile('us', realm, user, fields=['mounts'])
    user_mount_list = []
    for x in range(len(mounts['mounts']['collected'])):
        mount_name = mounts['mounts']['collected'][x]['name']
        user_mount_list.append(mount_name)
    return user_mount_list

def get_faction(user, realm):
    faction = WowApi.get_character_profile('us', realm, user)
    user_faction = faction["faction"]
    return user_faction

def check_mounts(user_mount_list, user_faction):
    """ This function compares the list of mounts for user with the model data from the COSMOS DB """
    model_list = get_model_list()
    user_list = user_mount_list
    match_user_list = []
    return_user_list = []
    pre_set_model_list = []
    if user_faction == 0:
        for x in range(len(model_list)):
            if model_list[x]['mount_faction'] == '0' or model_list[x]['mount_faction'] == "1":
                name = model_list[x]['mount_name']
                pre_set_model_list.append(name)
    if user_faction == 1:
        for x in range(len(model_list)):
            if model_list[x]['mount_faction'] == '1' or model_list[x]['mount_faction'] == "2":
                name = model_list[x]['mount_name']
                pre_set_model_list.append(name)
    set_model_list = set(pre_set_model_list)    
    set_user_list = set(user_list)
    match_user_list = set_model_list - set_user_list
    new_user_list = list(match_user_list)    
    for z in range(len(model_list)):    
        check_item = model_list[z]['mount_name']
        if check_item in new_user_list:
            name = str(model_list[z]['mount_name'])
            id = str(model_list[z]['mount_id'])
            return_user_list.append(name)
            return_user_list.append(id)
    return return_user_list

def get_model_list():
    """ This function gets a list formed from the model data from the COSMOS DB, filtering for Faction ID """
    #Set DB Client
    client = document_client.DocumentClient(config_cosmos_db.COSMOSDB_HOST, {'masterKey': config_cosmos_db.COSMOSDB_KEY})
    #Set DB
    db_id = config_cosmos_db.COSMOSDB_DATABASE
    db_query = "select * from r where r.id = '{0}'".format(db_id)
    db = list(client.QueryDatabases(db_query))[0]
    db_link = db['_self']
    #Set DB Collection
    coll_id = config_cosmos_db.COSMOSDB__MODEL_COLLECTION
    coll_query = "select * from r where r.id = '{0}'".format(coll_id)
    coll = list(client.QueryCollections(db_link, coll_query))[0]
    coll_link = coll['_self']
    #SQL Query
    query = { 'query': 'SELECT model.mount_name, model.mount_percent, model.mount_id, model.mount_faction FROM model' }    
    model = client.QueryDocuments(coll_link, query)
    model_data_list = list(model)
    return model_data_list


def get_mounts_list():
    """This Function gets the mount name and mount id from the COSMOS DB"""
    #Set DB Client
    client = document_client.DocumentClient(config_cosmos_db.COSMOSDB_HOST, {'masterKey': config_cosmos_db.COSMOSDB_KEY})
    #Set DB
    db_id = config_cosmos_db.COSMOSDB_DATABASE
    db_query = "select * from r where r.id = '{0}'".format(db_id)
    db = list(client.QueryDatabases(db_query))[0]
    db_link = db['_self']
    #Set DB Collection
    coll_id = config_cosmos_db.COSMOSDB__MOUNT_COLLECTION
    coll_query = "select * from r where r.id = '{0}'".format(coll_id)
    coll = list(client.QueryCollections(db_link, coll_query))[0]
    coll_link = coll['_self']
    #SQL Query
    query = { 'query': 'SELECT mount.mount_name, mount.itemId FROM mount' }    
    mounts = client.QueryDocuments(coll_link, query)
    mount_data = list(mounts)
    return mount_data