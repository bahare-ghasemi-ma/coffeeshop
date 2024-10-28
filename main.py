""" 
coffee_shop

ver:1.0.1
programmer: bahareh ghasemi

"""



import tkinter as tk
from tkinter import ttk
# from tkinter import *
from paygahdadeh import table_factor_selection,enter_factor_info
from paygahdadeh import  table_kala_selection,table_kala_insert, table_kala_update,show_top10_kala
from paygahdadeh import table_customer_selection,table_customer_insert,table_customer_update,search_customer_db,show_kalahay_factor_db
from datetime import datetime
import tkinter.messagebox as messagebox
import pandas as pd
from PIL import Image, ImageTk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib import font_manager
import arabic_reshaper
from matplotlib.pyplot import *
from bidi.algorithm import get_display
root = tk.Tk()
current_date = datetime.now().strftime('%Y-%m-%d')
root.title(f'بهاره قاسمی 503  - {current_date}')
root.geometry('900x900')



def clear_frame():
    for widget in content_frame.winfo_children():
        widget.destroy()

def show_order_form():
    clear_frame()
    kala_lst = table_kala_selection()
    selected_orders = {}
    
    tk.Label(content_frame, text="شماره مشتری:").grid(row=0, column=0, padx=5, pady=30, sticky='w')
    customer_id_entry = tk.Entry(content_frame)
    customer_id_entry.grid(row=0, column=1, padx=5, pady=30, sticky='w')
    
    tk.Label(content_frame, text="تاریخ:").grid(row=0, column=2, padx=5, pady=30, sticky='w')
    date_entry = tk.Entry(content_frame)
    date_entry.grid(row=0, column=3, padx=5, pady=30, sticky='w')
    date_entry.insert(0, current_date)

    def add_order(item):
        item_id = item[0]
        item_name = item[1]
        if item_name in selected_orders:
            selected_orders[item_name][1] += 1
            selected_orders[item_name][3] += int(item[2])
        else:
            selected_orders[item_name] = [item[0], 1, item[2], (int(item[2])*1)]
        update_order_list()
    
    def update_order_list():
        for item in tree.get_children():
            tree.delete(item)
        for name, (id, count, price, sum_row) in selected_orders.items():
            tree.insert("", "end", values=(id, name, price, count, sum_row))
    
    def remove_order():
        selected_item = tree.selection()[0]
        item = tree.item(selected_item)["values"]
        item_name = item[1]
        if item_name in selected_orders:
            if selected_orders[item_name][1] > 1:
                selected_orders[item_name][1] -= 1
                selected_orders[item_name][3] -= int(item[2])
            else:
                del selected_orders[item_name]
        update_order_list()
    
    def edit_order():
        selected_item = tree.selection()[0]
        item = tree.item(selected_item)["values"]
        item_name = item[1]
        if item_name in selected_orders:
            new_count = int(count_entry.get())
            if new_count > 0:
                selected_orders[item_name][1] = new_count
                selected_orders[item_name][3] = int(item[2]) * new_count
                update_order_list()
            count_entry.delete(0, tk.END)

    cols = 4
    for i, item in enumerate(kala_lst):
        btn = tk.Button(content_frame, text=f"{item[1]}", command=lambda item=item: add_order(item), width=13, height=1)
        btn.grid(row=(i//cols) + 1, column=i%cols, padx=2, pady=2, sticky='w')

    def register_order():
        list_kala = [v for k,v in selected_orders.items()]
        factor_id = enter_factor_info(customer_id=customer_id_entry.get(),
                          factor_date=date_entry.get(),
                          list_kala=list_kala) 
        
        yes_no= messagebox.askyesno("ثبت موفق", " سفارش با موفقیت ثبت شد، آیا مایل به چاپ هستید؟؟!")
        if yes_no:
            print_order()

        customer_id_entry.delete(0, tk.END)
        selected_orders.clear()
        for item in tree.get_children():
            tree.delete(item)

    def print_order():
        list_kala = [v for k,v in selected_orders.items()]
        factor_id = enter_factor_info(customer_id=customer_id_entry.get(),
                        factor_date=date_entry.get(),
                        list_kala=list_kala) 
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", 
                                             filetypes=[("CSV files", "*.csv")],
                                             title="انتخاب مسیر و نام فایل برای ذخیره",
                                             initialfile=f"order_{factor_id}.csv")

        if file_path:
       
            df = pd.DataFrame(list_kala, columns=["شماره کالا", "تعداد", "قیمت واحد", "جمع ردیف"])
            df["شماره فاکتور"] = factor_id
            df["شماره مشتری"] = customer_id_entry.get()
            df["تاریخ"] = current_date
            df.to_csv(file_path, index=False, encoding='utf-8-sig')
            messagebox.showinfo("چاپ موفق", f"سفارش به صورت CSV ذخیره شد در: {file_path}")
        else:
            messagebox.showinfo("چاپ لغو شد", "چاپ سفارش لغو شد.")


    cols = ("id", "name", "price", "count", "sum_row")
    tree = ttk.Treeview(content_frame, columns=cols, show="headings", height=5)
    tree.heading("id", text="شماره کالا")
    tree.heading("name", text="نام کالا")
    tree.heading("price", text="قیمت (تومان)")
    tree.heading("count", text="تعداد")
    tree.heading("sum_row", text="جمع ردیف")

    # تنظیم عرض ستون‌ها
    tree.column("id", width=70, anchor='center')
    tree.column("name", width=150, anchor='center')
    tree.column("price", width=80, anchor='center')
    tree.column("count", width=50, anchor='center')
    tree.column("sum_row", width=100, anchor='center')

    tree.grid(row=8, column=0, columnspan=20, sticky='w')

    tk.Button(content_frame, text="ویرایش", command=edit_order).grid(row=9, column=0, sticky='w', padx=5,pady=5)
    tk.Button(content_frame, text="حذف", command=remove_order).grid(row=9, column=1, sticky='w', padx=5,pady=5)

    tk.Label(content_frame, text="تعداد جدید:").grid(row=9, column=2, sticky='w', padx=5,pady=5)
    count_entry = tk.Entry(content_frame )
    count_entry.grid(row=9, column=3,sticky='w', padx=5,pady=5)

    tk.Button(content_frame, text="ثبت سفارش", command=register_order).grid(row=10, column=0, sticky='w', padx=5,pady=5)

# //////////////////////////////کالاها//////////////////////////////////

def show_kala_form(): 
    global  entry_item_name, entry_item_price, tree
    clear_frame()
    kala_list = table_kala_selection()

    cols = ('شماره کالا', 'نام کالا', 'قیمت کالا')
    tree = ttk.Treeview(content_frame, columns=cols, show='headings')
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor='center', stretch=False)
    tree.grid(row=0, column=0, columnspan=10)
    for row in kala_list:
        tree.insert('', tk.END, values=row)

    tree.bind("<<TreeviewSelect>>", edit_kala)
    labels = ['نام کالا', 'قیمت کالا']
    entries = []

    for i, text in enumerate(labels, start=1):
        tk.Label(content_frame, text=text).grid(row=i+1, column=0, padx=1, pady=5, sticky='w')
        entry = tk.Entry(content_frame)
        entry.grid(row=i+1, column=1, padx=1, pady=5, sticky='w')
        entries.append(entry)

    entry_item_name, entry_item_price = entries
    tk.Button(content_frame, text='ثبت در منو', command=insert_kala, borderwidth=5, padx=1, pady=5).grid(row=len(cols) + 2, column=0, columnspan=1, padx=5, pady=5)
    tk.Button(content_frame, text='ویرایش منو',command=edit_kala2, borderwidth=5, padx=1, pady=5 ).grid(row=len(cols) + 2, column=1, columnspan=1, padx=5, pady=5)
    tk.Button(content_frame, text=' نمایش کالاهای محبوب',command=plot_top10_kala, borderwidth=5, padx=1, pady=5 ).grid(row=len(cols) + 2, column=4, columnspan=3, padx=20, pady=5)


def insert_kala():
    
    item_name = entry_item_name.get()
    item_price = entry_item_price.get()
    if len(item_name) ==0 or len(item_price) == 0 : 
        messagebox.showinfo("ثبت",".لطفا نام کالا و قیمت را پر کنید")
        return
    table_kala_insert( item_name, item_price)
    #tree.insert('', tk.END, values=( item_name, item_price))
    
    entry_item_name.delete(0, tk.END)
    entry_item_price.delete(0, tk.END)
    messagebox.showinfo("ثبت موفق", "کالا با موفقیت به منو اضافه شد!")
    show_kala_form()

def edit_kala(event):

    entry_item_name.delete(0, tk.END)
    entry_item_price.delete(0, tk.END)
    selected_item = tree.selection()[0] 

    item = tree.item(selected_item)["values"]
    item_id = item[0]
    entry_item_name.insert(0,item[1])
    entry_item_price.insert(0,item[2])
    

def edit_kala2():
   
    selected_item = tree.selection()[0] 
    item = tree.item(selected_item)["values"]
    item_id = item[0]
    table_kala_update(item_id,entry_item_name.get(),entry_item_price.get())

    entry_item_name.delete(0, tk.END)
    entry_item_price.delete(0, tk.END)
    messagebox.showinfo("ثبت موفق", "کالا با موفقیت ثبت شد!")
    show_kala_form()



def plot_top10_kala():
    data = show_top10_kala()

    kala_name = [item[1] for item in data]  # لیست کالاها
    occurrence_counts = [item[2] for item in data]  # لیست تعداد وقوع

   
    reshaped_kala_name = [get_display(arabic_reshaper.reshape(name)) for name in kala_name]
    reshaped_xlabel = get_display(arabic_reshaper.reshape("تعداد فروش"))
    reshaped_ylabel = get_display(arabic_reshaper.reshape("نام کالا"))
    reshaped_title = get_display(arabic_reshaper.reshape("10 کالای برتر"))

   
    font_path = 'E:\\Softwares\\Editor\\Farsi Fonts\\BFonts\\BNazanin.ttf' 
    font_prop = font_manager.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()
    
    plt.figure(figsize=(10, 6))
    plt.bar(reshaped_kala_name, occurrence_counts, color='skyblue')
    plt.xlabel(reshaped_xlabel, fontproperties=font_prop)
    plt.ylabel(reshaped_ylabel, fontproperties=font_prop)
    plt.title(reshaped_title, fontproperties=font_prop)
    
    plt.show()



# ////////////////////کالاها پایان////////////////////////



# /////////////////////مشتریان///////////////////////

def show_customers_form():
    global entry_customer_name, entry_customer_family, entry_customer_phone, tree
    clear_frame()
    customer_list = table_customer_selection()

    cols = ("شماره مشتری", "نام", "نام خانوادگی", "تلفن")
    tree = ttk.Treeview(content_frame, columns=cols, show='headings', )
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor='center', stretch=False)
    tree.grid(row=0, column=0, columnspan=10)
    for row in customer_list:
        tree.insert('', tk.END, values=row)

    tree.bind("<<TreeviewSelect>>", edit_customer)

    labels = [ "نام", "نام خانوادگی", "تلفن"]
    entries = []

    for i, text in enumerate(labels, start=1):
        tk.Label(content_frame, text=text).grid(row=i+1, column=0, padx=1, pady=5, sticky='w')
        entry = tk.Entry(content_frame)
        entry.grid(row=i+1, column=1, padx=1, pady=5, sticky='w')
        entries.append(entry)

    entry_customer_name, entry_customer_family, entry_customer_phone = entries
    tk.Button(content_frame, text='ثبت مشتری', borderwidth=5, padx=1, pady=5, command=insert_customer).grid(row=len(cols) + 2, column=0, columnspan=2, padx=10, pady=5)

    tk.Button(content_frame, text='ویرایش مشتری', borderwidth=5, padx=1, pady=5, command=edit_customer2).grid(row=len(cols) + 2, column=1, columnspan=7, padx=10, pady=5)

def insert_customer():
   
    customer_name = entry_customer_name.get()
    customer_family = entry_customer_family.get()
    customer_phone = entry_customer_phone.get()
    if len(customer_name) ==0 or len(customer_family) == 0 or len(customer_phone)==0 : 
        messagebox.showinfo("ثبت",".لطفا تمام فیلدها را پر کنید")
        return
    table_customer_insert(customer_name, customer_family, customer_phone)

    entry_customer_name.delete(0, tk.END)
    entry_customer_family.delete(0, tk.END)
    entry_customer_phone.delete(0, tk.END)
    show_customers_form()
    messagebox.showinfo("ثبت موفق", "مشتری جدیداضافه شد!")

def edit_customer(event):

    entry_customer_name.delete(0, tk.END)
    entry_customer_family.delete(0, tk.END)
    entry_customer_phone.delete(0, tk.END)
    selected_item = tree.selection()[0] 

    item = tree.item(selected_item)["values"]
    customer_id = item[0]

    entry_customer_name.insert(0,item[1])
    entry_customer_family.insert(0,item[2])
    entry_customer_phone.insert(0,item[3])



def edit_customer2():
   
    selected_item = tree.selection()[0] 
    item = tree.item(selected_item)["values"]
    customer_id = item[0]
    table_customer_update(customer_id,entry_customer_name.get(),entry_customer_family.get(),entry_customer_phone.get())

    entry_customer_name.delete(0, tk.END)
    entry_customer_family.delete(0, tk.END)
    entry_customer_phone.delete(0, tk.END)
    show_customers_form()
    messagebox.showinfo("ویرایش موفق", "مشتری ویرایش شد!")

# //////////////////////// اطلاعات مشتریان پایان/////////////////////////////////////


# /////////////////////////جستجوی فاکتور////////////////////////////////////////////

def search_customer_form():
    def search_customer():
        for item in tree.get_children():
            tree.delete(item)
        factor_date1=date_entry1.get()
        factor_date2=date_entry2.get()
        customer_name=customer_name_entry.get()
        
        customer_list = search_customer_db(factor_date1,factor_date2,customer_name)
        
        for row in customer_list:
            tree.insert('', tk.END, values=row)
    
    def show_kalahay_factor(event):

        for item in tree2.get_children():
            tree2.delete(item)
        selected_item = tree.selection()[0] 
        item = tree.item(selected_item)["values"]
        item_id = item[0]
        kala_list = show_kalahay_factor_db(item_id)
        for row in kala_list:
            tree2.insert('', tk.END, values=row)

        

    clear_frame()
    tk.Label(content_frame, text=" از تاریخ :").grid(row=0, column=0, padx=1, pady=1, sticky='w')
    date_entry1 =tk.Entry(content_frame)
    tk.Label(content_frame, text="تا تاریخ :").grid(row=1, column=0, padx=1, pady=1, sticky='w')
    date_entry2 =tk.Entry(content_frame)
    tk.Label(content_frame, text="نام مشتری  :").grid(row=2, column=0, padx=1, pady=1, sticky='w')
    customer_name_entry =tk.Entry(content_frame)

    date_entry1.grid(row=0, column=1, padx=5, pady=5, sticky='w')
    date_entry2.grid(row=1, column=1, padx=5, pady=5, sticky='w')
    customer_name_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

    tk.Button(content_frame, text= ' جستجوی مشتری  ',borderwidth=5, padx=1, pady=5,command=search_customer).grid(row = 0,column=2, columnspan=3,padx=10, pady=5)
    cols = ("شماره فاکتور","شماره مشتری", "نام", "نام خانوادگی", "تلفن")
    tree = ttk.Treeview(content_frame, columns=cols, show='headings', )
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor='center', stretch=False)
    tree.grid(row=3, column=0, columnspan=6)

    tree.bind("<<TreeviewSelect>>", show_kalahay_factor)


    cols = ("اسم کالا","تعداد","قیمت ","قیمت ردیف")
    tree2 = ttk.Treeview(content_frame, columns=cols, show='headings', )
    for col in cols:
        tree2.heading(col, text=col)
        tree2.column(col, width=100, anchor='center', stretch=False)
    tree2.grid(row=16, column=0, columnspan=6)



# //////////////////////////////////////////////////////////////////////////////

button_frame = tk.Frame(root, bg='#FFF0E0')
button_frame.place(relwidth=0.2, relheight=1)

order_button = ttk.Button(button_frame, text='ثبت سفارش', command=show_order_form)
order_button.pack(pady=10, padx=10)

store_button = ttk.Button(button_frame, text='منو', command=show_kala_form)
store_button.pack(pady=10, padx=10)

customers_button = ttk.Button(button_frame, text='اطلاعات مشتریان', command=show_customers_form)
customers_button.pack(pady=10, padx=10)

customers_button = ttk.Button(button_frame, text='جستجوی فاکتور' , command=search_customer_form)
customers_button.pack(pady=10, padx=10)

content_frame = tk.Frame(root, bg='#FFF0E0')
content_frame.place(relx=0.2, rely=0.0, relwidth=0.6, relheight=1.0)



content_frame2 = tk.Frame(root, bg="blue")
content_frame2.place(relx=0.8, rely=0.0, relwidth=0.2, relheight=1.0)

canvas = tk.Canvas(content_frame2, bg="#FFFFCC", highlightthickness=0)
canvas.pack(fill="both", expand=True)
text = " کافی شاپ "
canvas.create_text(100, 350, text=text, fill="orange", font=("Arial", 35), angle=90)

image_path = "F:\\Python_learning\\Radman\\projects\\503_bahareh_ghasemi_coffeeshop\\storage\\coffee.png"  
image = Image.open(image_path)
image = image.resize((150, 150)) 
photo = ImageTk.PhotoImage(image)


image_label_top = tk.Label(content_frame2, image=photo, bg="orange")
image_label_top.place(relx=0.5, rely=0.05, anchor="n")


image_label_bottom = tk.Label(content_frame2, image=photo, bg="orange")
image_label_bottom.place(relx=0.5, rely=0.85, anchor="s")

image_label_top.image = photo
image_label_bottom.image = photo
root.mainloop()



