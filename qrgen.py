import sys
# Load Gtk
import gi
from gi.overrides.Gtk import Adjustment
import qrcode
import os
import shutil

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gio, GObject, GdkPixbuf
from gi.repository import GdkPixbuf
from gi.repository.GdkPixbuf import InterpType

class Item(GObject.Object):
    __gtype_name__ = 'Item'
    name = GObject.Property(type=str)

class QRCodeGen(Gtk.Application):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)
        self.builder = Gtk.Builder()
        self.cwd = os.getcwd()
        self.appdir = self.cwd+"/.local/share/QRGen/"
        self.uifile = self.appdir+"qrcode.ui"
        self.builder.add_from_file(self.uifile)

    def on_activate(self, app):


        _clear_btn = self.builder.get_object("clear_btn")
        _clear_btn.connect('clicked', self.on_clear_clicked)

        _gen_btn = self.builder.get_object("gen_btn")
        _gen_btn.connect('clicked', self.on_generate_clicked)

        self.data_entry = self.builder.get_object("data_txt")
        self.download_btn = self.builder.get_object("download_btn")
        self.download_btn.connect('clicked', self.on_image_clicked)

        self.box_size_entry = self.builder.get_object("size_txt")
        self.border_entry = self.builder.get_object("border_txt")
        self.error_correction_combo = self.builder.get_object("err_correction_combo")

        self.qr = self.builder.get_object("qrcode_display")
        self.image = GdkPixbuf.Pixbuf.new_from_file_at_size(self.appdir+"default.png", 300, 300)

        self.qr.set_from_pixbuf(self.image)

       


        self.store = Gtk.ListStore(str)
        self.store.append(["L"])
        self.store.append(["M"])
        self.store.append(["Q"])
        self.store.append(["H"])
        
        self.error_correction_combo.set_model(self.store)
        self.error_correction_combo.set_active(0)
        cell = Gtk.CellRendererText()
        self.error_correction_combo.pack_start(cell, True)
        self.error_correction_combo.add_attribute(cell, "text", 0)


        window = self.builder.get_object("appwindow")
        app.add_window(window)
        window.present()

    def generate_qr_code(self, data, box_size=300, border=2, error_correction="M"):
        """Generates a QR code image from the given data and saves it as a PNG file."""
        filename=self.appdir+"qrcode.png"

        match error_correction:
            case "L":
                ERR_CORRECT=qrcode.constants.ERROR_CORRECT_L
            case "M":
                ERR_CORRECT=qrcode.constants.ERROR_CORRECT_M    
            case "Q":
                ERR_CORRECT=qrcode.constants.ERROR_CORRECT_Q
            case "H":
                ERR_CORRECT=qrcode.constants.ERROR_CORRECT_H   

        qr = qrcode.QRCode(
            version=1,
            error_correction=ERR_CORRECT,
            box_size=box_size,
            border=border,
        )
        qr.add_data(data)
        qr.make(fit=True)

        #update to have fill colors combo or color picker
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(filename)
        print(f"QR code generated and saved as {filename}")

    def on_generate_clicked(self, widget):
        data = self.data_entry.get_text()
        box_size = int(self.box_size_entry.get_text()) or 300
        border = int(self.border_entry.get_text()) or 2
        error_correction_val = self.error_correction_combo.get_active()
        mod = self.error_correction_combo.get_model()
        val = mod[error_correction_val]
        print(self.box_size_entry.get_text())

        self.generate_qr_code(data, box_size, border, val[0])
        self.image = GdkPixbuf.Pixbuf.new_from_file_at_size(self.appdir+"qrcode.png", 300, 300)
        self.qr.set_from_pixbuf(self.image)

    def on_clear_clicked(self, widget):
        self.data_entry.set_text("")
        self.box_size_entry.set_text("300")
        self.border_entry.set_text("4")
        self.error_correction_combo.set_active(0)  # Reset to default

    def on_image_clicked(self, widget):
        dialog = Gtk.FileDialog.new()
        dialog.set_title("Save QRCode as...")

        # === Create the PNG filter ===
        png_filter = Gtk.FileFilter()
        png_filter.set_name("PNG Image") 
        png_filter.add_suffix("png")  
        filters = Gio.ListStore.new(Gtk.FileFilter)
        filters.append(png_filter)
        dialog.set_filters(filters)
        dialog.set_initial_name("QR Code.png")

        dialog.save(
            parent=None,
            cancellable=None,
            callback=self.on_save_response
        )

    def on_save_response(self, dialog, result):
        try:
            file = dialog.save_finish(result)
            if file:
                path = file.get_path()
                print(f"Save to: {path}")
                shutil.copyfile("qrcode.png", file)
            else:
                pass
        except Exception as e:
            print(e)
       
  


# Create a new application
app = QRCodeGen(application_id="com.wheelerwire.qrcodegen")
app.run(sys.argv)
