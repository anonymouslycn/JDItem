# coding=utf-8
import os,json
import jieba
import csv
from collections import Counter
from wordcloud import WordCloud,ImageColorGenerator
import matplotlib.pyplot as plt
from wordcloud import WordCloud,ImageColorGenerator
import matplotlib.font_manager as fm
from PIL import Image
import numpy as  np
from scipy.ndimage import gaussian_gradient_magnitude
import matplotlib.pyplot as plt


filelist = os.listdir("./")
filelist = [i for i in filelist if "data" in i]
print (filelist)
stopwords_path='CNstopwords.txt'
brand = []
brandkey = []
prices = []
commit_all = ''

def jiebaclearText(text):
    #定义一个空的列表，将去除的停用词的分词保存
    mywordList=[]
    #进行分词
    seg_list=jieba.cut(text,cut_all=False)
    #将一个generator的内容用/连接
    listStr='/'.join(seg_list)
    #打开停用词表
    f_stop=open(stopwords_path,'r')
    #读取
    try:
        f_stop_text=f_stop.read()
    finally:
        f_stop.close()#关闭资源
    #将停用词格式化，用\n分开，返回一个列表
    f_stop_seg_list=f_stop_text.split("\n")
    #对默认模式分词的进行遍历，去除停用词
    for myword in listStr.split('/'):
        #去除停用词
        # print ((myword),not (myword) in f_stop_seg_list)
        if not (myword) in f_stop_seg_list and len(myword.strip())>1:
            mywordList.append(myword)
    return ' '.join(mywordList)

its = 0

for i in filelist:
    tag = i[5:-4]
    print (tag)
    brand.append(tag)
    f = open(i,"r")
    # f = f.read()
    titlewords = ''
    comments = ''
    papers = []
    for line in f.readlines():
        dic = json.loads(line)
        papers.append(dic)
        its += 1

    for item in papers:
        try:
            v = float(item['price'])
            if v < 1000:
                prices.append(v)
        except:
            pass
        titlewords += jiebaclearText(item['title'])
        if len(item['comments_in_pages']) != 0:
            for t in item['comments_in_pages']:
                comments += jiebaclearText(t['text'])
    if len(comments)!=0:
        commit_all += comments
        comments = comments.split()
        result = Counter(comments)
        d = sorted(result.items(), key=lambda x: x[1], reverse=True)
        # print(d)
        brandkey.append([d[:5]])
    else:
        brandkey.append([])
    # print (comments,titlewords)
        
# bf = open('brand.csv','w',encoding='utf-8')
# csv_writer = csv.writer(bf)
# csv_writer.writerow(["品牌","关键词"])
# print (len(brandkey),len(brand))
# for i in range(len(brand)):
#     csv_writer.writerow([brand[i],brandkey[i]])
# bf.close()
# d = os.path.dirname(__file__)

# # bg = np.array(Image.open(os.path.join(d, "bg.jpg")))
# # # print (bg)
# # wc=WordCloud(
# #     background_color="white",
# #     mask=bg,            #设置图片的背景
# #     random_state=42,
# #     font_path='/System/Library/Fonts/Hiragino Sans GB.ttc'   #中文处理，用系统自带的字体
# #     ).generate(commit_all)

# parrot_color = np.array(Image.open(os.path.join(d, "b.jpeg")))
# # subsample by factor of 3. Very lossy but for a wordcloud we don't really care.
# parrot_color = parrot_color[::3, ::3]

# # create mask  white is "masked out"
# parrot_mask = parrot_color.copy()
# parrot_mask[parrot_mask.sum(axis=2) == 0] = 255

# # some finesse: we enforce boundaries between colors so they get less washed out.
# # For that we do some edge detection in the image
# edges = np.mean([gaussian_gradient_magnitude(parrot_color[:, :, i] / 255., 2) for i in range(3)], axis=0)
# parrot_mask[edges > .08] = 255

# # create wordcloud. A bit sluggish, you can subsample more strongly for quicker rendering
# # relative_scaling=0 means the frequencies in the data are reflected less
# # acurately but it makes a better picture
# wc = WordCloud(background_color="white",max_words=2000, mask=parrot_mask, max_font_size=40, random_state=42, relative_scaling=0,font_path='/System/Library/Fonts/Hiragino Sans GB.ttc')

# # generate word cloud
# wc.generate(commit_all)


# # #开始画图
# # plt.imshow(wc,interpolation="bilinear")
# # #为云图去掉坐标轴
# # plt.axis("off")
# # #画云图，显示
# # #plt.figure()
# # plt.show()

# image_colors = ImageColorGenerator(parrot_color)
# wc.recolor(color_func=image_colors)
# plt.figure(figsize=(10, 10))
# plt.imshow(wc, interpolation="bilinear")
# wc.to_file("parrot_new.png")

# plt.figure(figsize=(10, 10))
# plt.title("Original Image")
# plt.imshow(parrot_color)

# plt.figure(figsize=(10, 10))
# plt.title("Edge map")
# plt.imshow(edges)
# plt.show()
# #保存云图
# wc.to_file("kouzhao.png")

prop = fm.FontProperties(fname='/System/Library/Fonts/Hiragino Sans GB.ttc')
fig, ax = plt.subplots()
ax.hist(np.array(prices),bins=100)       #载入数据

ax.set_xlabel('价格', fontproperties=prop)     #设置X轴标签
ax.set_ylabel('数量', fontproperties=prop)     #设置Y轴标签
ax.set_title('价格分布', fontproperties=prop)  #设置直方图名称
print ("有效价格："+str(len(prices))+"  评论条目："+str(its))
plt.show()
print (commit_all)
