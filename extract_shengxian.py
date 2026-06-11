#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提取生鲜类目内容，生成独立的 HTML 页面
"""

from bs4 import BeautifulSoup
import re

# 读取原始 HTML
with open('index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')

# 1. 修改标题
title_tag = soup.find('title')
if title_tag:
    title_tag.string = '生鲜创意素材分析'

h1_tag = soup.find('h1', class_='report-title')
if h1_tag:
    h1_tag.string = '🥩 生鲜创意素材分析'

# 2. 修改副标题
subtitle = soup.find('div', class_='report-subtitle')
if subtitle:
    subtitle.clear()
    subtitle.append(soup.new_tag('span'))
    subtitle.span.string = '🥩 专注生鲜行业'
    subtitle.append(soup.new_tag('span'))
    subtitle.contents[1].string = '🤖 Gemini 全视频AI分析'

# 3. 删除行业筛选器（只有生鲜一个行业）
industry_filter_group = soup.find('select', id='industryFilter')
if industry_filter_group:
    filter_group_parent = industry_filter_group.find_parent('div', class_='filter-group')
    if filter_group_parent:
        filter_group_parent.decompose()

# 4. 提取生鲜类目选项，删除其他类目
category_filter = soup.find('select', id='categoryFilter')
if category_filter:
    # 保留生鲜相关的类目
    shengxian_categories = [
        '海参', '鸡肉', '即食肉类', '南北干货', '榴莲', '鱼类',
        '牛肉', '鲜活蛋类', '贝类', '半成品菜/预制菜', '鸭肉',
        '坚果炒货', '苹果'
    ]
    
    # 删除不相关的 option
    for option in category_filter.find_all('option'):
        if option.get('value') not in ['all'] + shengxian_categories:
            option.decompose()

# 5. 删除茶叶和酒水的 tier tab
tier_tabs = soup.find('div', class_='tier-tabs')
if tier_tabs:
    for tab in tier_tabs.find_all('div', class_='tier-tab'):
        if tab.get('data-industry') in ['茶叶', '酒水']:
            tab.decompose()

# 6. 删除茶叶和酒水的 tier panel
for panel in soup.find_all('div', class_='tier-panel'):
    if panel.get('data-industry') in ['茶叶', '酒水']:
        panel.decompose()

# 7. 删除茶叶和酒水的卡片
for card in soup.find_all('div', class_='card'):
    if card.get('data-industry') in ['茶叶', '酒水']:
        card.decompose()

# 8. 删除茶叶和酒水的 gallery section
for gallery in soup.find_all('div', class_='gallery-section'):
    if gallery.get('data-industry') in ['茶叶', '酒水']:
        gallery.decompose()

# 9. 统计生鲜素材数量
shengxian_cards = soup.find_all('div', class_='card', attrs={'data-industry': '生鲜'})
total_count = len(shengxian_cards)

# 更新筛选器中的数量显示
filter_count = soup.find('div', class_='filter-count')
if filter_count:
    filter_count.clear()
    filter_count.string = f'共 '
    strong_tag = soup.new_tag('strong')
    strong_tag.string = str(total_count)
    filter_count.append(strong_tag)
    filter_count.append(soup.new_string(' 条素材'))

# 10. 保存修改后的 HTML
output_html = str(soup)

# 写入新文件
with open('index_shengxian.html', 'w', encoding='utf-8') as f:
    f.write(output_html)

print(f'✅ 提取完成！')
print(f'📊 生鲜素材数量: {total_count} 条')
print(f'📁 输出文件: index_shengxian.html')
