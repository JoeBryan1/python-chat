import tkinter as tk
import asyncio
from client import AsynchronousClient

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"
CHAT_COLOR = "#000000"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"


def ip_character_limit(entry_text):
    if len(entry_text.get()) > 0:
        entry_text.set(entry_text.get()[:3])


def uname_character_limit(entry_text):
    if len(entry_text.get()) > 0:
        entry_text.set(entry_text.get()[:12])


def create_label(frame, label_text, label_column, label_row, label_width, pad_x=0, pad_y=10):
    label = tk.Label(frame, bg=BG_COLOR, fg=TEXT_COLOR,
                     text=label_text, font=FONT_BOLD,
                     width=label_width)
    label.grid(column=label_column, row=label_row, pady=pad_y,
               padx=pad_x)
    return label


def create_entry(entry_label, entry_func, entry_width, validation, entry_text):
    entry = tk.Entry(entry_label, bg="#2C3E50", fg=TEXT_COLOR, font=FONT,
                     width=entry_width, validate=validation, textvariable=entry_text)
    entry.grid()
    entry.bind("<Return>", entry_func)
    return entry


class ChatApplication:

    def __init__(self):
        super().__init__()

        self.interval = 1 / 120

        self.window = tk.Tk()
        self.window.title("Joe's Chat Room")
        self.login_widgets = []
        self.main_widgets = []
        self.setup_login()

        self.is_typing_msg = 'TYPING'
        self.not_typing_msg = 'NOT TYPING'
        self.typing = asyncio.Event()
        self.typing_users = []
        self.empty_entry = asyncio.Event()

        self.loop = asyncio.get_event_loop()
        self.ac = AsynchronousClient()
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
        username_label = create_label(frame=self.window, label_text="Username", label_column=0,
                                      label_row=0, label_width=10)
        self.login_widgets.append(username_label)

        # username entry label
        uname_entry_label = create_label(frame=self.window, label_text=None, label_column=1,
                                         label_row=0, label_width=10)
        self.login_widgets.append(uname_entry_label)

        # username entry
        uname_text = tk.StringVar()
        self.username_entry = create_entry(entry_label=uname_entry_label, entry_func=self.on_username_enter,
                                           entry_width=15, validation='none', entry_text=uname_text)
        self.login_widgets.append(self.username_entry)

        uname_text.trace("w", lambda *args: uname_character_limit(uname_text))

        # ip label
        ip_label = create_label(frame=self.window, label_text="IP:", label_column=0,
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

        ip_text_1.trace("w", lambda *args: ip_character_limit(ip_text_1))
        ip_text_2.trace("w", lambda *args: ip_character_limit(ip_text_2))
        ip_text_3.trace("w", lambda *args: ip_character_limit(ip_text_3))
        ip_text_4.trace("w", lambda *args: ip_character_limit(ip_text_4))

        frame.grid(column=1, row=1,
                   padx=10)

    def setup_main_window(self):
        self.window.configure(background=BG_COLOR)
        self.window.resizable(False, False)

        # head label
        head_label = create_label(frame=self.window, label_text='Welcome',
                                  label_column=0, label_row=0, label_width=50,
                                  pad_x=5, pad_y=10)
        self.main_widgets.append(head_label)

        # users label
        users_label = create_label(frame=self.window, label_text='Users',
                                   label_column=1, label_row=0, label_width=15,
                                   pad_x=0, pad_y=10)
        self.main_widgets.append(users_label)

        # users widget
        self.users_widget = tk.Text(self.window, width=15, height=20, bg=BG_COLOR, fg=TEXT_COLOR,
                                    font=FONT)
        self.users_widget.grid(column=1, row=1)
        self.users_widget.configure(cursor="arrow", state=tk.DISABLED)

        # text widget

        self.text_frame = tk.Frame(self.window)
        self.text_frame.grid(column=0, row=1)

        self.text_widget = tk.Text(self.text_frame, width=45, height=20, bg=BG_GRAY, fg=CHAT_COLOR,
                                   font=FONT)
        self.text_widget.grid(column=0, row=0)
        self.text_widget.configure(cursor="arrow", state=tk.DISABLED)

        self.typing_widget = tk.Label(self.text_frame, width=45, height=1, bg=BG_GRAY,
                                      fg=CHAT_COLOR, font=FONT, anchor=tk.W)
        self.typing_widget.grid(column=0, row=1)
        self.typing_widget.configure(state=tk.DISABLED)

        # scroll bar
        # scrollbar = tk.Scrollbar(self.text_widget)
        # scrollbar.grid(column=1, row=0, rowspan=2)
        # scrollbar.configure(command=self.text_widget.yview)

        # bottom label
        bottom_label = tk.Label(self.window, bg=BG_GRAY)
        bottom_label.grid(column=0, row=2, padx=5, pady=5)

        # message entry box
        msg = tk.StringVar()
        self.msg_entry = tk.Entry(bottom_label, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, width=30,
                                  textvariable=msg)
        self.msg_entry.grid(column=0, row=0)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self.on_msg_enter)

        msg.trace("w", lambda *args: self.is_typing(msg))

        # send button
        send_button = tk.Button(bottom_label, text="Send", font=FONT_BOLD, width=5, bg=BG_GRAY, command=self.
                                send_message)
        send_button.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)

    # Create Widgets
    def create_ip_labels(self, frame, column, entry_text):

        # ip entry label
        ip_entry_label = create_label(frame, None, column, 0, 3)
        self.login_widgets.append(ip_entry_label)

        # ip entry box
        ip_entry = create_entry(entry_label=ip_entry_label,
                                entry_func=self.on_ip_enter,
                                entry_width=3, validation='key',
                                entry_text=entry_text)
        self.login_widgets.append(ip_entry)

        column += 1

        if column != 7:
            # ip period label
            period_label = create_label(frame, ".", column, 0, 1)
            self.login_widgets.append(period_label)

        return ip_entry

    def is_typing(self, msg):
        if msg.get() == '':
            self.empty_entry.set()
        else:
            self.typing.set()
            self.empty_entry.clear()

    # CLIENT HANDLING
    def on_msg_enter(self, event):
        msg = self.msg_entry.get()
        if msg != '':
            self.tasks.append(self.loop.create_task(self.ac.send_message(self.username, msg)))
            self.msg_entry.delete(0, tk.END)

    def on_username_enter(self, event):
        self.handle_connection()

    def on_ip_enter(self, event):
        self.handle_connection()

    async def typing_handling(self):
        is_typing = False
        while True:
            await self.typing.wait()
            if not is_typing:
                is_typing = True
                await self.typing.wait()

                task = self.loop.create_task(self.ac.send_message(self.username, self.is_typing_msg))
                self.tasks.append(task)

            elif is_typing:
                await self.empty_entry.wait()
                self.typing.clear()
                task = self.loop.create_task(self.ac.send_message(self.username, self.not_typing_msg))
                self.tasks.append(task)
                is_typing = False

    def handle_connection(self):
        self.username = self.username_entry.get()
        ip_1 = self.ip_entry_1.get()
        ip_2 = self.ip_entry_2.get()
        ip_3 = self.ip_entry_3.get()
        ip_4 = self.ip_entry_4.get()

        self.ip = (ip_1 + '.' + ip_2 + '.' + ip_3 + '.' + ip_4)

        if self.username != "":
            self.tasks.append(self.loop.create_task(self.handle_client()))
            self.close_login()

    async def handle_client(self):
        task = self.loop.create_task(self.ac.handle_connection(self.username, self.ip))
        self.tasks.append(task)
        await task
        self.tasks.append(self.loop.create_task(self.receive_message()))
        self.tasks.append(self.loop.create_task(self.typing_handling()))

    def send_message(self):
        msg = self.msg_entry.get()
        if msg != '':
            self.tasks.append(self.loop.create_task(self.ac.send_message(self.username, msg)))
            self.msg_entry.delete(0, tk.END)

    async def receive_message(self):
        users = []
        while True:
            self.fut = self.loop.create_future()
            loopTask = self.loop.create_task(self.ac.receive_message(self.fut))
            self.tasks.append(loopTask)
            data_list = await self.fut

            client_id = data_list[0]
            message = data_list[1]
            username = data_list[2]

            if message == 'USER':
                user = (client_id, username)

                if user not in users:
                    users.append(user)
                    await asyncio.sleep(self.interval)

                    self.users_widget.configure(state=tk.NORMAL)
                    self.users_widget.insert(tk.INSERT, user[1] + "\n")
                    self.users_widget.configure(state=tk.DISABLED)

            elif message == 'TYPING':
                if str(username) not in self.typing_users:
                    self.typing_users.append(str(username))
                    self.update_is_typing(username)

            elif message == 'NOT TYPING':
                if str(username) in self.typing_users:
                    self.typing_users.remove(str(username))
                    self.update_is_typing(username)

            else:
                msg = f"{username}: {message}\n"

                self.text_widget.configure(state=tk.NORMAL)
                self.text_widget.insert(tk.INSERT, msg)
                self.text_widget.configure(state=tk.DISABLED)

    def update_is_typing(self, username):
        typing_msg = ''

        length = len(self.typing_users)

        print(length)

        if length > 0:
            if length == 2:
                typing_msg = self.typing_users[0] + ' and ' + self.typing_users[1] + ' are typing!'
            elif length > 1:
                counter = 1
                for username in self.typing_users:
                    if length == counter:
                        typing_msg = typing_msg + 'and ' + username
                    else:
                        typing_msg = typing_msg + username + ', '
                        counter = counter + 1
                typing_msg = typing_msg + ' are typing!'
            else:
                typing_msg = username + ' is typing!'

            self.typing_widget.config(text=typing_msg)

        else:
            self.typing_widget.config(text='')

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
