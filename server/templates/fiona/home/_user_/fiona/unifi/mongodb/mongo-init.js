db.getSiblingDB("unifi").createUser({user: "{{ app_unifi_mongodb_user }}", pwd: "{{ app_unifi_mongodb_password }}", roles: [{role: "readWrite", db: "unifi"}]});
db.getSiblingDB("unifi_stat").createUser({user: "{{ app_unifi_mongodb_user }}", pwd: "{{ app_unifi_mongodb_password }}", roles: [{role: "readWrite", db: "unifi_stat"}]});
