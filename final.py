import pandas as pd

# Step 1: 读取清洗后的数据，确定基础时间
base_file_path = 'cleaned_hkgolden.csv'  # 清洗后的基础数据文件
base_data = pd.read_csv(base_file_path)

# 打印原始 post_time 列内容，便于调试
print("原始 post_time 列内容：")
print(base_data['post_time'].head())

# 尝试解析时间
base_data['post_time'] = pd.to_datetime(base_data['post_time'], errors='coerce')

# 检查解析结果
if base_data['post_time'].isna().all():
    print("清洗后的数据中所有时间解析失败，请检查时间列内容是否为空或格式不正确")
    print(base_data.head())  # 打印前几行数据以便调试
    base_data['post_time'] = pd.Timestamp("1970-01-01")  # 添加一个默认时间以避免崩溃
    print("使用默认时间 '1970-01-01' 填充 post_time 列")

# 检查解析结果，确保至少有部分时间解析成功
if base_data['post_time'].isna().all():
    print("以下时间无法解析：")
    print(base_data[base_data['post_time'].isna()])
    raise ValueError("清洗后的数据中所有时间解析失败，请检查 'cleaned_hkgolden.csv' 的时间格式是否为标准格式")

# 获取最新基础时间
base_time = base_data['post_time'].max()
print("基础时间:", base_time)

# Step 2: 读取每日爬取数据并筛选出新数据
new_posts_file_path = 'newest_data.csv'
new_posts = pd.read_csv(new_posts_file_path)

# 打印原始 post_time 列内容，便于调试
print("原始 post_time 列内容：")
print(new_posts['post_time'].head(5))

# 指定每日爬取数据的时间解析格式
new_posts['post_time'] = pd.to_datetime(new_posts['post_time'], format='%Y年%m月%d日 %H:%M', errors='coerce')

# 检查解析结果，确保解析成功
if new_posts['post_time'].isna().all():
    print("每日爬取数据中以下时间无法解析：")
    print(new_posts[new_posts['post_time'].isna()])
    raise ValueError("每日爬取数据中所有时间解析失败，请检查 'newest_data.csv' 的时间格式是否为 'YYYY年MM月DD日 HH:MM'")

# 筛选比 base_time 更新的新数据
filtered_posts = new_posts[new_posts['post_time'] > base_time]
print(f"共有 {len(filtered_posts)} 条新数据需要清理")

# Step 3: 清理新数据（删除重复项）
original_count = len(filtered_posts)

# 3.1 删除基于 `id` 和 `post_time` 的重复项
filtered_posts_no_duplicates = filtered_posts.drop_duplicates(subset=['id', 'post_time'])

# 3.2 删除基于 `title` 的重复项，保留 `post_time` 最新的记录
filtered_posts_no_duplicates = filtered_posts_no_duplicates.sort_values(by='post_time', ascending=False)
cleaned_new_posts = filtered_posts_no_duplicates.drop_duplicates(subset=['title'], keep='first')

# 显示删除的行数
deleted_id_post_time_count = original_count - len(filtered_posts_no_duplicates)
deleted_title_count = len(filtered_posts_no_duplicates) - len(cleaned_new_posts)
print(f"基于 'id' 和 'post_time' 删除了 {deleted_id_post_time_count} 条数据")
print(f"基于 'title' 删除了 {deleted_title_count} 条数据")

# Step 4: 合并清理后的新数据和基础数据
updated_data = pd.concat([base_data, cleaned_new_posts], ignore_index=True)

# 确保数据按照时间倒序排列
updated_data = updated_data.sort_values(by='post_time', ascending=False)

# **整合 baseline_clean 的清洗逻辑**：
# 再次全局去重，确保最终数据中没有重复项目
# 1. 删除基于 `id` 和 `post_time` 的重复项
updated_data = updated_data.drop_duplicates(subset=['id', 'post_time'], keep='first')

# 2. 删除基于 `title` 的重复项，保留时间最新的记录
updated_data = updated_data.drop_duplicates(subset=['title'], keep='first')

# 保存清理后的数据到文件
updated_data.to_csv('cleaned_hkgolden.csv', index=False)
print("已将清理后的数据保存至 cleaned_hkgolden.csv")
print(f"最终清理后的数据共有 {len(updated_data)} 行")

# Step 5: 选择并保留所需的列，并保存最终结果
columns_to_keep = ['title', 'username', 'post_time', 'post_content', 'replies', 'url', 'keyword', 'platform']
final_data = updated_data[columns_to_keep]

# **保持时间格式为原始格式**
# 不再格式化 post_time 列，直接输出 datetime 类型
final_data = final_data.sort_values(by='post_time', ascending=False)
final_data.to_csv('hkgolden.csv', index=False)
print("最终清理数据已保存至 hkgolden.csv")

# 保存为 Excel 格式
excel_file_path = 'hkgolden.xlsx'
final_data.to_excel(excel_file_path, index=False, engine='openpyxl')
print(f"最终清理数据已保存至 {excel_file_path} (Excel 格式)")
