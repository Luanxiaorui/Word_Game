import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Tuple
from core import WordGame

class WordGameUI:
    """英语单词猜词游戏界面"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("英语单词趣味猜词游戏")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # 游戏核心逻辑
        self.game = WordGame()
        
        # 界面变量
        self.selected_library = tk.StringVar()
        self.selected_length = tk.IntVar()
        self.guess_var = tk.StringVar()
        self.guess_entries = []  # 新增：用于存储每个字母的Entry
        
        # 创建界面
        self.create_widgets()
        
        # 加载词库
        self.load_libraries()
        
    def create_widgets(self):
        """创建界面组件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="英语单词趣味猜词游戏", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # 词库选择区域
        self.create_library_section(main_frame)
        
        # 游戏设置区域
        self.create_game_setup_section(main_frame)
        
        # 游戏区域
        self.create_game_section(main_frame)
        
        # 状态栏
        self.create_status_bar(main_frame)
        
    def create_library_section(self, parent):
        """创建词库选择区域"""
        # 词库选择框架
        library_frame = ttk.LabelFrame(parent, text="词库选择", padding="10")
        library_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        library_frame.columnconfigure(1, weight=1)
        
        # 词库标签
        ttk.Label(library_frame, text="选择词库:").grid(row=0, column=0, sticky=tk.W)
        
        # 词库下拉框
        self.library_combo = ttk.Combobox(library_frame, textvariable=self.selected_library, 
                                         state="readonly", width=30)
        self.library_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        self.library_combo.bind("<<ComboboxSelected>>", self.on_library_selected)
        
        # 词库信息标签
        self.library_info_label = ttk.Label(library_frame, text="请选择词库")
        self.library_info_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
        
    def create_game_setup_section(self, parent):
        """创建游戏设置区域"""
        # 游戏设置框架
        setup_frame = ttk.LabelFrame(parent, text="游戏设置", padding="10")
        setup_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        setup_frame.columnconfigure(1, weight=1)
        
        # 单词长度选择
        ttk.Label(setup_frame, text="单词长度:").grid(row=0, column=0, sticky=tk.W)
        
        self.length_combo = ttk.Combobox(setup_frame, textvariable=self.selected_length, 
                                        state="readonly", width=10)
        self.length_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # 开始游戏按钮
        self.start_button = ttk.Button(setup_frame, text="开始新游戏", 
                                      command=self.start_new_game)
        self.start_button.grid(row=0, column=2, padx=(20, 0))
        
        # 游戏信息标签
        self.game_info_label = ttk.Label(setup_frame, text="请选择单词长度并开始游戏")
        self.game_info_label.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(5, 0))
        
    def create_game_section(self, parent):
        """创建游戏区域"""
        # 游戏框架
        game_frame = ttk.LabelFrame(parent, text="猜词游戏", padding="10")
        game_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        game_frame.columnconfigure(0, weight=1)
        game_frame.rowconfigure(1, weight=1)
        parent.rowconfigure(3, weight=1)
        
        # 输入区域
        input_frame = ttk.Frame(game_frame)
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        ttk.Label(input_frame, text="输入单词:").grid(row=0, column=0, sticky=tk.W)
        
        self.guess_input_frame = ttk.Frame(input_frame)
        self.guess_input_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 10))
        
        self.guess_button = ttk.Button(input_frame, text="猜测", command=self.make_guess)
        self.guess_button.grid(row=0, column=2)
        
        # 游戏表格
        self.create_game_table(game_frame)
        
    def create_game_table(self, parent):
        """创建游戏表格（Canvas+滚动条）"""
        self.canvas_frame = ttk.Frame(parent)
        self.canvas_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.v_scroll = ttk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.v_scroll.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.current_word_length = 0
        self.current_max_attempts = 0
        # 绑定鼠标滚轮事件
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)  # Windows/macOS
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)    # Linux
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)    # Linux

    def _on_mousewheel(self, event):
        # Windows/macOS
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")
        
    def create_status_bar(self, parent):
        """创建状态栏"""
        self.status_label = ttk.Label(parent, text="就绪", relief=tk.SUNKEN)
        self.status_label.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
    def load_libraries(self):
        """加载词库"""
        libraries = self.game.load_word_libraries()
        if libraries:
            library_names = list(libraries.keys())
            self.library_combo['values'] = library_names
            if library_names:
                self.library_combo.set(library_names[0])
                self.on_library_selected()
        else:
            messagebox.showerror("错误", "未找到词库文件！请确保wordlib目录存在且包含.txt文件。")
            
    def on_library_selected(self, event=None):
        """词库选择事件"""
        library_name = self.selected_library.get()
        if library_name and self.game.select_library(library_name):
            # 更新词库信息
            info = self.game.get_library_info()
            self.library_info_label.config(
                text=f"词库: {info['name']} | 总单词数: {info['total_words']}"
            )
            
            # 更新可用长度
            lengths = self.game.get_available_lengths()
            self.length_combo['values'] = lengths
            if lengths:
                self.length_combo.set(lengths[0])
                []
            self.status_label.config(text=f"已选择词库: {library_name}")
        else:
            self.library_info_label.config(text="词库选择失败")
            
    def start_new_game(self):
        """开始新游戏"""
        if not self.selected_library.get():
            messagebox.showwarning("警告", "请先选择词库！")
            return
            
        length = self.selected_length.get()
        if not length:
            messagebox.showwarning("警告", "请选择单词长度！")
            return
            
        if self.game.start_new_game(length):
            # 更新游戏信息
            status = self.game.get_game_status()
            self.game_info_label.config(
                text=f"游戏开始！单词长度: {length} | 最大尝试次数: {status['max_attempts']}"
            )
            
            # 清空表格
            self.clear_game_table()
            
            # 设置表格列
            self.setup_game_table(length)
            
            # 清空输入
            self.guess_var.set("")
            # 新增：重建输入格子
            self.build_guess_entries(length)
            
            self.status_label.config(text="游戏已开始，请输入单词进行猜测")
        else:
            messagebox.showerror("错误", f"无法开始游戏！词库中没有长度为{length}的单词。")
            
    def setup_game_table(self, word_length):
        """设置游戏表格（Canvas模式下只需记录参数并重绘）"""
        status = self.game.get_game_status()
        self.current_word_length = word_length
        self.current_max_attempts = status['max_attempts']
        self.draw_game_canvas()
        
    def clear_game_table(self):
        """清空游戏表格（Canvas模式下清空画布）"""
        if hasattr(self, 'canvas'):
            self.canvas.delete("all")
            
    def update_game_table(self, feedback):
        """Canvas模式下直接重绘，不再单独更新一行"""
        self.draw_game_canvas()
        
    def draw_game_canvas(self):
        """根据已猜测内容绘制Canvas，支持自适应和滚动"""
        if not hasattr(self, 'canvas'):
            return
        self.canvas.delete("all")
        status = self.game.get_game_status()
        word_length = status.get('word_length', self.current_word_length)
        max_attempts = status.get('max_attempts', self.current_max_attempts)
        cell_size = 48
        padding = 12
        y_offset = 20
        font = ("Arial", 20, "bold")

        # 动态计算宽高
        total_width = word_length * cell_size + (word_length - 1) * padding + 80
        total_height = max_attempts * cell_size + (max_attempts - 1) * padding + 2 * y_offset
        self.canvas.config(width=min(total_width, 700), height=min(total_height, 400))
        self.canvas.config(scrollregion=(0, 0, total_width, total_height))

        # 居中起始x
        canvas_width = int(self.canvas.cget('width'))
        x_start = max((canvas_width - (word_length * cell_size + (word_length - 1) * padding)) // 2, 20)

        for row in range(max_attempts):
            if row < len(status['attempts']):
                word = status['attempts'][row]
                feedback = self.game._generate_feedback(word)
            else:
                feedback = [("", "white")] * word_length
            for col, (letter, color) in enumerate(feedback):
                x0 = x_start + col * (cell_size + padding)
                y0 = y_offset + row * (cell_size + padding)
                x1 = x0 + cell_size
                y1 = y0 + cell_size
                fill = {'green': '#90EE90', 'yellow': '#FFFF99', 'red': '#FFB6C1', 'white': '#FFFFFF'}.get(color, '#FFFFFF')
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill, outline="black", width=2)
                if letter:
                    self.canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2, text=letter.upper(), font=font)
            
    def build_guess_entries(self, word_length):
        # 清空旧的 Entry
        for entry in getattr(self, 'guess_entries', []):
            entry.destroy()
        self.guess_entries = []
        # 新建 Entry
        for i in range(word_length):
            entry = ttk.Entry(self.guess_input_frame, width=2, font=("Arial", 18), justify='center')
            entry.grid(row=0, column=i, padx=2)
            entry.bind("<KeyRelease>", lambda e, idx=i: self.on_entry_key(e, idx))
            self.guess_entries.append(entry)
        if self.guess_entries:
            self.guess_entries[0].focus()
    def on_entry_key(self, event, idx):
        entry = self.guess_entries[idx]
        value = entry.get()
        # 只允许一个字母
        if len(value) > 1:
            entry.delete(1, tk.END)
        # 自动跳到下一个
        if value and idx + 1 < len(self.guess_entries):
            self.guess_entries[idx + 1].focus()
        # 回退时跳到前一个
        elif not value and idx > 0 and event.keysym == 'BackSpace':
            self.guess_entries[idx - 1].focus()
            
    def make_guess(self):
        """进行猜测"""
        word = ''.join(entry.get() for entry in self.guess_entries).strip()
        if not word:
            return
        # 检查游戏是否结束
        status = self.game.get_game_status()
        if status['game_over']:
            messagebox.showinfo("游戏结束", "游戏已结束或还未开始，请开始新游戏！")
            return
        # 进行猜测
        feedback = self.game.make_guess(word)
        if feedback is None:
            messagebox.showerror("错误", "无效的单词！请确保单词长度正确且在词库中。")
            return
        # 更新表格显示（Canvas重绘）
        self.update_game_table(feedback)
        # 清空输入
        for entry in self.guess_entries:
            entry.delete(0, tk.END)
        if self.guess_entries:
            self.guess_entries[0].focus()
        # 检查游戏状态
        status = self.game.get_game_status()
        if status['game_over']:
            if status['won']:
                messagebox.showinfo("恭喜", f"恭喜你赢了！目标单词是: {status['target_word']}")
                self.status_label.config(text="游戏胜利！")
            else:
                messagebox.showinfo("游戏结束", f"游戏结束！目标单词是: {status['target_word']}")
                self.status_label.config(text="游戏失败！")
        else:
            self.status_label.config(
                text=f"剩余尝试次数: {status['remaining_attempts']}"
            )
            
    def run(self):
        """运行界面"""
        self.root.mainloop() 