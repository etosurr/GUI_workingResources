from database import DB
import tkinter as tk
from tkinter import ttk
from abc import ABC


class Mediator(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        toolbar = tk.Frame(bg='#DCDCDC', bd=2, borderwidth=5)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.resource_img = tk.PhotoImage(file='images/resources.png').subsample(10)
        btn_open_dialog = tk.Button(toolbar, text='Добавить', command=self.open_dialog,
                                  bg='#DCDCDC', bd=0, compound=tk.TOP, image=self.resource_img)
        btn_open_dialog.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file='images/edit.png').subsample(10)
        btn_edit_dialog = tk.Button(toolbar, text='Редактировать', bg='#DCDCDC', bd=0,
                                    image=self.update_img, compound=tk.TOP, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=('ID', 'description', 'costs', 'total'),
                                 height=20, show='headings')
        self.tree.column('ID', width=40, anchor=tk.CENTER)
        self.tree.column('description', width=300, anchor=tk.CENTER)
        self.tree.column('costs', width=150, anchor=tk.CENTER)
        self.tree.column('total', width=150, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('description', text='Название')
        self.tree.heading('costs', text='Наличие')
        self.tree.heading('total', text='Сумма')

        self.tree.pack()

    def records(self, description, costs, total):
        self.db.insert_data(description, costs, total)
        self.view_records()

    def update_record(self, description, costs, total):
        self.db.exemplar.execute('''UPDATE resources SET description=?, costs=?, total=? WHERE ID=?''',
                                 (description, costs, total, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    def view_records(self):
        self.db.exemplar.execute('''SELECT * FROM resources''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.exemplar.fetchall()]

    def open_dialog(self):
        Insert()

    def open_update_dialog(self):
        Update()


class Form(ABC, tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавить ресурсы')
        self.geometry('500x225+300+300')
        self.resizable(False, False)

        label_description = ttk.Label(self, text='Наименование:')
        label_description.place(x=50, y=50)

        label_select = ttk.Label(self, text='Наличие:')
        label_select.place(x=50, y=80)

        label_sum = ttk.Label(self, text='Сумма:')
        label_sum.place(x=50, y=110)

        self.entry_description = ttk.Entry(self)
        self.entry_description.place(x=200, y=50)

        self.entry_money = ttk.Entry(self)
        self.entry_money.place(x=200, y=100)

        self.combobox = ttk.Combobox(self, values=[u'Присутствует', u'Отсутствует'])
        self.combobox.current(0)
        self.combobox.place(x=200, y=75)

        self.btn_add = ttk.Button(self, text='Добавить')
        self.btn_add.place(x=170, y=150)
        self.btn_add.bind('<Button-1>', lambda event: self.view.records(self.entry_description.get(),
                                                                        self.combobox.get(),
                                                                        self.entry_money.get()))

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=270, y=150)

        self.grab_set()
        self.focus_set()


class Insert(Form):
    def __init__(self):
        super().__init__()
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавить ресурсы')
        self.geometry('500x225+300+300')
        self.resizable(False, False)

        label_description = ttk.Label(self, text='Наименование:')
        label_description.place(x=50, y=50)

        label_select = ttk.Label(self, text='Наличие:')
        label_select.place(x=50, y=80)

        label_sum = ttk.Label(self, text='Сумма:')
        label_sum.place(x=50, y=110)

        self.entry_description = ttk.Entry(self)
        self.entry_description.place(x=200, y=50)

        self.entry_money = ttk.Entry(self)
        self.entry_money.place(x=200, y=100)

        self.combobox = ttk.Combobox(self, values=[u'Присутствует', u'Отсутствует'])
        self.combobox.current(0)
        self.combobox.place(x=200, y=75)

        self.btn_add = ttk.Button(self, text='Добавить')
        self.btn_add.place(x=170, y=150)
        self.btn_add.bind('<Button-1>', lambda event: self.view.records(self.entry_description.get(),
                                                                        self.combobox.get(),
                                                                        self.entry_money.get()))

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=270, y=150)

        self.grab_set()
        self.focus_set()


class Update(Form):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app

    def init_edit(self):
        self.title('Редактировать позицию')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=130, y=150)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_description.get(),
                                                                          self.combobox.get(),
                                                                          self.entry_money.get()))
        self.btn_add.destroy()


if __name__=="__main__":
    root = tk.Tk()
    db = DB()
    app = Mediator(root)
    app.pack()
    root.title("Working resources")
    root.geometry("650x450+300+200")
    root.resizable(False, False)
    root.mainloop()
