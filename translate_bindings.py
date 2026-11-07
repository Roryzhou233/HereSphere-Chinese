"""Display labels only: action IDs and Unreal FKey names must stay unchanged."""
import json
from pathlib import Path
from translate_help import rows

actions = {}
for line in """
Delete Current File=删除当前文件
Toggle Menu=显示／隐藏菜单
Temporarily Toggle Menu=临时显示／隐藏菜单
Gaze Click=凝视点击
Left Motion Controller Click=左手体感控制器点击
Right Motion Controller Click=右手体感控制器点击
Mouse Click=鼠标点击
Secondary Click=辅助点击
Menu Up Action=菜单向上操作
Menu Down Action=菜单向下操作
Menu Left Action=菜单向左操作
Menu Right Action=菜单向右操作
Menu Center Action=菜单中央操作
Menu Rotation Action=菜单旋转操作
Smooth Scroll=平滑滚动
Scroll Up=向上滚动
Scroll Down=向下滚动
Play/Pause=播放／暂停
Open Next Media=打开下一个媒体
Open Previous Media=打开上一个媒体
Open Random Media=随机打开媒体
Open Random Playlist=随机打开播放列表
Increment Volume=调整音量
Toggle Mute=切换静音
Increase Playback Speed=提高播放速度
Decrease Playback Speed=降低播放速度
Seek Forward=向前跳转
Seek Backward=向后跳转
Seek Forward Medium=中距离向前跳转
Seek Backward Medium=中距离向后跳转
Seek Forward Long=长距离向前跳转
Seek Backward Long=长距离向后跳转
Seek Forward Percentage=按百分比向前跳转
Seek Backward Percentage=按百分比向后跳转
Seek Next Tag=跳转到下一个标签
Seek Previous Tag=跳转到上一个标签
Frame Step Forward=前进一帧
Frame Step Backward=后退一帧
Toggle AB Loop=切换 AB 循环
Update AB Loop Start=更新 AB 循环起点
Update AB Loop End=更新 AB 循环终点
Update Tag Start=更新标签起点
Update Tag End=更新标签终点
Toggle Favorite=切换收藏
Toggle Always Show Controllers=切换始终显示控制器
Toggle Timestamp Server=切换时间戳服务器
Toggle Synchronized Peripherals=切换外设同步
Play/Pause Peripherals=播放／暂停外设
Next Peripherals Time Offset=下一个外设时间偏移
Previous Peripherals Time Offset=上一个外设时间偏移
Next Peripherals Range=下一个外设运动范围
Previous Peripherals Range=上一个外设运动范围
Toggle Peripherals Oscillation=切换外设往复运动
Next Peripherals Oscillation Speed=下一个外设往复速度
Previous Peripherals Oscillation Speed=上一个外设往复速度
Toggle Peripherals Pattern=切换外设运动模式
Next Peripherals Pattern=下一个外设运动模式
Previous Peripherals Pattern=上一个外设运动模式
Reset Orientation=重置朝向
Recenter Yaw=偏航重新居中
Recenter All=所有朝向重新居中
Rotate Up=向上旋转
Rotate Right=向右旋转
Rotate Clockwise=顺时针旋转
Drag Rotation=拖动旋转
Increment Desktop FOV=调整桌面视场角
Toggle Force Mono=切换强制单目
Perspective Projection Mode=透视投影模式
Equirectangular Projection Mode=等距柱状投影模式
Fisheye Projection Mode=鱼眼投影模式
Toggle Anaglyph=切换红蓝立体辅助视图
Toggle Level Guide=切换水平辅助线
Increment Origin Forward=调整原点前后位置
Increment Origin Right=调整原点左右位置
Increment Origin Up=调整原点上下位置
Move Origin Forward=前后移动原点
Move Origin Right=左右移动原点
Move Origin Up=上下移动原点
Drag Origin=拖动原点
Toggle Motion=切换头部位移跟踪
Recenter Motion=头部位移重新居中
Increment Motion Distance=调整头部位移距离
Update Motion Distance=更新头部位移距离
Increment Focus Pitch=调整对焦俯仰角
Increment Focus Yaw=调整对焦偏航角
Reset Focus Direction=重置对焦方向
Toggle Autofocus=切换自动对焦
Increment True FOV=调整实际镜头视场角
Offset Sensor Shift X=反向调整双眼水平平移
Offset Sensor Shift Y=反向调整双眼垂直平移
Increment Sensor Shift X=同向调整双眼水平平移
Increment Sensor Shift Y=同向调整双眼垂直平移
Offset Sensor Scale X=反向调整双眼水平缩放
Offset Sensor Scale Y=反向调整双眼垂直缩放
Increment Sensor Scale X=同向调整双眼水平缩放
Increment Sensor Scale Y=同向调整双眼垂直缩放
Increment Stereo Alignment Pitch=调整立体对齐俯仰角
Increment Stereo Alignment Yaw=调整立体对齐偏航角
Increment Stereo Alignment Roll=调整立体对齐翻滚角
Increment Stereo Alignment Right=调整立体对齐水平间距
Recenter Screen=屏幕重新居中
Increment Screen Distance=调整屏幕距离
Increment Screen Height=调整屏幕高度
Increment Screen Curve=调整屏幕曲率
Next Aspect Ratio=下一个宽高比
Previous Aspect Ratio=上一个宽高比
Toggle Multiscreen=切换多屏模式
Focus Multiscreen=聚焦／取消聚焦单个屏幕
Toggle Multiscreen Audio Switching=切换多屏自动音频切换
Multiscreen Play/Pause=多屏播放／暂停
""".strip().splitlines():
    source, target = line.split('=', 1)
    actions[source] = target
for i in range(0, 100, 10):
    actions[f'Seek Percentage {i}'] = f'跳转到 {i}%'
assert set(r['Key'] for r in rows[249:]) <= actions.keys()

labels = dict(actions)
for side, target in [('L', '左'), ('R', '右')]:
    for source, value in {
        'Trigger': '扳机', 'Double Trigger': '双击扳机', 'Grip': '握持键',
        'Double Grip': '双击握持键', 'Direction Up': '方向上', 'Direction Down': '方向下',
        'Direction Left': '方向左', 'Direction Right': '方向右', 'Direction Center': '方向中央',
        **{f'Button {i}': f'按键 {i}' for i in range(1, 7)},
    }.items():
        labels[f'({side}) {source}'] = f'（{target}）{value}'

# Registered controller display labels extracted from the original executable.
# Word replacement is limited to this known list; no runtime IDs are rewritten.
terms = {
    'Gamepad': '手柄', 'MotionController': '体感控制器', '(L)': '（左）', '(R)': '（右）',
    'D-pad': '十字键', 'Thumbstick': '摇杆', 'Trackpad': '触控板', 'Touchpad': '触控板',
    'Left': '左', 'Right': '右', 'Up': '上', 'Down': '下', 'Center': '中央',
    'Trigger': '扳机', 'Grip': '握持键', 'Bumper': '肩键', 'Shoulder': '肩键',
    'Button': '按键', 'Face': '面部', 'Bottom': '下', 'Top': '上', 'Special': '特殊键',
    'Back': '返回', 'Start': '开始', 'Options': '选项', 'Menu': '菜单', 'System': '系统',
    'Home': '主页', 'Press': '按下', 'Click': '点击', 'Touch': '触摸', 'Axis': '轴',
    'X-Axis': 'X 轴', 'Y-Axis': 'Y 轴', 'Vector': '向量', 'Force': '压力',
    'Pinch': '捏合', 'Grab': '抓握', 'Proximity': '接近感应',
    'Circle': '圆圈', 'Square': '方块', 'Triangle': '三角',
}
for source in json.loads((Path(__file__).parent/'native-key-labels.json').read_text(encoding='utf-8')):
    if source not in labels and (source.startswith('Gamepad ') or '(L)' in source or '(R)' in source):
        target = ' '.join(terms.get(word, word) for word in source.split(' '))
        if target != source:
            labels[source] = target
labels.update({
    'Mouse X': '鼠标 X 轴', 'Mouse Y': '鼠标 Y 轴', 'Mouse Wheel Axis': '鼠标滚轮轴',
    'Mouse Wheel Up': '滚轮向上', 'Mouse Wheel Down': '滚轮向下',
    'Left Mouse Button': '鼠标左键', 'Right Mouse Button': '鼠标右键',
    'Middle Mouse Button': '鼠标中键', 'Thumb Mouse Button': '鼠标侧键 1',
    'Thumb Mouse Button 2': '鼠标侧键 2', 'Mouse Button 4': '鼠标侧键 1', 'Mouse Button 5': '鼠标侧键 2',
    'Left Shift': '左 Shift', 'Right Shift': '右 Shift', 'Left Ctrl': '左 Ctrl',
    'Right Ctrl': '右 Ctrl', 'Left Control': '左 Ctrl', 'Right Control': '右 Ctrl',
    'Left Alt': '左 Alt', 'Right Alt': '右 Alt', 'Escape': 'Esc', 'Space Bar': '空格',
    'Spacebar': '空格', 'Backspace': '退格', 'Enter': '回车', 'Return': '回车',
    'Delete': '删除', 'Insert': '插入', 'Home': '行首', 'End': '行尾',
    'Page Up': '上一页', 'Page Down': '下一页', 'Caps Lock': '大写锁定',
    'Num Lock': '数字锁定', 'Scroll Lock': '滚动锁定', 'Print Screen': '截屏',
    'Pause': '暂停', 'Left': '左方向键', 'Right': '右方向键',
})
