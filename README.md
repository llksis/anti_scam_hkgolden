
Anti Scam HKGolden

项目说明 / Project Description
- 本项目通过爬取 HKGolden 论坛中与关键字相关的帖子，进行数据清洗并保存为结构化的 CSV 和 Excel 格式。
- 项目包含爬虫脚本、数据清洗逻辑和完整的自动化流程。
- This project crawls HKGolden forum posts related to specific keywords, cleans the data, and saves it in structured CSV and Excel formats.
- It includes a scraping script, data cleaning logic, and an automated workflow.

---

使用说明 / Usage Instructions

1. 克隆项目 / Clone the Repository/
   git clone https://github.com/llksis/anti_scam_hkgolden.git
   cd anti_scam_hkgolden

2. 安装依赖 / Install Dependencies/
   pip install -r requirements.txt

3. 运行主程序 / Run the Main Script/
   python main.py

---

文件说明 / File Descriptions

1. main.py
   - 功能 / Functionality:
     - 自动化整个流程，包括运行爬虫脚本、清洗数据和输出最终文件。
     - 确保必要的文件（如 cleaned_hkgolden.csv）存在，如果不存在则自动创建。

2. Scrape_hkgolden_3.1.py
   - 功能 / Functionality:
     - 使用 Selenium 和 BeautifulSoup 爬取 HKGolden 论坛中与关键字相关的帖子。
     - 抓取发帖人信息、发布时间、帖子标题、类别、评论数、点赞量、点踩量以及帖子内容和回复。
   - 主要模块 / Key Modules:
     - selenium：用于浏览器自动化。
     - beautifulsoup4：用于解析 HTML 页面。
     - requests：用于通过 API 获取帖子内容和评论。
   - 输出 / Output:
     - 生成 newest_data.csv 文件，包含爬取到的最新数据。

3. final.py
   - 功能 / Functionality:
     - 读取爬取的 newest_data.csv 和历史数据 cleaned_hkgolden.csv。
     - 合并新旧数据，并清洗数据，删除重复项目（基于 id、post_time 和 title）。
     - 输出清洗后的文件到 cleaned_hkgolden.csv 和 hkgolden.xlsx。
   - 清洗逻辑 / Cleaning Logic:
     - 删除重复帖子（基于 id 和 post_time）。
     - 删除重复标题的帖子，保留最新的记录。

4. requirements.txt
   - 功能 / Functionality:
     - 列出项目所需的 Python 包，方便用户快速安装依赖。

---

输出文件 / Output Files

1. newest_data.csv:
   - 每次爬取生成的新数据。
   - 包括帖子标题、发帖人、发布时间、评论数、点赞量、点踩量、内容和关键词。
2. cleaned_hkgolden.csv:
   - 合并并清洗后的数据，去除了重复项。
3. hkgolden.xlsx:
   - 最终清洗结果，保存为 Excel 格式。

---

注意事项 / Notes

1. 运行环境 / Runtime Environment:
   - 确保安装了 Google Chrome 和相应的 ChromeDriver。
   - 如果没有 GUI 环境，可以使用无头模式运行爬虫（在 Scrape_hkgolden_3.1.py 中启用 chrome_options.add_argument("--headless")）。

2. 爬取速度限制 / Scraping Speed:
   - 避免频繁爬取以触发目标网站的反爬虫机制。
   - 可以通过 time.sleep() 增加爬取间隔。

3. 扩展关键字 / Extending Keywords:
   - 在 Scrape_hkgolden_3.1.py 中编辑 keywords 列表以添加更多搜索关键词。

.
