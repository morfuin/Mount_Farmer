import config_cosmos_db
import pydocumentdb.document_client as document_client
from wowapi import WowApi
import csv


client = document_client.DocumentClient(config_cosmos_db.COSMOSDB_HOST, {'masterKey': config_cosmos_db.COSMOSDB_KEY})

# Create database
db = client.CreateDatabase({ 'id': config_cosmos_db.COSMOSDB_DATABASE })

# Create collections
realm_collection = client.CreateCollection(db['_self'],{ 'id': config_cosmos_db.COSMOSDB__REALM_COLLECTION })
mount_collection = client.CreateCollection(db['_self'],{ 'id': config_cosmos_db.COSMOSDB__MOUNT_COLLECTION })
model_collection = client.CreateCollection(db['_self'],{ 'id': config_cosmos_db.COSMOSDB__MODEL_COLLECTION })

#Gets a list of realms from the wowapi. Creats a document for each realm. 
realms = WowApi.get_realm_status('us')
realm_counter = 0
for realm in realms['realms']:
    realm_name = realms["realms"][realm_counter]['name']
    realm_counter +=1
    realm_document = client.CreateDocument(realm_collection['_self'],
        { 'id': realm_name,
          'realm_name': realm_name + " (US)",
          'name': realm_name 
        })      
      
#Gets a list of mounts from the wowapi. Creats a document for each realm. Using mount name + itemID for document ID. 
mounts = WowApi.get_mounts('us')
mount_counter = 0
for mount in mounts['mounts']:
    mount_name = mounts["mounts"][mount_counter]['name']
    mount_spellid = mounts["mounts"][mount_counter]['spellId']
    mount_itemid = mounts["mounts"][mount_counter]['itemId']
    mount_counter +=1
    mount_itemid_str = str(mount_itemid)
    mount_spellid_str = str(mount_spellid)  
    mount_doc_id = mount_name + "_" + mount_itemid_str + "_" + mount_spellid_str
    mount_document = client.CreateDocument(mount_collection['_self'],
        { 'id': mount_doc_id,
          'mount_name': mount_name,
          'spellId': mount_spellid,
          'itemId': mount_itemid,
          'name': mount_name 
        })

#Sets up init mount distribution values for mount model from local csv data.        
with open('init_mount_dist.csv') as m:
   mount_name = csv.reader(m)
   mount_dist_list = list(mount_name)
mount_dist_name_int = 0
mount_dist_percent_int = 1
mount_dist_id_int = 2
mount_dist_faction_int = 3
mount_dist_counter = 0
for mount_dist in mount_dist_list:
   mount_dist_name = mount_dist_list[mount_dist_counter][mount_dist_name_int]
   mount_dist_percent = mount_dist_list[mount_dist_counter][mount_dist_percent_int]
   mount_dist_id = mount_dist_list[mount_dist_counter][mount_dist_id_int]
   mount_dist_faction = mount_dist_list[mount_dist_counter][mount_dist_faction_int]
   mount_dist_counter +=1
   model_document = client.CreateDocument(model_collection['_self'],
    { 'mount_name': mount_dist_name,
      'mount_percent': mount_dist_percent,
      'name': mount_dist_name,
      'mount_id': mount_dist_id,
      'mount_faction': mount_dist_faction
    })
   
