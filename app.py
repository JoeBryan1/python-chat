import tkinter as tk
import asyncio
from client import AsyncronousClient

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"
CHAT_COLOR = "#000000"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"


class ChatApplication:

    def __init__(self):
        super().__init__()

        self.interval = 1/120

        self.window = tk.Tk()
        self.window.title("Joe's Chat Room")
        self.login_widgets = []
        self.setup_login()

        self.loop = asyncio.get_event_loop()

        self.ac = AsyncronousClient()

        self.tasks = []
        self.tasks.append(self.loop.create_task(self.updater(self.interval)))
        self.loop.run_forever()

    async def updater(self, interval):
        while True:
            tk.Tk.update(self.window)
            await asyncio.sleep(interval)

    def setup_login(self):
        self.window.configure(bg=BG_COLOR)
        self.window.resizable(False, False)

        # username label
        username_label = self.create_label(frame=self.window, label_text="Username", label_column=0,
                                           label_row=0, label_width=10)
        self.login_widgets.append(username_label)

        # username entry label
        uname_entry_label = self.create_label(frame=self.window, label_text=None, label_column=1,
                                              label_row=0, label_width=10)
        self.login_widgets.append(uname_entry_label)

        # username entry
        uname_text = tk.StringVar()
        self.username_entry = self.create_entry(entry_label=uname_entry_label, entry_func=self.on_username_enter,
                                                entry_width=15, validation='none', entry_text=uname_text)
        self.login_widgets.append(self.username_entry)

        uname_text.trace("w", lambda *args: self.uname_character_limit(uname_text))

        # ip label
        ip_label = self.create_label(frame=self.window, label_text="IP:", label_column=0,
                                     label_row=1, label_width=3)
        self.login_widgets.append(ip_label)

        frame = tk.Frame(self.window)
        frame.configure(bg=BG_COLOR)

        # ip entry labels

        ip_text_1 = tk.StringVar()
        ip_text_2 = tk.StringVar()
        ip_text_3 = tk.StringVar()
        ip_text_4 = tk.StringVar()

        self.ip_entry_1 = self.create_ip_labels(frame, 0, ip_text_1)
        self.ip_entry_2 = self.create_ip_labels(frame, 2, ip_text_2)
        self.ip_entry_3 = self.create_ip_labels(frame, 4, ip_text_3)
        self.ip_entry_4 = self.create_ip_labels(frame, 6, ip_text_4)

        ip_text_1.trace("w", lambda *args: self.ip_character_limit(ip_text_1))
        ip_text_2.trace("w", lambda *args: self.ip_character_limit(ip_text_2))
        ip_text_3.trace("w", lambda *args: self.ip_character_limit(ip_text_3))
        ip_text_4.trace("w", lambda *args: self.ip_character_limit(ip_text_4))

        frame.grid(column=1, row=1,
                   padx=10)

    def setup_main_window(self):
        self.window.configure(background=BG_COLOR)
        self.window.resizable(False, False)

        # head label
        head_label = tk.Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR,
                              text="Welcome", font=FONT_BOLD,
                              width=50)
        head_label.grid(column=0, row=0, padx=5, pady=10)

        # users label
        users_label = tk.Label(self.window, bg=BG_GRAY, fg=TEXT_COLOR,
                               text="Users", font=FONT_BOLD,
                               width=15)
        users_label.grid(column=1, row=0, pady=10)

        # users widget
        self.users_widget = tk.Text(self.window, width=15, height=20, bg=BG_COLOR, fg=TEXT_COLOR,
                                    font=FONT)
        self.users_widget.grid(column=1, row=1)
        self.users_widget.configure(cursor="arrow", state=tk.DISABLED)

        # text widget
        self.text_widget = tk.Text(self.window, width=45, height=20, bg=BG_GRAY, fg=CHAT_COLOR,
                                   font=FONT)
        self.text_widget.grid(column=0, row=1)
        self.text_widget.configure(cursor="arrow", state=tk.DISABLED)

        # scroll bar
        scrollbar = tk.Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.967)
        scrollbar.configure(command=self.text_widget.yview)

        # bottom label
        bottom_label = tk.Label(self.window, bg=BG_GRAY)
        bottom_label.grid(column=0, row=2, padx=5, pady=5)

        # message entry box
        self.msg_entry = tk.Entry(bottom_label, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, width=30)
        self.msg_entry.grid(column=0, row=0)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self.on_msg_enter)

        # send button
        send_button = tk.Button(bottom_label, text="Send", font=FONT_BOLD, width=5, bg=BG_GRAY, command=self.
                                send_message)
        send_button.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)

    # Widget Code
    def ip_character_limit(self, entry_text):
        if len(entry_text.get()) > 0:
            entry_text.set(entry_text.get()[:3])

    def uname_character_limit(self, entry_text):
        if len(entry_text.get()) > 0:
            entry_text.set(entry_text.get()[:12])

    # Create Widgets
    def create_ip_labels(self, frame, column, entry_text):

        # ip entry label
        ip_entry_label = self.create_label(frame, None, column, 0, 3)
        self.login_widgets.append(ip_entry_label)

        # ip entry box
        ip_entry = self.create_entry(entry_label=ip_entry_label,
                                          entry_func=self.on_ip_enter,
                                          entry_width=3, validation='key',
                                          entry_text=entry_text)
        self.login_widgets.append(ip_entry)

        column += 1

        if column != 7:
            # ip period label
            period_label = self.create_label(frame, ".", column, 0, 1)
            self.login_widgets.append(period_label)

        return ip_entry

    def create_label(self, frame, label_text, label_column, label_row, label_width):
        label = tk.Label(frame, bg=BG_COLOR, fg=TEXT_COLOR,
                         text=label_text, font=FONT_BOLD, pady=10,
                         width=label_width)
        label.grid(column=label_column, row=label_row)
        return label

    def create_entry(self, entry_label, entry_func, entry_width, validation, entry_text):
        entry = tk.Entry(entry_label, bg="#2C3E50", fg=TEXT_COLOR, font=FONT,
                         width=entry_width, validate=validation, textvariable=entry_text)
        entry.grid()
        entry.bind("<Return>", entry_func)
        return entry

    # CLIENT HANDLING
    def send_message(self):
        msg = self.msg_entry.get()
        self.tasks.append(self.loop.create_task(self.ac.send_message(self.username, msg)))
        self.msg_entry.delete(0, tk.END)

    def on_msg_enter(self, event):
        msg = self.msg_entry.get()
        self.tasks.append(self.loop.create_task(self.ac.send_message(self.username, msg)))
        self.msg_entry.delete(0, tk.END)

    def on_username_enter(self, event):
        self.handle_connection()

    def on_ip_enter(self, event):
        self.handle_connection()

    def handle_connection(self):
        self.username = self.username_entry.get()
        ip_1 = self.ip_entry_1.get()
        ip_2 = self.ip_entry_2.get()
        ip_3 = self.ip_entry_3.get()
        ip_4 = self.ip_entry_4.get()

        self.ip = (ip_1+"."+ip_2+"."+ip_3+"."+ip_4)

        if self.username != "":
            self.tasks.append(self.loop.create_task(self.handle_client()))
            self.close_login()

    async def handle_client(self):
        task = self.loop.create_task(self.ac.handle_connection(self.username, self.ip))
        self.tasks.append(task)
        await task
        self.tasks.append(self.loop.create_task(self.receive_message()))

    async def receive_message(self):
        userlist = []
        while True:
            self.fut = self.loop.create_future()
            loopTask = self.loop.create_task(self.ac.receive_message(self.fut))
            data = await self.fut

            dataList = data.decode().split(',')

            client_id = dataList[0]
            message = dataList[1]
            username = dataList[2]

            if message == 'USER':
                user = (client_id, username)

                if user not in userlist:
                    userlist.append(user)
                    await asyncio.sleep(self.interval)

                    self.users_widget.configure(state=tk.NORMAL)
                    self.users_widget.insert(tk.INSERT, user[1] + "\n")
                    self.users_widget.configure(state=tk.DISABLED)

            else:
                msg = f"{username}: {message}\n"

                self.text_widget.configure(state=tk.NORMAL)
                self.text_widget.insert(tk.INSERT, msg)
                self.text_widget.configure(state=tk.DISABLED)

    # Close Handling
    def close_login(self):
        for widget in self.login_widgets:
            widget.destroy()
        self.setup_main_window()

    def close(self):
        for task in self.tasks:
            task.cancel()
        self.loop.stop()
        tk.Tk.destroy(self.window)


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
if __name__ == "__main__":
    a = ChatApplication()
