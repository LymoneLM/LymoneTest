import tkinter as tk
from tkinter import messagebox
import random
import time
from PIL import ImageTk, Image

assets_path = "./assets"
name = "点击挑战小游戏"
copy_right = "某某某_学号xxx制作"


class ClickSpeedGame:
    def __init__(self, root):
        # 初始化
        self.root = root
        self.root.title(f"{name} {copy_right}")
        self.root.iconbitmap(f"{assets_path}/icon.ico")

        # 游戏常量
        self.GRID_SIZE = 10
        self.TARGET_COUNT = 10
        self.CELL_SIZE = 50

        # 状态变量
        self.remaining = self.TARGET_COUNT
        self.started = False
        self.start_time = 0
        self.records = []
        self.target_positions = []

        # 加载图片
        try:
            self.bg_img = ImageTk.PhotoImage(
                Image.open(f"{assets_path}/bg.png").resize((self.CELL_SIZE, self.CELL_SIZE)))
            self.active_img = ImageTk.PhotoImage(
                Image.open(f"{assets_path}/active.png").resize((self.CELL_SIZE, self.CELL_SIZE)))
            self.clicked_img = ImageTk.PhotoImage(
                Image.open(f"{assets_path}/clicked.png").resize((self.CELL_SIZE, self.CELL_SIZE)))
        except Exception as e:
            messagebox.showerror("错误", f"图片加载失败: {str(e)}")
            root.destroy()
            return

        # 创建界面
        self.create_widgets()
        self.new_game()

    def create_widgets(self):
        # 左侧游戏区域
        self.game_frame = tk.Frame(self.root)
        self.game_frame.grid(row=0, column=0, padx=10, pady=10)

        # 创建网格
        self.cells = []
        for i in range(self.GRID_SIZE):
            row = []
            for j in range(self.GRID_SIZE):
                label = tk.Label(self.game_frame, image=self.bg_img,
                                 borderwidth=1, relief="solid")
                label.grid(row=i, column=j)
                label.bind("<Button-1>", lambda e, x=i, y=j: self.click_handler(x, y))
                row.append(label)
            self.cells.append(row)

        # 右侧信息面板
        self.info_frame = tk.Frame(self.root)
        self.info_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        # 当前时间显示
        self.time_var = tk.StringVar()
        tk.Label(self.info_frame, text="当前用时:", font=("微软雅黑", 14)).pack(pady=5)
        self.time_label = tk.Label(self.info_frame, textvariable=self.time_var,
                                   font=("微软雅黑", 18), fg="blue")
        self.time_label.pack()

        # 排行榜
        tk.Label(self.info_frame, text="排行榜", font=("微软雅黑", 16)).pack(pady=10)
        self.record_listbox = tk.Listbox(self.info_frame, width=20, height=10,
                                         font=("微软雅黑", 12))
        self.record_listbox.pack()

        # 新游戏按钮
        tk.Button(self.info_frame, text="新游戏", command=self.new_game,
                  font=("微软雅黑", 14)).pack(pady=20)

    def new_game(self):
        # 重置游戏状态
        self.remaining = self.TARGET_COUNT
        self.started = False
        self.time_var.set("0.000 秒")
        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE):
                self.cells[i][j].config(image=self.bg_img)

        # 生成新的目标位置
        self.target_positions = random.sample(
            [(i, j) for i in range(self.GRID_SIZE) for j in range(self.GRID_SIZE)],
            self.TARGET_COUNT
        )
        for x, y in self.target_positions:
            self.cells[x][y].config(image=self.active_img)

    def click_handler(self, x, y):
        if (x, y) not in self.target_positions:
            return

        if not self.started:
            self.start_time = time.time()
            self.started = True
            self.update_timer()

        self.cells[x][y].config(image=self.clicked_img)
        self.target_positions.remove((x, y))
        self.remaining -= 1

        if self.remaining == 0:
            elapsed = time.time() - self.start_time
            self.time_var.set(f"{elapsed:.3f} 秒")
            self.update_records(elapsed)
            messagebox.showinfo("完成！", f"用时：{elapsed:.3f} 秒")

    def update_timer(self):
        if self.started and self.remaining > 0:
            elapsed = time.time() - self.start_time
            self.time_var.set(f"{elapsed:.3f} 秒")
            self.root.after(50, self.update_timer)

    def update_records(self, new_time):
        self.records.append(new_time)
        self.records.sort()
        self.record_listbox.delete(0, tk.END)
        for i, t in enumerate(self.records[:10]):
            self.record_listbox.insert(tk.END, f"{i + 1}. {t:.3f} 秒")


if __name__ == "__main__":
    root = tk.Tk()
    game = ClickSpeedGame(root)
    root.mainloop()
