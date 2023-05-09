# Here is a script to run a simple GUI to use the ChatBot
# Written with the help of ChatGPT
#
# author: wangyan, chatgpt
# date: 2023/05/06

# Importing libs
from frchat.frchatbot import FRChatBot
import re
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv("dev.env"))  # read local .env file

import tkinter as tk
from tkinter import filedialog
import datetime

# 设置ChatBot
## Providing a context to start a conversation topic
messages = [
    {'role':'system', 'content':'你是一个机器人用户助手,帮助用户控制一个6关节机器人运动, \
     你需要组合使用一些函数来完成特定任务,只使用用户提供的函数,不要自行引入其他第三方库(如RoboDK)'},
    {'role':'user', 'content':'你好,请编写机器人控制指令,假设已实例化对象robot=frrpc.RPC(192.168.58.2), \
     用户提供的函数均为对象的方法.请在每次输出程序时加上机器人实例化部分的指令'},
    {'role':'assistant', 'content':'好的，请告诉我能够使用哪些函数'},
    {'role':'user','content':'我需要添加一些约束条件：最终生成的代码都需要是可执行的函数，并返回函数名称'},
    {'role':'assistant','content':'好的'},
    {'role': 'user', 'content': '最终返回一个可执行的main函数'},
    {'role': 'assistant', 'content': '好的'},

]
## Instantiating a ChatBot
frcb = FRChatBot(messages, temperature=0.1)

# 交互界面
## 创建主窗口
root = tk.Tk()
root.title("Fairy小助手")
root.geometry("1024x512")
font=('Times New Roman', 10)
## 创建输入历史框和用户输入框
frame_left = tk.Frame(root)
frame_left.pack(side="left", fill="both", expand=True, padx=10, pady=10)
### 创建输入历史框
label_input = tk.Label(frame_left, text="输入历史", font=font)
label_input.grid(row=0, column=0, sticky="w")
scrollbar_input_history = tk.Scrollbar(frame_left)
text_input_history = tk.Text(frame_left, 
                             width=10, 
                             height=10, 
                             yscrollcommand=scrollbar_input_history.set,
                             font=font)
text_input_history.grid(row=1, column=0, sticky="nsew")
scrollbar_input_history.config(command=text_input_history.yview)
scrollbar_input_history.grid(row=1, column=1, sticky="ns")
### 创建用户输入框
label_input = tk.Label(frame_left, text="请输入(Ctrl+s发送)", font=font)
label_input.grid(row=2, column=0, sticky="w")
scrollbar_input = tk.Scrollbar(frame_left)
text_input = tk.Text(frame_left, 
                     width=10, 
                     height=10, 
                     yscrollcommand=scrollbar_input.set,
                     font=font)
text_input.grid(row=3, column=0, sticky="nsew")
scrollbar_input.config(command=text_input.yview)
scrollbar_input.grid(row=3, column=1, sticky="ns")

frame_right = tk.Frame(root)
frame_right.pack(side="right", fill="both", expand=True, padx=10, pady=10)
## 创建输出框
label_output = tk.Label(frame_right, text="小助手", font=font)
label_output.grid(row=0, column=0, sticky="w")
scrollbar_output = tk.Scrollbar(frame_right)
text_output = tk.Text(frame_right, 
                      width=10, 
                      height=20, 
                      yscrollcommand=scrollbar_output.set,
                      font=font)
text_output.grid(row=1, column=0, sticky="nsew")
scrollbar_output.config(command=text_output.yview)
scrollbar_output.grid(row=1, column=1, sticky="ns")

## 让文本框适应窗口大小
frame_left.rowconfigure(1, weight=1)
frame_left.rowconfigure(3, weight=1)
frame_left.columnconfigure(0, weight=1)
frame_left.columnconfigure(1, weight=0)
frame_right.rowconfigure(1, weight=1)
frame_right.columnconfigure(0, weight=1)
frame_right.columnconfigure(1, weight=0)

## 禁止输入历史框和输出框编辑
text_input_history.config(state="disabled")
text_output.config(state="disabled")

## 导入配置文件内容
### 创建一个空菜单，用于添加文件选项
menubar = tk.Menu(root) 
filemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="配置文件", menu=filemenu)
### 定义打开文件方法
def open_file():
    filename = filedialog.askopenfilename(filetypes=[("yaml files", "*.yaml")])
    if filename:
        print(f"选择的配置文件: {filename}")
        # 读取配置文件内容并添加到输入框
        output = frcb.generate_function_list(filename)
        text_input.insert("end", str(output))
### 将 “打开” 选项添加到菜单中
filemenu.add_command(label="打开", command=open_file)
### 将单栏添加到主窗口中
root.config(menu=menubar)

## 消息处理
### 保存输入历史并添加时间戳
def save_input_history(message):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    text_input_history.configure(state="normal")
    text_input_history.insert("end", f"\n====={now}=====\n{message}")
    text_input_history.configure(state="disabled")
    text_input_history.see('end')

### 让输入框在每次输入后自动滚动到底部
def on_input_change(*_):
    text_input.yview_moveto(1.0)
text_input.bind("<KeyPress>", on_input_change)

### 处理用户输入并返回消息

def process_message():
    time_step = 0
    prompt= text_input.get("1.0", "end")
    # print('prompt:',prompt)
    if prompt:            
        text_input.delete("1.0", "end")
        save_input_history(prompt)
        text_input.see('end')
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response = frcb.chat(prompt)
        # 这个保存的结果需要做一个切片
        #处理信息返回
        output_content = response
        pattern = re.compile(r"```python([\s\S]*?)```")
        matches = pattern.findall(output_content)

        # 将匹配到的内容保存到 txt 文件中
        with open('test.py', 'w',encoding='utf-8') as f:
            for match in matches:
                f.write(f"\n{match}\n\n")
        try:
            from test import main
            main()
            print('运行成功')
        except Exception as e:
            print('所有的错误，我都在这里处理掉%s' % e)
            # 按照错误类型重新修改,并重新提交问题
            error_question_prompt=str(e)
            response=frcb.chat(prompt+error_question_prompt)
            output_content = response
            pattern = re.compile(r"```python([\s\S]*?)```")
            matches = pattern.findall(output_content)
            with open('test.py', 'w', encoding='utf-8') as f:
                for match in matches:
                    f.write(f"\n{match}\n\n")
        print('time_step', time_step)
        time_step+=1
        text_output.configure(state="normal")
        text_output.insert("end", f"\n-----{now}-----\n{output_content}\n")
        text_output.configure(state="disabled")
        text_output.see('end')
        return output_content



### 定义发送消息函数
def send_message(event):
    output_content=process_message()
    print('output-content:',output_content)

### 绑定Ctrl+s事件，发送消息
root.bind("<Control-Key-s>", send_message)

## 开始事件循环
root.mainloop()