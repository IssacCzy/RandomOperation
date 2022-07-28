## RandomOperation
> 小学二年级口语训练
* 1、热身训练
  * 乘法口诀
  * 20以内加减
  * 整十、整百、整千加减训练
* 2、模拟训练
  * 加减混合运算
  * 10以内的连除
  * 100以内的有余数的除法
  * 100以内乘除混合运算
  * 乘加、乘减混合（加减乘混合）
  * 除加、除减混合（加减除混合）
  * 含小括号的（加减）(乘除)混合

    
## 打包过程
* 1、创建 setup.py 将需要加密的 *.py 文件配置进去（通常是除 main.py 之外的所有 py 文件）（防止反编译）；
* 2、readMe.md 同目录（项目根目录）下的所有文件拷贝到 install_exe 文件夹下；
* 3、进入 install_exe 目录；
* 4、执行命令生成加密文件；
`python setup.py build_ext --inplace`
* 5、执行命令删除加密后的多余文件(此步骤可省略)
`python 修改 pyd 文件名 + 删除 c 文件.py`
* 6、执行脚本打包，得到 main.spec 文件：
`python -m eel main.py web --onefile --noconsole --hidden-import=queue -F -w -i favicon.ico`
`(--hidden-import queue 隐式导入需要依赖的 queue 包)`
* 7、修改 main.spec：
```
 hiddenimports：将所有引用的包添加进去
 修改 name 属性(打出来的 exe 的名字)

可以通过比对实现修改： main.spec  main - 对比文件.spec
```
* 8、再执行脚本实现真正打包：dist/*.exe
`pyinstaller main.spec`
* 9、最后
```
a、chromedriver.exe 拷贝到 dist 目录下
b、创建 log 文件夹
c、创建 temp/history.txt
```

## 如果是用 Anaconda Prompt 来打包
* 1、打开 Anaconda Prompt
* 2、激活对应的 python 环境
`(base) C:\Users\Administrator>conda activate python3.7`
* 3、进入项目所在磁盘
`(python3.7) C:\Users\Administrator>D:`
* 4、进入对应项目目录
`(python3.7) D:\Projects\RandomOperation\install_exe>`
* d、剩余的步骤和上面的打包过程完全相同
> ==注意事项==
* 由于 pyinstaller 和 pyechart 不兼容，打包生成 exe 文件后，双击 exe 报错
`FileNotFoundError: [Errno 2] No such file or directory: ‘C:\Users\xxx\AppData\Local\Temp\_MEI944442\pyecharts\datasets\map_filename.json’`
* ==解决方案：==
* a、找到 conda 虚拟环境的安装包路径
`(python3.7) D:\Projects\RandomOperation\install_exe>python -m site`
* 结果如下：
```
sys.path = [
    'D:\\Projects\\RandomOperation\\install_exe',
    'd:\\ProgramData\\Anaconda3\\envs\\python3.7\\python37.zip',
    'd:\\ProgramData\\Anaconda3\\envs\\python3.7\\DLLs',
    'd:\\ProgramData\\Anaconda3\\envs\\python3.7\\lib',
    'd:\\ProgramData\\Anaconda3\\envs\\python3.7',
    'd:\\ProgramData\\Anaconda3\\envs\\python3.7\\lib\\site-packages',  --》目标文件夹
]
```
* b、进入 PyInstaller\hooks\ 文件夹
`D:\ProgramData\Anaconda3\envs\python3.7\Lib\site-packages\PyInstaller\hooks`
* c、创建 hook-pyecharts.py 文件，文件内容如下：
```
 #-----------------------------------------------------------------------------
 # Copyright (c) 2017-2020, PyInstaller Development Team.
 #
 # Distributed under the terms of the GNU General Public License (version 2
 # or later) with exception for distributing the bootloader.
 #
 # The full license is in the file COPYING.txt, distributed with this software.
 #
 # SPDX-License-Identifier: (GPL-2.0-or-later WITH Bootloader-exception)
 #----------------------------------------------------------------------------- 
# Hook for nanite: https://pypi.python.org/pypi/nanite 
from PyInstaller.utils.hooks import collect_data_files 
datas = collect_data_files('pyecharts') 
```
* d、保存文件，删除打包目录下的 xxxxx.spec 文件，重新打包即可！