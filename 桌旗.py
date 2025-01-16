import os
import shutil
from tkinter import Tk, Label, Button, Entry, filedialog, messagebox, Checkbutton, BooleanVar

def select_folder(entry):
    folder = filedialog.askdirectory()
    if folder:
        entry.delete(0, "end")
        entry.insert(0, folder)

def copy_and_rename_files():
    root_path = root_entry.get()
    file_name_keyword = file_name_entry.get()
    output_path = output_entry.get()
    keep_structure = keep_structure_var.get()

    if not os.path.isdir(root_path):
        messagebox.showerror("错误", "请输入有效的根目录路径")
        return

    if not os.path.isdir(output_path):
        messagebox.showerror("错误", "请输入有效的输出目录路径")
        return

    if not file_name_keyword:
        messagebox.showerror("错误", "请输入文件名关键字")
        return

    try:
        for subfolder_name in os.listdir(root_path):
            subfolder_path = os.path.join(root_path, subfolder_name)

            if os.path.isdir(subfolder_path):
                for file_name in os.listdir(subfolder_path):
                    file_base_name = os.path.splitext(file_name)[0]
                    if file_base_name == file_name_keyword:
                        file_path = os.path.join(subfolder_path, file_name)
                        if os.path.isfile(file_path):
                            if keep_structure:
                                subfolder_output_path = os.path.join(output_path, subfolder_name)
                                if not os.path.exists(subfolder_output_path):
                                    os.makedirs(subfolder_output_path)
                                shutil.copy(file_path, subfolder_output_path)
                            else:
                                shutil.copy(file_path, output_path)

                                ext = os.path.splitext(file_name)[-1].lower()
                                new_name = f"{subfolder_name}{ext}"
                                new_path = os.path.join(output_path, new_name)

                                counter = 1
                                while os.path.exists(new_path):
                                    new_name = f"{subfolder_name}_{counter}{ext}"
                                    new_path = os.path.join(output_path, new_name)
                                    counter += 1

                                os.rename(os.path.join(output_path, file_name), new_path)

        messagebox.showinfo("完成", "文件已成功复制并重命名！" if not keep_structure else "文件已成功复制！")
    except Exception as e:
        messagebox.showerror("错误", f"出现问题：{str(e)}")

root = Tk()
root.title("桌旗")
root.geometry("600x450")

Label(root, text="选择根目录路径：").pack(pady=5)
root_entry = Entry(root, width=50)
root_entry.pack(pady=5)
Button(root, text="选择根目录", command=lambda: select_folder(root_entry)).pack(pady=5)

Label(root, text="请输入文件名关键字：").pack(pady=10)
file_name_entry = Entry(root, width=50)
file_name_entry.pack(pady=5)

Label(root, text="选择输出目录路径：").pack(pady=10)
output_entry = Entry(root, width=50)
output_entry.pack(pady=5)
Button(root, text="选择输出目录", command=lambda: select_folder(output_entry)).pack(pady=5)

keep_structure_var = BooleanVar()
keep_structure_var.set(True)
Checkbutton(root, text="保留子文件夹结构", variable=keep_structure_var).pack(pady=10)

Button(root, text="开始复制并重命名", command=copy_and_rename_files).pack(pady=20)

root.mainloop()
