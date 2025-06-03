# 爬虫主要文件
# 使用网易云音乐API爬取歌手、歌曲、评论、用户信息

import json
import urllib.request
import urllib.parse
import time

output = "../output"
prefix = 'http://163api.qijieya.cn/'


# 进行get请求并将JSON解码  加入自动重试
def doGet(url):
    while True:
        try:
            req = urllib.request.Request(url=prefix + url, method="GET")
            response = urllib.request.urlopen(req)
            res = response.read().decode('utf-8')
            return json.loads(res)
        except:
            print("异常URL：{}".format(url))
            time.sleep(10)


# 歌手列表 歌手名name id
def getHotArtists(num=100):
    # 只能获取100个
    # url = '/top/artists?offset=0&limit={}'.format(num)

    res = []
    offsets = [i for i in range(0, num, 100)]
    for offset in offsets:
        url = '/artist/list?type=-1&area=7&initial=-1&limit=100&offset={}'.format(offset)
        dict = doGet(url)
        res += dict['artists']
    return res


# 某歌手的热门歌曲 name id
def getHotSongOfArtist(artistId, num=50):
    url = '/artist/top/song?id={}'.format(artistId)
    dict = doGet(url)
    return dict['songs']


def getSongsOfArtist(artistId, num=100):
    url = "/artist/songs?id={}&limit={}".format(artistId, num)
    dict = doGet(url)
    return dict['songs']


# 某歌曲的热门评论 MAX=3000
def getHotComments(songId, num=100):
    url = '/comment/hot?id={}&type=0&limit={}'.format(songId, num)
    dict = doGet(url)
    return dict['hotComments']


# 寻找相似歌曲
def getSimilarSongs(songId):
    url = "/simi/song?id={}".format(songId)
    songs = doGet(url)['songs']
    # 只保留相似的目标歌曲ID
    res = []
    for item in songs:
        res.append(item['id'])
    return res


if __name__ == '__main__':

    singer_num = 500
    song_num_per_singer = 300
    comment_num_per_song = 3000

    singer_file = open(output+'/singers.txt', 'w', encoding='utf-8')
    song_file = open(output+'/songs.txt', 'w', encoding='utf-8')
    comment_file = open(output+'/comments.txt', 'w', encoding='utf-8')
    simi_file = open(output+"/similar.txt", 'w', encoding='utf-8')

    artists = getHotArtists(singer_num)
    for artist in artists:
        singer_file.write(json.dumps(artist, ensure_ascii=False) + '\n')

    print('找到的歌手数量:' + str(len(artists)))
    
    for artist, i in zip(artists, range(0, singer_num)):

        songs = getHotSongOfArtist(artist['id'], song_num_per_singer)
        print('目前是第{}<{}>的场子, 歌曲数目为 {}'.format(i + 1, artist['name'], len(songs)))
        for song in songs:
            song_file.write(json.dumps(song, ensure_ascii=False) + '\n')
            song_file.flush()

            # 歌曲相似关系获取
            simi = getSimilarSongs(song['id'])
            for ii in simi:
                dd = {'source': song['id'], 'target': ii}
                simi_file.write(json.dumps(dd) + '\n')
            simi_file.flush()

            comments = getHotComments(song['id'], comment_num_per_song)
            print('{}--{}--{}'.format(artist['name'], song['name'], len(comments)))
            i = 0
            for comment in comments:
                if comment['likedCount'] > 100:
                    continue
                i += 1
                comment['content'] = comment['content']
                comment_file.write(json.dumps(comment, ensure_ascii=False) + '\n')
            print("筛选后还剩{}条评论".format(i))
            time.sleep(3)

            comment_file.flush()

    singer_file.close()
    song_file.close()
    comment_file.close()
    simi_file.close()
