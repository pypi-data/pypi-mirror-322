import os
import sys
import subprocess
from tkinter import GROOVE, Tk, Button, Label, filedialog, messagebox
from tkinter.ttk import Progressbar

def main():
    def convert_py_to_pyx(py_file):
        """将 .py 文件转换为 .pyx 文件。"""
        pyx_file = py_file[:-3] + '.pyx'
        with open(py_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        with open(pyx_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return pyx_file

    def create_setup_file(pyx_file):
        """创建 setup.py 文件以编译 .pyx 文件。"""
        setup_file = "setup.py"
        content = f"""
    from setuptools import setup, Extension
    from Cython.Build import cythonize

    setup(
        name='{os.path.splitext(os.path.basename(pyx_file))[0]}',
        ext_modules=cythonize(Extension(
            name='{os.path.splitext(os.path.basename(pyx_file))[0]}',
            sources=['{pyx_file}'],
        )),
        zip_safe=False,
    )
    """
        with open(setup_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return setup_file

    def compile_pyx_to_pyd(setup_file, pyx_file):
        """编译 .pyx 文件为 .pyd 文件，并实时输出进度。"""
        progress['value'] = 0  # 重设进度条

        # 启动子进程
        process = subprocess.Popen(
            [sys.executable, setup_file, "build_ext", "--inplace"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,  # 行缓冲
            universal_newlines=True
        )
        
        def update_progress():
            output = process.stdout.readline()
            
            if output:
                # 进度条假设每行输出增加一定比例，这里简单映射为增加10%（可根据实际情况修改）
                if progress['value'] < 90:  # 根据实际行数确定进度
                    progress['value'] += 10  
                progress.update_idletasks()  # 更新进度条
            
            # 检查进程是否仍在运行
            if process.poll() is None:  # 进程仍在运行
                root.after(100, update_progress)  # 每100毫秒调用一次
            else:  # 进程完成
                process.wait()
                if process.returncode == 0:
                    messagebox.showinfo("成功", "成功生成 .pyd 文件！")
                    clean_up(setup_file, pyx_file)  # 清理文件
                else:
                    error_output = process.stderr.read()
                    messagebox.showerror("编译错误", f"编译失败: {error_output}")

                progress['value'] = 100  # 设置进度条为 100%

        # 启动输出读取
        update_progress()

    def clean_up(setup_file, pyx_file):
        """删除 .pyx、setup.py 以及生成的 .c 文件。"""
        try:
            if os.path.exists(setup_file):
                os.remove(setup_file)
            if os.path.exists(pyx_file):
                os.remove(pyx_file)

            # 确保对应的 .c 文件被删除
            c_file = pyx_file[:-4] + '.c'
            if os.path.exists(c_file):
                os.remove(c_file)  # 删除 .c 文件
        except Exception as e:
            messagebox.showwarning("清理错误", f"清理文件时出错: {str(e)}")

    def process_file():
        """处理选择的 Python 文件。"""
        py_file = filedialog.askopenfilename(title="选择 Python (.py) 文件", filetypes=[("Python 文件", "*.py")])
        
        if not py_file:
            return

        try:
            # 转换 .py 为 .pyx
            pyx_file = convert_py_to_pyx(py_file)
            # 创建 setup.py 文件
            setup_file = create_setup_file(pyx_file)
            # 编译 .pyx 为 .pyd
            compile_pyx_to_pyd(setup_file, pyx_file)
        except Exception as e:
            messagebox.showerror("错误", str(e))

    # 创建主 GUI 窗口
    root = Tk()
    root.title("Py To Pyd")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - 500) // 2
    y = (screen_height - 500) // 2

    root.geometry(f"400x250+{x}+{y}")
    root.wm_iconbitmap('PyToPyd.ico')

    # 创建和放置控件
    label = Label(root, text="选择要转换和编译的 Py 文件：",font=('黑体',15))
    label.pack(pady=20)

    process_button = Button(root, text="选择文件", command=process_file, bg='yellow', relief=GROOVE, width=15)
    process_button.pack(pady=10)

    label = Label(root, text="进度:",font=('黑体',12))
    label.place(x=45,y=140)

    # 创建进度条
    progress = Progressbar(root, orient='horizontal', length=300, mode='determinate')
    progress.pack(pady=60)

    # 启动 GUI 事件循环
    root.mainloop()

if __name__ == '__main__':
    main()