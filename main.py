import os
import sys
import pandas as pd
import traceback

def ensure_cleaned_data_exists():
    """
    检查或初始化 cleaned_hkgolden.csv 文件。
    如果文件不存在，则创建一个空的 CSV 文件。
    """
    if not os.path.exists('cleaned_hkgolden.csv'):
        print("cleaned_hkgolden.csv 不存在，正在创建一个空白文件...")
        # 创建一个空的 DataFrame，包含所需列
        empty_data = pd.DataFrame(columns=['id', 'title', 'username', 'post_time', 'post_content', 'replies', 'url', 'keyword', 'platform'])
        empty_data.to_csv('cleaned_hkgolden.csv', index=False)
        print("已创建空的 cleaned_hkgolden.csv")

def check_dependencies():
    """
    检查脚本所需的依赖项。
    如果缺少依赖项，提示用户安装。
    """
    try:
        import pandas  # 示例依赖
    except ImportError:
        print("错误：未安装必要的依赖项 'pandas'。")
        print("请运行以下命令安装依赖：")
        print("pip install pandas")
        sys.exit(1)

def run_step(description, command):
    """
    运行系统命令并捕获错误信息。
    """
    print(f"开始：{description}")
    result = os.system(command)
    if result != 0:
        print(f"错误：{description} 失败")
        raise RuntimeError(f"步骤失败：{description}")

def main():
    """
    主函数，按照以下流程运行：
    1. 初始化环境。
    2. 运行爬虫脚本。
    3. 更新数据库。
    4. 输出完成信息。
    """
    try:
        # Step 0: 检查依赖项
        check_dependencies()

        # Step 1: 确保 cleaned_hkgolden.csv 文件存在
        ensure_cleaned_data_exists()

        # Step 2: 运行爬虫脚本
        run_step("正在抓取最新数据...", 'python Scrape_hkgolden_3.1.py')

        # Step 3: 更新数据库并清洗数据
        run_step("正在更新数据库...", 'python final.py')

        # 流程完成
        print("流程完成，数据库已更新！")

    except Exception as e:
        print("\n错误发生！详情如下：")
        traceback.print_exc()  # 打印完整的错误堆栈
        sys.exit(1)

if __name__ == "__main__":
    main()