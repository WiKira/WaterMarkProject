from tkinter import *
from PIL import ImageTk, Image, ImageFont, ImageDraw
from tkinter import filedialog, messagebox
from tkinter.constants import DISABLED, NORMAL

ORIGINAL_IMG = None
EDITED_IMG = None

def get_img():
    try:
        filename = openfn()
        img = Image.open(filename)
        img = ImageTk.PhotoImage(img)
        return img, filename
    except:
        messagebox.showerror("Erro", "Não foi possível carregar a imagem.")


def get_original_img():
    global ORIGINAL_IMG
    img, _ = get_img()
    ORIGINAL_IMG = _
    img_panel.configure(image=img, height=img.height(), width=img.width())
    img_panel.image = img


def get_logo_img():
    img, filename = get_img()
    entry['state'] = NORMAL
    entry.delete(0, END)
    entry.insert(0, filename)
    entry['state'] = DISABLED


def sel(var):
    value = var.get()
    if value == 1:
       btnLogo['state'] = DISABLED
       entry['state'] = NORMAL
       entry.delete(0, END)
    else:
        btnLogo['state'] = NORMAL
        entry.delete(0, END)
        entry['state'] = DISABLED


def openfn():
    filename = filedialog.askopenfilename(title='open')
    return filename


def generate_image(var):
    global EDITED_IMG

    value = var.get()
    img = Image.open(ORIGINAL_IMG)

    if value == 1:
        draw = ImageDraw.Draw(img)
        mf = ImageFont.truetype('arial.ttf', 50)
        draw.text(((img.width-(len(entry.get())*25))// 2, img.height // 2), entry.get() , (255, 255, 255, 1), font=mf)
    else:
        logo = Image.open(entry.get()).resize((img.width//5, img.height//5))
        logo2 = logo.copy()
        logo_w, logo_h = logo.size
        logo.putalpha(50)
        logo.paste(logo2, logo)
        img.paste(logo, (((img.width - logo_w) // 2, (img.height - logo_h) // 2)), logo)

    EDITED_IMG = img
    edited_img = ImageTk.PhotoImage(img)
    img_panel.configure(image=edited_img)
    img_panel.image = edited_img


def save_img():
    try:
        if EDITED_IMG:
            files = [('PNG', '*.png'),
                     ('JPG', '*.jpg'),
                     ('All Files', '*.*')]
            filename = filedialog.asksaveasfile(title='open', filetypes=files)
            EDITED_IMG.save(filename.name)
            messagebox.showinfo("Sucesso", "Imagem Salva com Sucesso.")
    except:
        messagebox.showerror("Erro", "Ocorreu um erro ao salvar a imagem.")

root = Tk()
root.resizable(width=True, height=True)

title_label = Label(root, text="WaterMarkit", font=("Arial", 16, "bold"))
title_label.grid(row=0, column=0, sticky=NSEW, pady=5, columnspan=5, padx=5)

btn = Button(root, text='Open Image', command=get_original_img)
btn.grid(row=1, column=0, pady=2, columnspan=5, padx=5)

var = IntVar(value=1)
R1 = Radiobutton(root, text="Add Text", variable=var, value=1, command=lambda: sel(var))
R1.grid(row=2, column=0, sticky=W, pady=2, padx=5)
R2 = Radiobutton(root, text="Add Image", variable=var, value=2, command=lambda: sel(var))
R2.grid(row=2, column=1, sticky=W, pady=2, padx=5)

entry = Entry(root, width=100)
entry.focus_set()
entry.grid(row=3, column=0, sticky=W, pady=2, columnspan=1, padx=5)
btnLogo = Button(root, text='Search Logo', command=get_logo_img, state="disabled")
btnLogo.grid(row=3, column=1, sticky=W, pady=2, padx=5)

generate_btn = Button(root, text='Generate', command=lambda: generate_image(var))
generate_btn.grid(row=4, column=0, sticky=W, pady=2, padx=5)

save_btn = Button(root, text='Save', width=9, command=save_img)
save_btn.grid(row=4, column=1, sticky=W, pady=2, padx=5)

img_panel = Label(root, width=100, height=50)
img_panel.grid(row=5, column=0, sticky=W, pady=2, padx=5, columnspan=2)

root.mainloop()
