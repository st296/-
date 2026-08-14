import requests
from bs4 import BeautifulSoup
from typing import List, Dict

#bs：用来解析的类#

def get_baidu_hot_top10() -> List[Dict]:
    # 百度实时热搜官方页面地址
    url = "https://top.baidu.com/board?tab=realtime"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Referer": "https://www.baidu.com/"
    }
    #数据类型字典，对应了各个传入的信息，可以把代码伪装成正常浏览器#

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = "utf-8"
        
        if response.status_code != 200:
            print(f"请求失败，状态码：{response.status_code}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        #传入bs的构造函数；需要第二个参数去指定解析器#
        hot_items = soup.find_all("div", class_="category-wrap_iQLoo")
        
        result = []
        for index, item in enumerate(hot_items[:10]):
            rank = index + 1
            title_tag = item.find("div", class_="c-single-text-ellipsis")
            #可以在网页检查找到：<div class="c-single-text-ellipsis">  让思想之光照亮强军征程 <!--27--></div>#
            title = title_tag.get_text(strip=True) if title_tag else "无标题"
            hot_tag = item.find("div", class_="hot-index_1Bl1a")
            hot_value = hot_tag.get_text(strip=True) if hot_tag else "无热度数据"
            link_tag = item.find("a", class_="img-wrapper_29V76")
            link = link_tag.get("href", "") if link_tag else ""

            result.append({
                "排名": rank,
                "热搜标题": title,
                "热度值": hot_value,
                "跳转链接": link
            })
        
        return result

    except Exception as e:
        print(f"爬取过程出现异常：{str(e)}")
        return []

if __name__ == "__main__":
    hot_data = get_baidu_hot_top10()
    
    if hot_data:
        print("=== 当前百度热搜Top10 ===")
        for item in hot_data:
            print(f"{item['排名']}. {item['热搜标题']}  热度：{item['热度值']}")
    else:
        print("未能获取到热搜数据，请检查网络或页面结构是否更新")
