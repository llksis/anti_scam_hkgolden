import pandas as pd

# 文件路径
base_file_path = 'cleaned_hkgolden.csv'
new_posts_file_path = 'newest_data.csv'

# 是否启用详细日志
verbose = False

# Step 1: 读取清洗后的数据，确定基础时间
base_data = pd.read_csv(base_file_path)

if verbose:
    print("原始 post_time 列内容：")
    print(base_data['post_time'].head())

# 尝试解析时间
base_data['post_time'] = pd.to_datetime(base_data['post_time'], errors='coerce')

if base_data['post_time'].isna().all():
    raise ValueError("清洗后的数据中所有时间解析失败，请检查 'cleaned_hkgolden.csv' 的时间格式是否为标准格式")

# 获取最新基础时间
base_time = base_data['post_time'].max()
print(f"基础时间: {base_time}")

# Step 2: 读取每日爬取数据并筛选出新数据
new_posts = pd.read_csv(new_posts_file_path)

if verbose:
    print("原始 post_time 列内容：")
    print(new_posts['post_time'].head())

new_posts['post_time'] = pd.to_datetime(new_posts['post_time'], format='%Y年%m月%d日 %H:%M', errors='coerce')

if new_posts['post_time'].isna().all():
    raise ValueError("每日爬取数据中所有时间解析失败，请检查 'newest_data.csv' 的时间格式是否为 'YYYY年MM月DD日 HH:MM'")

filtered_posts = new_posts[new_posts['post_time'] > base_time]
print(f"共有 {len(filtered_posts)} 条新数据需要清理")

# Step 3: 清理新数据（删除重复项）
def remove_duplicates(data, subset, sort_by):
    """删除重复项并按指定列排序"""
    data = data.sort_values(by=sort_by, ascending=False)
    return data.drop_duplicates(subset=subset, keep='first')

filtered_posts_no_duplicates = remove_duplicates(filtered_posts, ['id', 'post_time'], 'post_time')
cleaned_new_posts = remove_duplicates(filtered_posts_no_duplicates, ['title'], 'post_time')

print(f"- 删除基于 'id' 和 'post_time' 的重复项: {len(filtered_posts) - len(filtered_posts_no_duplicates)}")
print(f"- 删除基于 'title' 的重复项: {len(filtered_posts_no_duplicates) - len(cleaned_new_posts)}")

# Step 4: 合并清理后的新数据和基础数据
updated_data = pd.concat([base_data, cleaned_new_posts], ignore_index=True)
updated_data = remove_duplicates(updated_data, ['id', 'post_time'], 'post_time')
updated_data = remove_duplicates(updated_data, ['title'], 'post_time')

# 保存清理后的数据到文件
updated_data.to_csv('cleaned_hkgolden.csv', index=False)
print(f"已将清理后的数据保存至 cleaned_hkgolden.csv ({len(updated_data)} 行)")

# Step 5: 选择并保存最终结果
columns_to_keep = ['title', 'username', 'post_time', 'post_content', 'replies', 'url', 'keyword', 'platform']
final_data = updated_data[columns_to_keep].sort_values(by='post_time', ascending=False)
final_data.to_csv('hkgolden.csv', index=False)
print("最终清理数据已保存至 hkgolden.csv")
'''
#可选excel格式
excel_file_path = 'hkgolden.xlsx'
final_data.to_excel(excel_file_path, index=False, engine='openpyxl')
print(f"最终清理数据已保存至 {excel_file_path} (Excel 格式)")
'''