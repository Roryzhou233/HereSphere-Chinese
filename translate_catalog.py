"""Reviewed Simplified Chinese terms for the installed HereSphere build."""
import json
from pathlib import Path

ROOT = Path(__file__).parent
translations = {}


def pairs(text):
    for line in text.strip().splitlines():
        source, target = line.split("\t", 1)
        translations[source] = target


pairs("""
About	关于
Accept	接受
Add New Track	新增轨道
Add to Playlist	添加到播放列表
Add to playlist	添加到播放列表
Advanced Video Settings	高级视频设置
Alignment	对齐
All Media	全部媒体
Auto Seek Avoids Tag	自动跳转排除标签
Auto Seek Optional Tag	自动跳转可选标签
Auto Seek Requires Tag	自动跳转必含标签
Autocomplete Tag Entry	自动补全标签
Autodetect	自动检测
Backspace	退格
Basic Video Settings	基本视频设置
Cancel	取消
Category	分类
Close	关闭
Color	颜色
Create New Profile	新建配置档案
Decline the HereSphere EULA and exit	拒绝许可协议并退出
Delete	删除
Delete Media Source	删除媒体源
Delete Playlist	删除播放列表
Delete Tag	删除标签
Deselect All	取消全选
Disabled	已禁用
Enter	回车
Exit HereSphere	退出 HereSphere
Export HSP File	导出 HSP 文件
FAQ	常见问题
Favorites	收藏
File Explorer	文件浏览器
File Explorer Bookmark Path	文件书签路径
Format	格式
Gamepad	游戏手柄
Generate Categorized Tags	生成分类标签
Global Setting	全局设置
Global Settings	全局设置
Hide	隐藏
High Definition	高清
I have read and accept the HereSphere EULA	我已阅读并接受 HereSphere 许可协议
Image	图像
Import HSP File	导入 HSP 文件
Insert After	在后面插入
Insert Before	在前面插入
Insert Tag After	在后面插入标签
Insert Tag Before	在前面插入标签
Instructions	操作说明
Invert Selection	反向选择
Key Bindings	按键绑定
Keyboard	键盘
LOAD DEFAULT KEY BINDINGS	载入默认按键绑定
Label	名称
Linear	线性
List Name	列表名称
Login	登录
Logout	退出登录
Main Menu	主菜单
Mass Export HSP Files	批量导出 HSP 文件
Mass Export HSP Files For All Local Videos	为所有本地视频批量导出 HSP 文件
Media Library	媒体库
Media Sources	媒体源
Motion	头部位移
Motion Controller	体感控制器
Mouse	鼠标
Move Down	下移
Move Up	上移
None	无
Option	选项
Orientation	朝向
Origin	视点原点
Overwrite	覆盖
Paste	粘贴
Permanently Delete Actual Files	永久删除实际文件
Permanently Delete Files	永久删除文件
Playlist	播放列表
Playlists	播放列表
Projection	投影
Quick Start	快速入门
Recent	最近播放
Refresh Page	刷新页面
Remove Items From Playlist	从播放列表移除
Remove Playlist Item	移除播放列表项目
Remove Saved Video Settings Only	仅移除已保存的视频设置
Rename Playlist	重命名播放列表
Rename Tag	重命名标签
Rescan Library	重新扫描媒体库
Screen	屏幕
Search	搜索
Search Avoids Tag	搜索排除标签
Search Optional Tag	搜索可选标签
Search Requires Tag	搜索必含标签
Select All	全选
Shift	Shift
Space	空格
Tag	标签
Text	文本
Up	向上
Update End	更新结束点
Update End Time	更新结束时间
Update Start	更新起始点
Update Start Time	更新起始时间
User Guide	使用指南
User Settings	用户设置
Video Tags	视频标签
Web Browser	网页浏览器
Web Browser Bookmark URL	网页书签网址
24-Hour Clock Format	24 小时制
Alpha Coordinates:	透明通道坐标：
Alphabetical Folders	文件夹按字母排序
Always Load HSP	始终载入 HSP
Always Show Controllers	始终显示控制器
Anaglyph View Guide	红蓝立体辅助视图
Aspect Ratio	宽高比
Audio	音频
Audio Track	音轨
Auto Collapse Main Menu	自动收起主菜单
Auto Create HSP File	自动创建 HSP 文件
Auto Focus Accuracy	自动对焦精度
Auto Focus Scale	自动对焦缩放
Auto Focus Sensitivity	自动对焦灵敏度
Auto Hide Menu	自动隐藏菜单
Auto Play After Delete	删除后自动播放
Auto Play Next File	自动播放下一个文件
Auto Seek Tags Criteria	自动跳转标签条件
Auto Switch Screen	自动切换屏幕
Auto Update HSP File	自动更新 HSP 文件
Autofocus	自动对焦
Autoplay	自动播放
Axis	输入轴
Backend	播放后端
Background	背景
Background RGB	背景 RGB
Blue	蓝色
Browse to current file	定位当前文件
Cache	缓存
Camera Stereo Alignment	立体相机对齐
Chroma Key 1:	色度抠像 1：
Chroma Key 2:	色度抠像 2：
Chroma Key 3:	色度抠像 3：
Clock	时钟
Color RGB	颜色 RGB
Columns	列数
Connection Key	连接密钥
Context Menu Text	右键菜单文本
Contrast	对比度
Contrast A	整体对比度
Contrast B	蓝色对比度
Contrast G	绿色对比度
Contrast R	红色对比度
Cursor Pitch	光标俯仰角
Curve	曲率
Cutoff	截断阈值
Date	日期
Default	默认
Description	说明
Desktop FOV	桌面视场角
Direction Pitch/Yaw	对焦方向：俯仰/偏航
Directory	目录
Distance	距离
Distance Imperial Units	距离使用英制单位
Distance Min/Max	最小/最大距离
Distance Override	手动指定距离
Drag Rotation Acts As Toggle	拖动旋转使用开关模式
Drag Rotation With Head	使用头部拖动旋转
Drives	驱动器
Duration	时长
Editable Text Box	可编辑文本框
Emulate Spatial	模拟空间音频
Enable Scrubbing	拖动时更新画面
Enable external subtitle files (srt/ssa/ass)	启用外挂字幕（srt/ssa/ass）
Enabled	已启用
Encoding	编码
Environment	环境
Exponent	指数
Export C1	导出 C1
Export C2	导出 C2
Export C3	导出 C3
Export C4	导出 C4
Export FOV	导出视场角
Export HSP File?	导出 HSP 文件？
Export Lens	导出镜头
Exposure	曝光
Eye Swap	交换左右眼
FPS	帧/秒
Failed to open file.	无法打开文件。
Fallback Directory	备用目录
Fast CPU Copy	快速 CPU 复制
Fast Seek	快速跳转
File Deletion Delay	文件删除延迟
Fixed Distance	固定距离
Flip Front	前后翻转
Flip Right	左右翻转
Flip Up	上下翻转
Force Gaze Cursor	强制使用凝视光标
Force Mono	强制单目
Forward	前方
Gain A	整体增益
Gain B	蓝色增益
Gain G	绿色增益
Gain R	红色增益
Gamma A	整体伽马
Gamma B	蓝色伽马
Gamma G	绿色伽马
Gamma R	红色伽马
Global Settings and Tools	全局设置与工具
Green	绿色
Heatmap Opacity	热力图不透明度
Height	高度
HereSphere Version	HereSphere 版本
Hide Distance Overlay	隐藏距离叠加显示
Hide Menu Tooltips	隐藏菜单提示
Hint Text	提示文字
Homepage	主页
Homepage URL	主页网址
IP Address	IP 地址
IPD	瞳距
Import HSP File?	导入 HSP 文件？
Keep picture quality changes?	保留画质更改？
Key	按键
Layer	按键层
Left Image Flare X/Y	左眼梯形变形 X/Y
Left Image Scale X/Y	左眼缩放 X/Y
Left Image Shear X/Y	左眼斜切 X/Y
Left Image Shift X/Y	左眼平移 X/Y
Left Image Slant X/Y	左眼传感器倾斜 X/Y
Lens	镜头
Level Guide	水平辅助线
Light Despill:	溢色消除：
Light Inject:	光照注入：
Link Server	链接解析服务器
Link Server Url	链接解析服务器网址
Lock Mouse to Window	将鼠标锁定在窗口内
Lock Pitch	锁定俯仰
Lock Roll	锁定翻滚
Lock Yaw	锁定偏航
Logged in as:	当前登录：
Login:	登录：
Loop Media List	循环播放列表
Manual Oscillation Speed	手动往复速度
Manual Script Pattern	手动脚本模式
Mask	遮罩
Media Count	媒体数量
Media Player	媒体播放器
Menu Controls	菜单操作
Menu Position	菜单位置
Menu Sharpen	菜单锐化
Midtones	中间调
Miscellaneous	其他
Move Forward Scale	前后移动倍率
Move Right Scale	左右移动倍率
Move Up Scale	上下移动倍率
Multipart Encodings	多段视频编码
Multiple Screens	多屏模式
Name	名称
Offset A	整体偏移
Offset B	蓝色偏移
Offset G	绿色偏移
Offset R	红色偏移
Opacity Multiplier:	不透明度倍率：
Overwrite Favorite	覆盖收藏
Overwrite Rating	覆盖评分
Overwrite Tags	覆盖标签
Overwrite?	是否覆盖？
Password	密码
Peripheral Disabled	外设已禁用
Pitch	俯仰
Pitch (Position)	俯仰（位置）
Pitch Adjustment Scale	俯仰调整倍率
Play All Screens	播放所有屏幕
Play Count	播放次数
Play Video Links	播放视频链接
Playback	播放
Playlist Duplicates	允许播放列表重复项
Playlist Name	播放列表名称
Port	端口
Prefer Fisheye	优先使用鱼眼投影
Preset	预设
Preview	预览
Profile	配置档案
Profile Creation Prompt	创建配置档案
Profile Name	配置档案名称
Projection Controls	投影操作
Proximity	临近程度
Range Min/Max	最小/最大行程
Read Ahead	预读取
Red	红色
Reduce FOV During Rotation	旋转时缩小视场角
Remember Last Profile	记住上次配置档案
Remember Last URL	记住上次网址
Replace Passthrough With Color	使用纯色替代透视
Rescan	重新扫描
Resolution	分辨率
Resume From Last Position	从上次位置继续播放
Right	右方
Right (Scale)	右方（缩放）
Right Image Flare X/Y	右眼梯形变形 X/Y
Right Image Scale X/Y	右眼缩放 X/Y
Right Image Shear X/Y	右眼斜切 X/Y
Right Image Shift X/Y	右眼平移 X/Y
Right Image Slant X/Y	右眼传感器倾斜 X/Y
Roll	翻滚
Roll Adjustment Scale	翻滚调整倍率
Rotation Applies to Key Frame	旋转应用于关键帧
Rows	行数
Saturation	饱和度
Saturation A	整体饱和度
Saturation B	蓝色饱和度
Saturation G	绿色饱和度
Saturation R	红色饱和度
Save Login	保存登录信息
Scale	倍率
Scale X	缩放 X
Scale Y	缩放 Y
Screen Depth Offset	屏幕深度偏移
Screen Orientation	屏幕朝向
Scroll Speed	滚动速度
Search Name	搜索名称
Search Tags	搜索标签
Searching for Webstream API	正在查找流媒体 API
Seek Percentage	跳转百分比
Seek Seconds	跳转秒数
Seek Seconds Long	长距离跳转秒数
Seek Seconds Medium	中距离跳转秒数
Selected Tag Name	所选标签名称
Sensor and Stitching Adjustments	传感器与拼接调整
Server Enabled	启用服务器
Shadows	阴影
Sharpen	锐化
Shift X	平移 X
Shift Y	平移 Y
Show HSP Confirmation	显示 HSP 确认提示
Show Hidden Files	显示隐藏文件
Size	大小
Soften	柔化
Sort By	排序依据
Source	来源
Spectator Screen	桌面镜像
Speed	速度
Speed Increment	速度步长
Spill Mask	溢色遮罩
Start	开始
Startup Scan	启动时扫描
Stereo	立体模式
Strength	强度
Stretch	拉伸
Studio | Video Title	制作方 | 视频标题
Subtitles	字幕
Sync	同步
Synchronized Peripherals	同步外设
Temperature	色温
Time	时间
Time Offset	时间偏移
Timestamp Server	时间戳服务器
Tint	色调
Transition	过渡
Transition Speed	过渡速度
True C1	实际 C1
True C2	实际 C2
True C3	实际 C3
True C4	实际 C4
True FOV	实际视场角
True Lens	实际镜头
Update Interval	更新间隔
Use Auto Focus	使用自动对焦
Use File Modification Date	使用文件修改日期
Username	用户名
VapourSynth Max Megapixels	VapourSynth 最大百万像素
View Arc	菜单视角
Virtual Keyboard	虚拟键盘
Volume Multiplier	音量倍率
Web Browser FPS	浏览器帧率
Website URL	网站地址
Yaw	偏航
Yaw Adjustment Scale	偏航调整倍率
Zoom	缩放
""")

def indexed(filename, text):
    sources = json.loads((ROOT / filename).read_text(encoding="utf-8"))
    for line in text.strip().splitlines():
        number, target = line.split("\t", 1)
        translations[sources[int(number)]] = target.replace("\\n", "\n")


indexed("remaining-ui.json", r"""
3	已扫描 12/345 个视频
9	将此预设设为菜单居中操作的快捷载入项，便于快速比较。
10	将此预设设为菜单向下操作的快捷载入项，便于快速比较。
11	将此预设设为菜单向左操作的快捷载入项，便于快速比较。
12	将此预设设为菜单向右操作的快捷载入项，便于快速比较。
13	将此预设设为菜单向上操作的快捷载入项，便于快速比较。
14	新增一条轨道，并添加一个填满该轨道的标签。
15	将所选标签加入自动跳转排除条件，跳过包含该标签的视频片段。
16	将所选标签加入自动跳转必含条件，仅播放包含该标签的片段。
17	将所选标签加入自动跳转可选条件，播放包含该标签或其他可选标签的片段。
18	在当前播放时间添加关键帧。
19	新增预设。
20	将当前往复速度加入收藏。
21	将当前行程加入收藏。
22	收藏当前搜索框中的查询条件。
23	将当前时间偏移加入收藏。
24	调整桌面（2D）模式的相机视场角。对 VR 模式无效。
25	调整菜单不透明度。数值越小，菜单越透明。
26	调整浏览器缩放。数值越大，放大程度越高。默认值为 0。
27	通过菜单占据的视角调整菜单大小。视角越大，菜单越大。
28	允许向播放列表中添加重复文件。
29	始终按字母顺序排列文件夹，不受其他排序方式影响。
30	另一段较长文本
31	观看平面屏幕（透视投影）视频时，为字幕添加深度偏移。
32	点击文件打开视频后，自动收起主菜单。
33	若视频没有 HSP 文件，则自动创建。
34	按住辅助选择键调整视频设置时，自动隐藏菜单；松开后恢复显示。
35	列表播放到末尾时，自动从头继续。
36	删除当前文件后，自动播放列表中的下一个文件。
37	当前文件播放结束后，自动播放列表中的下一个文件。
39	第一组抠像颜色的蓝色分量。与该颜色相近的画面区域会变透明，也可用左侧取色器设置。
40	溢色消除颜色的蓝色分量。选择要从主体中去除的反射颜色（例如绿幕染到皮肤上的绿色）。此操作仅校色，不改变透明度；也可使用左侧取色器。
41	第二组抠像颜色的蓝色分量。与该颜色相近的画面区域会变透明，也可用左侧取色器设置。
42	第三组抠像颜色的蓝色分量。与该颜色相近的画面区域会变透明，也可用左侧取色器设置。
46	选择播放后端。Windows 默认使用 Media Foundation；播放 HEVC 等格式可能需要另行购买或安装解码扩展，对老旧格式或 MKV 的兼容性可能有限。\n\nDirectShow 的兼容性通常更好，但需要安装 K-Lite Codec Pack，适合高级用户。
47	点击标签进行编辑，再点一次跳转到标签起点。\n\n按住握持键：\n左：更新起点\n右：更新终点\n上：在前面插入标签\n下：在后面插入标签\n按下摇杆：删除标签
48	点击时间轴跳转，按住并拖动可预览定位。\n上：将当前位置设为 AB 循环起点\n下：将当前位置设为 AB 循环终点
49	点击载入往复速度。
50	点击打开书签。
51	点击载入行程。
52	点击载入已保存的预设。
53	点击载入时间偏移。
54	打开字幕菜单。
55	打开同步外设设置。\n\n颜色表示连接状态：\n白：已禁用\n黄：正在连接或上传脚本\n浅红：需要更新固件\n红：连接失败\n蓝：已连接\n深蓝：当前视频没有脚本\n深紫：脚本上传成功\n紫：正在播放
56	点击打开视频文件。
57	点击搜索此标签。按住握持键并推动摇杆可追加条件。\n左：追加排除条件（NOT）\n上：追加可选条件（OR）\n右：追加必含条件（AND）\n按下摇杆：从搜索中移除此标签
58	颜色：使用纯色背景\n透视：显示头显摄像头画面
59	外设的连接密钥。
60	右键菜单项
61	自动对焦深度检测的分辨率。数值越高越准确，但运算开销也越大；数值较低可改善性能。
62	将当前设置复制到剪贴板。
63	新建播放列表。
65	删除播放列表。
66	删除所选标签。
69	启用外设手动往复运动。启用后将停止使用脚本。
70	启用互动脚本目录中选定的手动模式。
71	启用同步外设。
72	允许 HereSphere 调整同步外设的运动行程。如果希望通过设备本身的按钮控制行程，请关闭此选项。
73	将所有已保存的本地视频设置导出为 HSP 文件？\n每个文件均保存在对应视频所在目录。网络流视频不会导出。操作可能需要一些时间。
76	第一组抠像颜色的绿色分量。与该颜色相近的画面区域会变透明，也可用左侧取色器设置。
77	溢色消除颜色的绿色分量。选择要从主体中去除的反射颜色（例如绿幕染到皮肤上的绿色）。此操作仅校色，不改变透明度；也可使用左侧取色器。
78	第二组抠像颜色的绿色分量。与该颜色相近的画面区域会变透明，也可用左侧取色器设置。
79	第三组抠像颜色的绿色分量。与该颜色相近的画面区域会变透明，也可用左侧取色器设置。
81	隐藏虚拟键盘。
82	数值越高，对物体边缘附近深度变化的检测越敏感，但也可能增加误判。数值越低越稳定，但灵敏度较低。
83	高光
85	若 HSP 文件已存在，则在更改视频设置时自动更新该文件。
86	当视频总像素数低于此值时启用 VapourSynth 滤镜。1080p 约为 2.1 百万像素，2160p 约为 8.3 百万像素。此滤镜允许 Smooth Video Project 等第三方程序在渲染前处理画面，但会增加开销，建议设为低于 8.4 百万像素（4096×2048）。
87	如果所选标签后方有空位，在同一轨道插入新标签。
88	如果所选标签前方有空位，在同一轨道插入新标签。
91	关键帧时间戳；点击可跳转。\n按住握持键后向左/右推动摇杆，可前移/后移时间戳。
93	锁定菜单的位置和旋转。
96	检测到左右并排的 VR 视频时，默认使用鱼眼投影而非等距柱状投影。
97	最大运动行程。
98	最小运动行程。
99	将所选标签移动到下一条轨道。
100	将所选标签移动到上一条轨道。
102	没有找到视频。\n请尝试更改搜索条件，并用英文逗号分隔多个搜索项。
104	以毫秒为单位偏移时间戳。
105	打开在线 API 设置，可重新扫描媒体库，或设置是否覆盖评分、收藏与标签。
106	打开浏览器设置，可调整主页、帧率和缩放。
107	打开选择菜单，可全选、取消全选或反选。
108	打开菜单不透明度滑块。
109	打开菜单，将项目加入播放列表。
110	打开遮罩设置。
112	从剪贴板粘贴。
113	将剪贴板内容粘贴到设置中。
114	暂停同步外设，同时让视频继续播放。
115	永久删除以下文件？\n文件不会进入回收站，删除后需借助文件恢复软件才可能恢复。
116	点击画面取色。
117	请等待已打开的文件关闭。
118	请等待配置档案载入完成。
119	正在批量导出 HSP 文件，请稍候。完成后此提示会自动关闭。
120	请按下要绑定的按键。
123	较长文本
124	将屏幕或头部位移位置重新居中。
125	重新连接同步外设。
126	第一组抠像颜色的红色分量。与该颜色相近的画面区域会变透明，也可用左侧取色器设置。
127	溢色消除颜色的红色分量。选择要从主体中去除的反射颜色（例如绿幕染到皮肤上的绿色）。此操作仅校色，不改变透明度；也可使用左侧取色器。
128	第二组抠像颜色的红色分量。与该颜色相近的画面区域会变透明，也可用左侧取色器设置。
129	第三组抠像颜色的红色分量。与该颜色相近的画面区域会变透明，也可用左侧取色器设置。
130	重新载入当前网页。
131	仅移除已保存的设置，还是永久删除以下文件？\n文件不会进入回收站，删除后需借助文件恢复软件才可能恢复。
132	从播放列表移除以下项目，还是永久删除实际文件？\n文件不会进入回收站，删除后需借助文件恢复软件才可能恢复。
133	从媒体库移除此媒体源？\n该媒体源的所有已保存视频设置都会被移除。
134	移除此预设。
135	移除当前关键帧。
136	从收藏中移除所选往复速度。
137	从收藏中移除所选行程。
138	从收藏中移除所选搜索项。
139	从收藏中移除所选时间偏移。
140	重命名播放列表。
141	重命名预设。
142	使用纯色替代头显透视画面。适合不想显示透视，或希望 Virtual Desktop 等应用将纯色替换成其自身透视画面的情况。
143	重新发送当前视频路径，以便其他未成功同步的应用再次同步。
145	将当前设置保存到此预设。
146	根据自动对焦深度缩放字幕距离。
147	重新扫描媒体源，更新文件列表。
148	搜索包含此标签或其他可选标签的视频。
149	搜索包含此标签的视频。
150	搜索不包含此标签的视频。
151	选择要播放的手动脚本模式。在互动脚本目录中创建名称以 Pattern 开头的脚本文件，即可添加模式。可用“下一个/上一个外设脚本模式”按键绑定切换。
152	选择要删除的行程。
153	选择背景类型。\n全局设置：沿用用户设置\n颜色：纯色背景\n透视：头显摄像头画面
154	将“拖动旋转”设为按一下开、再按一下关，无需持续按住。
155	用头部运动拖动旋转视频朝向，而不是使用体感控制器。
156	时钟使用 24 小时制，而非带上午/下午标记的 12 小时制。
157	调整旋转不正确的平面视频朝向。\n按住握持键：上/下切换；按下摇杆恢复“向上”。
158	导入或导出 HSP 文件时显示确认提示。
159	显示批量导出所有本地视频设置为 HSP 文件的提示。
160	显示并重命名此搜索条件的名称。
161	以列表形式显示文件。
162	以缩略图形式显示文件。
163	仅显示已收藏的文件。
164	显示删除当前文件的确认提示。
166	文本块
167	感谢试用 HereSphere！如果喜欢这款软件，请考虑购买完整版；完整版不会显示此试用提示。谢谢！
168	透明通道的水平缩放比例，相对于正常彩色图像计算。例如透明通道图像宽度为彩色图像的 40%，则设为 0.4。
169	透明通道的垂直缩放比例，相对于正常彩色图像计算。例如透明通道图像高度为彩色图像的 40%，则设为 0.4。
170	用于定位内嵌透明通道图像的水平偏移。例如向右偏移彩色图像宽度的四分之一，则设为 0.25。
171	用于定位内嵌透明通道图像的垂直偏移。例如向上偏移彩色图像高度的一半，则设为 -0.5。
172	用于替代透视画面的背景颜色蓝色分量。
173	观看透视投影视频时，背景颜色的蓝色分量。
174	背景颜色的蓝色分量。
175	决定颜色需要多接近抠像色才变为完全透明。截断阈值越高，完全透明的区域越大。
176	决定颜色需要多接近溢色消除色才进行校正。截断阈值越高，消除的溢色越多，适合去除主体周围的绿幕光晕。
177	过渡时长，单位为秒。\n按住握持键：上/下步长 1；左/右步长 0.1；按下摇杆恢复 0；按住扳机并转动控制器可连续调整。
178	调整透明度曲线。指数大于 1 时透明区域会更加透明，小于 1 时透明程度降低。建议保留默认值 1。
179	调整经过截断和柔化处理后的校色范围。指数大于 1 会扩大校色范围，小于 1 会缩小。建议保留默认值 1。
180	浏览器画面的渲染帧率。
181	用于替代透视画面的背景颜色绿色分量。
182	观看透视投影视频时，背景颜色的绿色分量。
183	背景颜色的绿色分量。
184	溢色消除强度。数值越高，校色越强；数值越低，变化越轻微。
185	链接解析服务器接收当前网页地址，返回可播放的视频和音频链接。
186	自动跳转所使用的条件列表。
187	手动往复速度，范围为 0 到 1。
188	遮罩用于隐藏画面的部分区域。\n无：保留原画面\n色度抠像：根据指定颜色隐藏区域\n内嵌透明通道：根据视频中独立嵌入的图像设置透明度
189	自动对焦允许的最大距离，单位为厘米。请参考场景中最远物体的距离。缩小最小/最大距离范围可减少深度跳变；距离变化很大时使用多个关键帧。如果无需对焦背景，可降低此值以关注近处。\n按住握持键：上/下步长 100；左/右步长 10；按下摇杆恢复 1000；按住扳机并转动控制器可连续调整。
190	自动对焦允许的最小距离，单位为厘米。请参考物体最靠近相机时的距离。缩小最小/最大距离范围可减少深度跳变；距离变化很大时使用多个关键帧。\n按住握持键：上/下步长 1；左/右步长 0.1；按下摇杆恢复 10；按住扳机并转动控制器可连续调整。
191	音量倍率，可统一不同片段的响度。\n按住握持键：上/下步长 0.1；左/右步长 0.01；按下摇杆恢复 1；按住扳机并转动控制器可连续调整。
192	删除网络文件前，等待文件关闭的秒数。
193	视频累计播放次数。
194	调整最终不透明度。小于 1 会使画面更透明，大于 1 会使画面更不透明。
195	时间轴上热力图的不透明度；数值越低越透明。
196	字幕相对于头部朝向的垂直角度。
197	所选标签的评分。
198	用于替代透视画面的背景颜色红色分量。
199	观看透视投影视频时，背景颜色的红色分量。
200	背景颜色的红色分量。
201	决定颜色需要多接近抠像色才变为半透明。数值越高，半透明范围越大，适合柔化头发等物体的边缘。
202	以渐变方式消除溢色。柔化值越高，逐渐校色的范围越大，适合去除主体整体的绿幕染色。
203	自动对焦深度变化的速度。较低数值更慢、更平滑；较高数值更快，但容易跳变。\n按住握持键：上/下步长 0.1；左/右步长 0.01；按下摇杆恢复 1；按住扳机并转动控制器可连续调整。
204	避免绿幕反光导致主体被错误抠除。溢色消除通常建议设为 0，以便识别这些染色区域；如果校正过强，可适当提高。
205	避免绿幕反光导致主体被错误抠除。色度抠像通常建议设为 1；如果需要抠除更多绿幕，可适当降低。
206	关闭自动对焦时的字幕距离。
207	音频时间偏移，单位为秒，用于校正音画同步。\n按住握持键：上/下步长 0.001；左/右步长 0.01；按下摇杆恢复 0；按住扳机并转动控制器可连续调整。
208	开启或关闭声音。
209	开启或关闭自动跳转。
210	打开该组设置的预设列表。\n按住握持键：向左/右可载入对应箭头所指定的预设。
211	打开环境设置的预设列表。\n按住握持键：向左/右可载入对应箭头所指定的预设。
212	打开同步设置的预设列表。打开新文件时，默认载入列表中的第一项。
213	打开收藏的往复速度列表。点击某项即可载入，也可通过“下一个/上一个外设往复速度”按键绑定切换。
214	打开收藏的行程列表。点击某项即可载入，也可通过“下一个/上一个外设行程”按键绑定切换。
215	打开收藏的时间偏移列表。点击某项即可载入，也可通过“下一个/上一个外设时间偏移”按键绑定切换。
216	打开音频设置的预设列表。打开新文件时默认载入第一项。\n按住握持键：向左/右可载入对应箭头所指定的预设。
217	显示或隐藏密码。
218	显示或隐藏隐藏文件和文件夹。
220	将所选标签的结束时间设为当前播放时间。
221	将所选标签的起始时间设为当前播放时间。
222	文件浏览器的日期使用文件修改时间，而非创建时间。
224	音量滑块。
226	自动对焦距离使用英制单位（英尺和英寸）；关闭时使用公制单位（厘米）。
227	以 .mp4 或 .webm 结尾的链接交由 HereSphere 播放，而非在浏览器中打开。
228	将鼠标限制在播放器窗口内，避免误点窗口外的内容。关闭后可移出窗口。更改后可能需要点击播放器窗口才会完全生效。
229	将播放命令发送给所有可见的多屏视频，可同时控制播放、暂停、跳转与速度。
230	视频暂停且开启自动对焦时，不显示距离叠加信息。
231	即使菜单隐藏，也始终显示体感控制器。
232	播放时预读取文件。关闭可能加快打开文件和跳转的速度，但播放期间可能增加缓冲停顿。
233	始终载入网页 API 提供的 HSP 文件，覆盖当前视频设置（包括标签）。默认关闭时，仅在视频尚无已保存设置的情况下载入 HSP 文件。
234	使用在线 API 提供的收藏状态覆盖本地收藏。
235	拖动时间轴时实时更新视频画面。
236	使用在线 API 提供的评分覆盖本地评分。
237	使用在线 API 提供的标签覆盖本地标签。请注意：在 HereSphere 中手动编辑的标签也会被覆盖。关闭时仅补充缺失标签。
238	如果网页 API 提供的编码名称以 File 开头，将其视为分段视频。上一个/下一个视频按键可切换分段，播放结束后也会自动切换。
239	软件解码时使用更快的 CPU 复制方式，可改善流畅度；但在高于 566.36 版本的 Nvidia 驱动上可能导致崩溃。
240	观看 VR 视频时，根据自动对焦深度实时调整字幕距离。
241	窗口未获得焦点。请点击桌面上的 HereSphere 窗口。
242	将去除非法文件名字符后的视频标题写入备用脚本目录，文件名为 [Video Title].title。可用该标题重命名脚本，使网络视频播放时也能找到对应脚本。
245	是 / 否 / 可能
""")

if __name__ == "__main__":
    (ROOT / "translations.json").write_text(json.dumps(translations, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Translations: {len(translations)}")
