from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager  # 用于自动管理驱动
from bs4 import BeautifulSoup
import pandas as pd
import time
#import random
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import html
import re




# 设置 Chrome 选项
chrome_options = Options()
#chrome_options.add_argument("--headless")  # 无头模式（可选）
chrome_options.add_argument("--disable-gpu") # 禁用 GPU
chrome_options.add_argument("--no-sandbox") # 禁用沙箱
#chrome_options.add_argument("user-agent = Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36")



keywords = ["Scam",  "騙", "Cheating", "Fraud", "詐",  "呃"]
#keywords = ["Scam", "Cheating", "Fraud", "欺騙", "行騙", "詐騙", "詐欺", "電騙", "騙"]

# 构造空的列表，用于存放发帖人，发帖人id，发布时间，标题，类别，评论数，点赞量，点踩量，帖子的链接
author = []
post_ids = []
publish_time = []
title = []
category = []
reply = []
upvote = []
downvote = []
post_links = []
word=[]


for keyword in keywords:
    url = f'https://forum.hkgolden.com/search/T/{keyword}'
    # 启动 Chrome 浏览器
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # 打开目标网页
    driver.get(url)
    #time.sleep(random.uniform(2, 5)) # 模拟人的行为

    # 等待页面加载，直到找到某个特定元素
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'jss126'))  # 替换为实际页面结构
    )
    #print(keyword+":")
    #print("页面加载成功", end="/")


    # 实现网页滚动到底，便于后续爬取全部内容
    def Scroll_webpage():
        from selenium.webdriver.common.keys import Keys  # 确保导入 Keys 模块
        # 记录初始的页面高度
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # 模拟滚动到底部
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)  # 使用正确的 Keys
            time.sleep(3)  # 根据网络速度和页面加载时间调整等待时间
            new_height = driver.execute_script("return document.body.scrollHeight") # 获取当前页面的高度
            # 如果滚动后页面高度没有变化，则认为所有内容已加载
            if new_height == last_height:
                #print("已加载到页面底部 无更多内容", end="/")
                break  # 退出循环
            last_height = new_height # 更新页面高度

    Scroll_webpage()


    # 使用 BeautifulSoup 解析 HTML
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    posts = soup.find_all('div', class_='jss262')


    # 构造用于爬取帖子基本信息的函数
    def Scrape_basic_info():

        # 遍历每个帖子提取信息
        for post in posts:
            try:
                # 提取发帖者
                author_tag = post.find('summary', class_=['jss267', 'jss268'])
                author.append(author_tag.text.strip() if author_tag else "Unknown")  # 检查是否为 None

                # 提取发帖时间
                small_tag = post.find('small')
                publish_time.append(small_tag.get('title') if small_tag else "Unknown")  # 检查是否为 None

                # 提取帖子标题
                title_tag = post.find('div', class_='jss251')
                title.append(title_tag.text.strip() if title_tag else "No Title")  # 检查是否为 None

                # 所属类别
                category_tag = post.find('div', class_='jss243 jss244')
                category.append(category_tag.text.strip() if category_tag else "Unknown")  # 检查是否为 None

                # 提取帖子的链接
                link = post.find('a', class_='jss263')
                link_tag = link['href'] if link else "#"
                full_link = f"https://forum.hkgolden.com{link_tag}"  # 构造完整链接，并检查是否为 None
                post_id = full_link.split('/thread/')[-1].split('/')[0]
                post_ids.append(post_id) # 顺带爬取发帖人的id号，便于后续爬取帖子的具体内容
                post_links.append(full_link)  

                # 提取评论量
                use_tag = post.find('use', {'xlink:href': '#go-reply'})
                small_tag = use_tag.find_parent('small')
                reply.append(small_tag.text.strip() if small_tag else "Unknown") # 检查是否为 None

                # 提取点赞量
                use_tag = post.find('use', {'xlink:href': '#good-line'})
                small_tag = use_tag.find_parent('small')
                upvote.append(small_tag.text.strip() if small_tag else "Unknown") # 检查是否为 None

                # 提取点踩量
                use_tag = post.find('use', {'xlink:href': '#bad-line'})
                small_tag = use_tag.find_parent('small')
                downvote.append(small_tag.text.strip() if small_tag else "Unknown") # 检查是否为 None
                
                # 加上keyword
                word.append(keyword)

            except Exception as e:
                print(f"提取信息时出错: {e}")
        
        print("已完成基础信息爬取", len(posts), end="/")

    Scrape_basic_info() # 运行函数


    # 构造空的列表，用于存放帖子和评论的具体内容
    post_contents = []
    all_posts_replies = []

    """获取每个帖子和相应评论的api网址"""
    def fetch_page_content(post_id, page):
        base_url = f"https://api.hkgolden.com/v1/view/{post_id}/{page}?sensormode=Y&hideblock=N"
        try:
            response = requests.get(base_url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"请求错误: {e}")
            return None

    """获取每个帖子的具体内容和指定页的评论"""
    def Scrape_content(post_ids):
        for post_id in post_ids:
            if post_id is None:
                post_contents.append(None)
                all_posts_replies.append(None)
                continue

            # 请求第一页，获取总页数
            url = f"https://api.hkgolden.com/v1/view/{post_id}/1?sensormode=Y&hideblock=N"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data and data.get("result") and data["data"]:
                # 爬取帖子的具体内容
                raw_content = data["data"].get("content", "")
                decoded_content = html.unescape(raw_content) # 解码 HTML 转义字符

                # 用正则表达式美化文本
                formatted_content = re.sub(r'(<br\s*/?>|\\u003Cbr\\u003E|\\n)', '\n',   decoded_content) # 先将 <br> 标签和换行符替换为换行
                formatted_content = re.sub(r'<(?!a\s|img\s)[^>]*>', '',     formatted_content) # 去掉除 <a> 和 <img> 之外的所有其他 HTML 标签
                formatted_content = re.sub(r'\n+', '\n', formatted_content).strip() # 替换多余的空行
                post_contents.append(formatted_content) # 存储到列表

                # 获取总页数，爬取每页的评论
                total_pages = data["data"].get("totalPage", 1)
                
                page_replies = [] # 构造空列表存放每个帖子的回复

                if total_pages == 1: # 如果只有一页内容，直接抓取而不使用并发
                    replies = data["data"].get("replies", [])
                    for idx, replies in enumerate(replies, start=1):
                        raw_reply = replies.get("content", "")
                        reply_decoded_content = html.unescape(raw_reply) # 解码 HTML 转义字符
                        reply_formatted_content = re.sub(r'(<br\s*/?>|\\u003Cbr\\u003E|\\n)', '\n', reply_decoded_content) # 用正则表达式美化文本
                        page_replies.append(f"{idx}: {reply_formatted_content}")
                else:
                    # 使用线程池并发抓取每页内容
                    with ThreadPoolExecutor(max_workers=5) as executor:
                        futures = {executor.submit(fetch_page_content, post_id, page):  page for page in range(1, total_pages + 1)}

                        global_idx = 1 # 重置全局序号计数器

                        for future in as_completed(futures):
                            page_data = future.result()

                            if page_data and page_data.get("result") and page_data  ["data"]:
                                replies = page_data["data"].get("replies", [])
                                for reply in replies:
                                    raw_reply = reply.get("content", "")
                                    reply_decoded_content = html.unescape(raw_reply)
                                    reply_formatted_content = re.sub(r'(<br\s*/?>|\\u003Cbr\\u003E|\\n)', '\n', reply_decoded_content)
                                    page_replies.append(f"{global_idx}:{reply_formatted_content}")
                                    global_idx += 1 # 递增全局序号

                # 将收集的页回复合并到所有回复列表，无论是否有回复数据，确保添加占位符
                all_posts_replies.append("\n".join(page_replies) if page_replies else None)
            else:
                print(post_id+"未找到内容")
                post_contents.append(None)
                all_posts_replies.append(None)

        print("已完成爬取内容和回复")

    Scrape_content(post_ids) # 执行内容爬虫
    
    driver.quit() # 全部爬完，退出网页


#把数据整合在一个数据表中
posts_data = {
    "title": title,
    "username": author,
    "post_time": publish_time,
    "id": post_ids,
    "category": category,
    "url": post_links,
    "reply_count": reply,
    "upvote_count": upvote,
    "downvote_count": downvote,
    "post_content": post_contents,
    "replies": all_posts_replies,
    "keyword":word,
    "platform":"HKgolden_forum"
    }

# 打印带有表格线的格式的表格，生成csv文件
from IPython.display import display
import pandas as pd
import shutil

# 将数据整合为 DataFrame
datatoday = pd.DataFrame.from_dict(posts_data)

# 保存为 newest_data.csv
datatoday.to_csv('newest_data.csv', encoding='utf-8-sig', index=False)
print("数据已保存至 newest_data.csv")

# 带时间戳的备份（可选启用）
# from datetime import datetime
# time_stamp = datetime.now().strftime("%Y-%m-%d_%H%M")
# file_name = f'{time_stamp}.csv'
# datatoday.to_csv(file_name, encoding='utf-8-sig', index=False)
# shutil.copy(file_name, 'newest_data.csv')
