import pandas as pd
from datetime import datetime

# 读取原始 CSV 数据
file_path = 'cleaned_data.csv'  # 替换为实际路径
data = pd.read_csv(file_path)
original_count = len(data)

# 创建备份文件
backup_file_path = f"backup_cleaned_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
data.to_csv(backup_file_path, index=False)
print(f"备份文件已保存至: {backup_file_path}")

# Step 1: 删除基于 `id` 和 `post_time` 的重复项
data['post_time'] = pd.to_datetime(data['post_time'], format='%Y年%m月%d日 %H:%M', errors='coerce')
data_no_id_publish_duplicates = data.drop_duplicates(subset=['id', 'post_time'])

# 显示基于 `id` 和 `post_time` 被删除的重复项
id_publish_duplicates = data[data.duplicated(subset=['id', 'post_time'], keep=False)]
deleted_id_publish_count = original_count - len(data_no_id_publish_duplicates)

# Step 2: 删除 `title` 重复项，保留 `post_time` 最新的行
data_sorted = data_no_id_publish_duplicates.sort_values(by='post_time', ascending=False)
cleaned_data = data_sorted.drop_duplicates(subset=['title'], keep='first')

# 保存清理后的数据到新文件
cleaned_file_path = 'cleaned_data.csv'
cleaned_data.to_csv(cleaned_file_path, index=False)

# 计算总删除的行数
final_deleted_count = original_count - len(cleaned_data)
print("清理完成，共删除了", final_deleted_count, "条数据，数据已保存至:", cleaned_file_path)