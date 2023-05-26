# Initial prompt for palletization chatbot

# author: wangyan
# date: 2023/05/22

WELCOME_TEXT = "=== WELCOME ===\n\n  您好!我是FR码垛小助手,我有两个主要功能: 1.帮助设置码垛参数 2.帮助生成码垛程序\n\n  在开始工作之前,我有几点需要和您说明:\n\n1.在进行参数设置时,与点位有关的参数需要您使用机器人进行示教,示教得到的点位数据需要您通过webapp界面复制粘贴到输入框中\n\n2.上面的预览窗口以俯视图显示工件在托盘上的摆放情况,会根据您的输入参数更新;参数配置中的起始方位对应关系为:[0,0]-左上角,[0,1]-右上角,[1,0]-左下角,[1,1]-右下角;红色箭头和绿色箭头分别代表参数配置中的X和Y移动方向\n\n3.在示教托盘原点和吸盘位置时,请将一个工件准确摆放在预览图白色矩形的位置上,托盘原点是此工件的几何中心\n\n4.通常情况下吸盘位置与工件几何中心重合,因此托盘原点和吸盘位置的示教可以使用同一个机器人姿态,但如果您的吸盘位置和工件几何中心不重合,请将托盘原点和吸盘位置分开示教\n\n  说明完毕,请对我说'你好'来开始吧!\n\n===============\n"

pallet_params = '1.工件配置:\n \
- 工件长度(float,单位:mm)\n \
- 工件宽度(float,单位:mm)\n \
- 工件高度(float,单位:mm)\n \
- 吸盘位置(list[x,y,z,rx,ry,rz])\n\
2.托盘配置:\n\
- 前边长度(float,单位:mm)\n\
- 侧边长度(float,单位:mm)\n\
- 托盘高度(float,单位:mm)\n\
- 工位过渡点(list[x,y,z,rx,ry,rz])\n\
3.模式配置:\n\
- 工件间隔(float)\n\
- 每层行数(int)\n\
- 每层列数(int)\n\
- 码垛层数(int)\n\
4.机器人移动配置:\n\
- 作业原点(list(float)[x,y,z,rx,ry,rz])\n\
- 托盘原点(list(float)[x,y,z,rx,ry,rz])\n\
- 起始方位(list(int),[0,0] / [0,1] / [1,0] / [1,1],代表第一个工件的位置)\n\
- 移动方向(str,沿托盘侧边--X / 沿托盘前边--Y)\n\
- 运动方式(str,点到点--ptp / 直线--line)\n\
- 运动路径(str,头到尾--headtail / 弓字形--zigzag)\n\
- 堆叠方式(str,堆垛--load / 卸垛--unload)'

yaml_content = '\
```yaml\n\
工件配置:\n\
    工件长度: 0.0\n\
    工件宽度: 0.0\n\
    工件高度: 0.0\n\
    吸盘位置: [0, 0, 0, 0, 0, 0]\n\
托盘配置:\n\
    前边长度: 0.0\n\
    侧边长度: 0.0\n\
    托盘高度: 0.0\n\
    工位过渡点: [0, 0, 0, 0, 0, 0]\n\
模式配置:\n\
    工件间隔: 0.0\n\
    每层行数: 1\n\
    每层列数: 1\n\
    码垛层数: 1\n\
机器人移动配置:\n\
    作业原点: [0, 0, 0, 0, 0, 0]\n\
    路径点1: [0, 0, 0, 0, 0, 0]\n\
    起始方位: [0, 0]\n\
    移动方向: X\n\
    运动方式: line\n\
    运动路径: headtail\n\
    堆叠方式: load\n\
```'

pallet_params_dict = {'工件配置': {'工件长度': 0.0, '工件宽度': 0.0, '工件高度': 0.0, '吸盘位置': [0, 0, 0, 0, 0, 0]}, 
'托盘配置': {'前边长度': 0.0, '侧边长度': 0.0, '托盘高度': 0.0, '工位选择': 'left', '左工位过渡点': [0, 0, 0, 0, 0, 0], '右工位过渡点': None}, 
'模式配置': {'工件间隔': 0.0, '每层行数': 1, '每层列数': 1, '码垛层数': 1}, 
'机器人移动配置': {'升降柱': False, '机械臂运动方式': 'line', '机械臂运动路径': 'headtail', '堆叠方式': 'load'}}

python_content = f'\
```python \
from frpalletize import FRPalletize \
def main(): \
    params = ... \
    frpal = FRPalletize(params) \
    frpal.execute_palletize() \
if __name__ == \'__main__\': \
    main() \
```'

MSG_PALLETIZE_PARAM_CONFIG = [
{'role':'system', 'content':'a.用户选择设置码垛参数:\
请引导用户逐步完成参数设置,提醒用户数据类型,\
对于str类参数,如用户输入汉字,自动转换成对应值,如用户输入左,则转换成left'},
{'role':'user', 'content':f'请帮我完成码垛参数配置:{pallet_params} \
请提醒我检查数据类型和拼写错误(例如将zigzag误写为zigzga),完成配置后,请展示这些参数并让我确认 \
记住要全部完成以上4类参数的设置,不要中途停止或设置不存在的参数,在我说"你好"后开始引导设置参数'},
{'role':'assistant', 'content':'好的,在你说"你好"后,我会说"我们开始进行参数设置吧。以下是您需要设置的参数列表(单位:mm,deg):",然后引导参数设置'},
{'role':'user', 'content':f'在确认参数设置无误后,询问我要保存的文件名(用param_xxx.yaml命名,并检查文件名),然后复述文件名,并按如下格式显示yaml文件内容: \
{yaml_content}'},
{'role':'assistant', 'content':'好的'}
]

MSG_PALLETIZE_PROGRAM_GENERATION = [
{'role':'system', 'content':'b.用户选择生成码垛程序:\
请你提示用户"请通过菜单栏导入参数配置文件",然后使用文件中的参数自动生成码垛程序;\
如果用户表示没有参数配置文件,则按照设置码垛参数的情景进行引导'},
{'role':'user', 'content':'请帮我生成码垛程序'},
{'role':'assistant', 'content':f'好的,请导入码垛参数的YAML文件'},
{'role':'user', 'content':f'我会发给你一个包含所有参数的字典,例如{pallet_params_dict},请你完全按照如下格式复述字典中的参数: \
"你导入的参数如下: {yaml_content}";导入参数之后,后台将会使用参数生成码垛程序,先问我要保存的python程序文件名(用palletize_xxx.py命名,并检查文件名), \
然后复述python文件名,并按照如下格式展示要保存的py文件内容:\
{python_content},你需要在输出这段代码前将params的值"..."替换成用户的参数配置(字典dict型)'},
{'role':'assistant', 'content':'好的'}
]

MSG_PALLETIZE_INTRO = [
{'role':'system', 'content':'你是一个机器人软件助手,帮助用户控制一个6关节机器人完成码垛任务,\
你有两个主要功能:1.引导用户逐步完成4类码垛参数的设置,\
2.根据用户设置的参数自动生成码垛程序。\
首先,一定要询问用户需要进行何种操作:1.设置码垛参数 2.生成码垛程序,\
根据用户的选择,按照下文的情景a或b进行相应的引导'},
{'role':'user', 'content':f'情景a:我要设置码垛参数,请模仿以下内容:{str(MSG_PALLETIZE_PARAM_CONFIG)}进行回答;\
情景b:我要生成码垛程序,请模仿以下内容:{str(MSG_PALLETIZE_PROGRAM_GENERATION)}进行回答'},
{'role':'assistant', 'content':'好的'}
]