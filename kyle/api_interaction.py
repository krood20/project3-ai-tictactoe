import http.client

import http.client
import mimetypes
from codecs import encode
import time

# TEAM INFO
#Main Team: TeamTacToe
#{"code":"OK","teamId":1260}
teamId = "1260"

teamId1 = "1260"
teamId2 = "1259"

# Test team: AlphaTicTacToe
# {"code":"OK","teamId":1259}

boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'


## GET ##
def get_myTeams(conn, payload, headers):
    conn.request("GET", "/aip2pgaming/api/index.php?type=myTeams", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    return data.decode("utf-8")

def get_team_members(conn, payload, headers, team_id):
    conn.request("GET", "/aip2pgaming/api/index.php?type=team&teamId=" + team_id, payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    return data.decode("utf-8")

def get_moves(conn, payload, headers, gameId, count):
    conn.request("GET", "/aip2pgaming/api/index.php?type=moves&gameId=" + gameId + "&count=" + count, payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    return data.decode("utf-8")

def get_board_string(conn, payload, headers, gameId):
    conn.request("GET", "/aip2pgaming/api/index.php?type=boardString&gameId=" + gameId, payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    return data.decode("utf-8")

def get_board_map(conn, payload, headers, gameId):
    conn.request("GET", "/aip2pgaming/api/index.php?type=boardMap&gameId=" + gameId, payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    return data.decode("utf-8")

## POST ##
def general_post(conn, payload, headers, dataList):
    body = b'\r\n'.join(dataList)
    payload = body
    headers = {
        'x-api-key': '9398bf5f4533fbabb0af',
        'userId': '1042',
        'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
    }

    conn.request("POST", "/aip2pgaming/api/index.php", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    return data.decode("utf-8")

def create_team(conn, payload, headers, team_name):
    # conn.request("POST", "/aip2pgaming/api/index.php?name=" + team_name + "&type=team", payload, headers)
    # res = conn.getresponse()
    # data = res.read()
    # print(data.decode("utf-8"))
    dataList = []
    boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=name;'))
    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))
    dataList.append(encode(team_name))
    dataList.append(encode('--' + boundary))

    dataList.append(encode('Content-Disposition: form-data; name=type;'))
    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))
    dataList.append(encode("team"))
    dataList.append(encode('--'+boundary+'--'))
    dataList.append(encode(''))

    general_post(conn, payload, headers, dataList)


def add_member_to_team(conn, payload, headers, teamId, userId):
    # conn.request("POST", "/aip2pgaming/api/index.php?type=" + entry_type + "&teamId=" + teamId + "&userId=" + userId, payload, headers)
    # res = conn.getresponse()
    # data = res.read()
    # print(data.decode("utf-8"))
    #For create team (not using params)
    dataList = []
    boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=type;'))
    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))
    dataList.append(encode("member"))
    dataList.append(encode('--' + boundary))

    dataList.append(encode('Content-Disposition: form-data; name=teamId;'))
    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))
    dataList.append(encode(teamId))
    dataList.append(encode('--' + boundary))

    dataList.append(encode('Content-Disposition: form-data; name=userId;'))
    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))
    dataList.append(encode(userId))
    dataList.append(encode('--'+boundary+'--'))
    dataList.append(encode(''))

    general_post(conn, payload, headers, dataList)

def create_game(conn, payload, headers, teamId1, teamId2, gameType):
    dataList = []
    boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=type;'))
    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))
    dataList.append(encode("game"))
    dataList.append(encode('--' + boundary))

    dataList.append(encode('Content-Disposition: form-data; name=teamId1;'))
    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))
    dataList.append(encode(teamId1))
    dataList.append(encode('--' + boundary))

    dataList.append(encode('Content-Disposition: form-data; name=teamid2;'))
    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))
    dataList.append(encode(teamId2))
    dataList.append(encode('--' + boundary))

    dataList.append(encode('Content-Disposition: form-data; name=gameType;'))
    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))
    dataList.append(encode(gameType))
    dataList.append(encode('--'+boundary+'--'))
    dataList.append(encode(''))

    general_post(conn, payload, headers, dataList)

def make_move(conn, payload, headers, teamId, move, gameId):
    dataList = []
    boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=type;'))
    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))
    dataList.append(encode("move"))
    dataList.append(encode('--' + boundary))

    dataList.append(encode('Content-Disposition: form-data; name=teamId;'))
    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))
    dataList.append(encode(teamId))

    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=move;'))
    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))
    dataList.append(encode(move))
    dataList.append(encode('--' + boundary))

    dataList.append(encode('Content-Disposition: form-data; name=gameId;'))
    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))
    dataList.append(encode(gameId))
    dataList.append(encode('--'+boundary+'--'))
    dataList.append(encode(''))

    general_post(conn, payload, headers, dataList)

def try_move(conn, payload, headers, teamId, gameId):
    move="4,4"

    moves = get_moves(conn, payload, headers, gameId, "30")
    board_string = get_board_string(conn, payload, headers, gameId)
    board_map = get_board_map(conn, payload, headers, gameId)

    #parsing the board
    board_by_rows = board_string.split("\"")[3].split("\\n")[:-1]
    print(board_by_rows)

    current_board = []
    for row in board_by_rows:
        row = row.replace('-', '_')
        current_board.append([char for char in row])

    for row in current_board:
        print(row)

    make_move(conn, payload, headers, teamId, move, gameId)


#NOT USED FUNCTIONS
#getting teams for current api user
# teams = get_myTeams(conn, payload, headers)
# print(teams)

# name = "AlphaTicTacToe"
# create_team(conn, payload, headers, name)

# entry_type = "member"
# userId = "1042"
# add_member_to_team(conn, payload, headers, teamId, userId)

# team_members = get_team_members(conn, payload, headers, teamId)
# print(team_members)

# gameType = "TTT"
# create_game(conn, payload, headers, teamId1, teamId2, gameType)

#Example Board map
#{"output":"{\"2,2\":\"O\",\"3,3\":\"X\",\"1,2\":\"O\",\"3,2\":\"X\",\"0,2\":\"O\"}","target":3,"code":"OK"}

#Example board string
# "{\"output\":\"--O-\n--O-\n--O-\n--XX\n\",\"target\":3,\"code\":\"OK\"}"

#Example moves
# {"moves":[{"moveId":"52412","gameId":"1310","teamId":"1204","move":"10,4","symbol":"X","moveX":"10","moveY":"4"},
#           {"moveId":"52378","gameId":"1310","teamId":"1229","move":"6,10","symbol":"O","moveX":"6","moveY":"10"},
#           {"moveId":"52372","gameId":"1310","teamId":"1204","move":"5,9","symbol":"X","moveX":"5","moveY":"9"},
#           {"moveId":"52342","gameId":"1310","teamId":"1229","move":"7,9","symbol":"O","moveX":"7","moveY":"9"},
#           {"moveId":"52336","gameId":"1310","teamId":"1204","move":"6,8","symbol":"X","moveX":"6","moveY":"8"},
#           {"moveId":"52324","gameId":"1310","teamId":"1229","move":"10,6","symbol":"O","moveX":"10","moveY":"6"},
#           {"moveId":"52323","gameId":"1310","teamId":"1204","move":"9,5","symbol":"X","moveX":"9","moveY":"5"},
#           {"moveId":"52321","gameId":"1310","teamId":"1229","move":"9,7","symbol":"O","moveX":"9","moveY":"7"},
#           {"moveId":"52320","gameId":"1310","teamId":"1204","move":"8,6","symbol":"X","moveX":"8","moveY":"6"},
#           {"moveId":"52319","gameId":"1310","teamId":"1229","move":"8,8","symbol":"O","moveX":"8","moveY":"8"},
#           {"moveId":"52318","gameId":"1310","teamId":"1204","move":"7,7","symbol":"X","moveX":"7","moveY":"7"},
#           {"moveId":"52316","gameId":"1310","teamId":"1229","move":"6,6","symbol":"O","moveX":"6","moveY":"6"}
#          ],"code":"OK"}

def run():
    #connect to api
    conn = http.client.HTTPSConnection("www.notexponential.com")
    payload = ''
    headers = {
        'x-api-key': '9398bf5f4533fbabb0af',
        'userId': '1042'
    }

    gameId = "1310"
    #RUN CODE#
    while True:
        try_move(conn, payload, headers, teamId, gameId)
        time.sleep(30)

#run()