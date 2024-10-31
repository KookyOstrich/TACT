import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import tiktoken
import tiktoken_ext
import pandas as pd
import os

# 定数定義
BACKGROUND_COLOR = '#2b2d42'
TEXT_COLOR = '#edf2f4'
BUTTON_COLOR = '#8d99ae'
FONT_NAME = "Arial"

# デフォルトのモデルCSVデータ
DEFAULT_MODELS = [
    {"model_name": "GPT-3.5-turbo", "encoding_name": "cl100k_base"},
    {"model_name": "GPT-4", "encoding_name": "cl100k_base"},
]

class TokenCounterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TACT")
        self.root.geometry("500x300")
        self.root.configure(bg=BACKGROUND_COLOR)

        # モデルデータの初期化
        self.models_df = pd.DataFrame(DEFAULT_MODELS)
        self.model_names = self.models_df['model_name'].tolist()

        # メニューバーの追加
        self.create_menu()

        # GUIコンポーネントの作成
        self.create_widgets()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

    def create_widgets(self):
        # フレームの作成
        main_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # タイトルラベル
        title_label = tk.Label(main_frame, text="TACT", font=(FONT_NAME, 16), fg=TEXT_COLOR, bg=BACKGROUND_COLOR)
        title_label.pack(pady=5)

        # テキスト入力ボックス
        self.input_text = tk.Text(main_frame, height=8, width=50, bg='#edf2f4', fg=BACKGROUND_COLOR, font=(FONT_NAME, 10))
        self.input_text.pack(pady=5)

        # モデル選択とロードボタンのフレーム
        model_frame = tk.Frame(main_frame, bg=BACKGROUND_COLOR)
        model_frame.pack(fill=tk.X, pady=5)

        # モデル選択ドロップダウン
        self.model_choice = ttk.Combobox(model_frame, state="readonly", values=self.model_names, width=30)
        self.model_choice.pack(side=tk.LEFT, padx=(0, 5))
        self.model_choice.set(self.model_names[0] if self.model_names else "Select a model")

        # モデルCSVをロードするボタン
        load_csv_button = tk.Button(model_frame, text="Load Models CSV", command=self.load_file, bg=BUTTON_COLOR, fg=BACKGROUND_COLOR, font=(FONT_NAME, 10))
        load_csv_button.pack(side=tk.LEFT)

        # ボタンフレーム
        button_frame = tk.Frame(main_frame, bg=BACKGROUND_COLOR)
        button_frame.pack(pady=5)

        # トークンカウントボタン
        count_button = tk.Button(button_frame, text="Count Tokens", command=self.count_tokens, bg=BUTTON_COLOR, fg=BACKGROUND_COLOR, font=(FONT_NAME, 10))
        count_button.pack(side=tk.LEFT, padx=2)

        # トークン数をコピーするボタン
        copy_button = tk.Button(button_frame, text="Copy Count", command=self.copy_token_count, bg=BUTTON_COLOR, fg=BACKGROUND_COLOR, font=(FONT_NAME, 10))
        copy_button.pack(side=tk.LEFT, padx=2)

        # トークンカウント結果を保存するボタン
        save_button = tk.Button(button_frame, text="Save Count", command=self.save_token_count, bg=BUTTON_COLOR, fg=BACKGROUND_COLOR, font=(FONT_NAME, 10))
        save_button.pack(side=tk.LEFT, padx=2)

        # トークン数表示ラベル
        self.token_count_label = tk.Label(main_frame, text="Token Count: 0", font=(FONT_NAME, 12), fg=TEXT_COLOR, bg=BACKGROUND_COLOR)
        self.token_count_label.pack(pady=5)

    def load_models_from_csv(self, filepath):
        try:
            models_df = pd.read_csv(filepath, skipinitialspace=True)
            if 'model_name' not in models_df.columns or 'encoding_name' not in models_df.columns:
                raise ValueError("CSVファイルには'model_name'と'encoding_name'の列が必要です。")
            
            # エンコーディング名の有効性をチェック
            for _, row in models_df.iterrows():
                try:
                    tiktoken.get_encoding(row['encoding_name'])
                except KeyError:
                    messagebox.showwarning("Warning", f"無効なエンコーディング名: {row['encoding_name']}")

            self.models_df = models_df.dropna(subset=['model_name', 'encoding_name'])
            self.model_names = self.models_df['model_name'].tolist()
            self.model_choice['values'] = self.model_names
            self.model_choice.set(self.model_names[0] if self.model_names else "Select a model")
            messagebox.showinfo("Success", "モデルCSVを正常にロードしました。")
        except Exception as e:
            messagebox.showerror("Error", f"モデルのロードに失敗しました: {e}")

    def load_file(self):
        file_path = filedialog.askopenfilename(title="Select Model CSV", filetypes=(("CSV Files", "*.csv"),))
        if file_path:
            self.load_models_from_csv(file_path)

    def count_tokens(self):
        text = self.input_text.get("1.0", tk.END).strip()
        selected_model = self.model_choice.get()

        if not text:
            messagebox.showwarning("Warning", "テキストを入力してください。")
            return
        if not selected_model or selected_model not in self.model_names:
            messagebox.showwarning("Warning", "有効なモデルを選択してください。")
            return

        try:
            # まず、モデル名でエンコーディングを取得しようとする
            try:
                enc = tiktoken.encoding_for_model(selected_model)
            except KeyError:
                # モデル名での取得に失敗した場合、エンコーディング名を使用
                encoding_name = self.models_df[self.models_df['model_name'] == selected_model]['encoding_name'].values[0]
                enc = tiktoken.get_encoding(encoding_name)
            
            tokens = enc.encode(text)
            token_count = len(tokens)
            self.token_count_label.config(text=f"Token Count: {token_count}")
        except Exception as e:
            messagebox.showerror("Error", f"トークンのカウント中にエラーが発生しました: {str(e)}")

    def copy_token_count(self):
        count_text = self.token_count_label.cget("text").replace("Token Count: ", "")
        self.root.clipboard_clear()
        self.root.clipboard_append(count_text)
        messagebox.showinfo("Copied", f"トークン数 {count_text} をクリップボードにコピーしました。")

    def save_token_count(self):
        count_text = self.token_count_label.cget("text").replace("Token Count: ", "")
        if count_text == "0":
            messagebox.showwarning("Warning", "保存するトークン数がありません。")
            return
        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.csv")])
        if save_path:
            try:
                with open(save_path, 'w') as file:
                    file.write(f"Token Count: {count_text}\n")
                messagebox.showinfo("Saved", f"トークン数 {count_text} を {save_path} に保存しました。")
            except Exception as e:
                messagebox.showerror("Error", f"保存中にエラーが発生しました: {e}")

    def show_about(self):
        about_window = tk.Toplevel(self.root)    
        about_window.title("About PRISM")    
        about_window.geometry("400x300")    
    
        style = ttk.Style()    
        style.configure("TLabel", font=("Helvetica", 10))    
        style.configure("TitleLabel.TLabel", font=("Helvetica", 16, "bold"))    
    
        frame = ttk.Frame(about_window, padding="20")    
        frame.pack(fill=tk.BOTH, expand=True)    
    
        ttk.Label(frame, text="TACT", style="TitleLabel.TLabel").pack(pady=(0, 10))    
        ttk.Label(frame, text="Version 1.0 β", style="TLabel").pack()    
    
        description = (    
            "TACT (タクト)\n"
            "- Token Analysis and Counting Tool\n"
            "- TACT enables you to consider token strategies before submit your prompt\n"    
        )    
        ttk.Label(frame, text=description, style="TLabel", justify=tk.CENTER).pack(pady=(20, 10))    
    
        ttk.Label(frame, text="© 2024 KookyOstrich", style="TLabel").pack()    
        ttk.Label(frame, text="Licensed under the MIT License", style="TLabel").pack()    

if __name__ == "__main__":
    root = tk.Tk()
    app = TokenCounterApp(root)
    root.mainloop()
