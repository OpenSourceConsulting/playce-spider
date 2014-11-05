#-*- coding: utf-8 -*-
'''
Created on 2014. 11. 5.

사용자 관련 모듈로써 다음과 같은 기능을 갖는다.
 - 로그인
 - 사용자 목록 조회
 - 사용자 추가

@author: Sang-Cheon Park
'''

from spidercore import *

logger = logging.getLogger(__name__)

"""
로그인
"""
@app.route("/user/login", methods=['POST'])
def login():
    jsonData = request.json
    
    userId = jsonData.get('userId')
    password = jsonData.get('password')
    
    logger.debug("userId : [%s], Password : [%s]", userId, password)
    
    users = read_repository("users")
    
    match = False
    for user in users:
        if user['userId'] == userId and user['password'] == password:
            match = True
            break

    if match:
        return json.dumps(user)
    else:
        return 'Invalid userId or password.', 404

"""
사용자 목록 조회
"""
@app.route("/user/list", methods=['GET'])
def user_list():
    users = read_repository("users")
    return json.dumps(users)

"""
사용자 추가
"""
@app.route("/user/insert", methods=['POST'])
def user_insert():
    jsonData = request.json
    
    if jsonData.get('userId') == None:
        return "userId can not be null.", 503
    elif jsonData.get('password') == None:
        return "password can not be null.", 503
    else:
        users = read_repository("users")
        
        # duplication check
        match = False
        for user in users:
            if user['userId'] == jsonData.get('userId') and user['password'] == jsonData.get('password'):
                match = True
                break
        
        if match:
            return jsonData.get('userId') + " is already exists."
        else:
            users.append(jsonData)
            write_repository("users", users)
            return json.dumps(users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)