import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GObject
import qrcode
import os
import sys

def generate_qr_code(data, filename="qrcode.png", box_size=10, border=4, error_correction="M"):
    """Generates a QR code image from the given data and saves it as a PNG file."""

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT[error_correction],
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    print(f"QR code generated and saved as {filename}")


class QRCodeGeneratorWindow(Gtk.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #Gtk.Window.__init__(self, title="QR Code Generator")
        #self.set_default_size(400, 300)

        # Widgets
        self.data_label = Gtk.Label(label="Data:")
        self.data_entry = Gtk.Entry()

        self.filename_label = Gtk.Label(label="Filename (e.g., myqrcode.png):")
        self.filename_entry = Gtk.Entry()

        self.box_size_label = Gtk.Label(label="Box Size:")
        self.box_size_entry = Gtk.Entry()
        self.box_size_entry.set_text("10")  # Default
    

        self.border_label = Gtk.Label(label="Border:")
        self.border_entry = Gtk.Entry()
        self.border_entry.set_text("4")

        self.error_correction_label = Gtk.Label(label="Error Correction:")
        self.store = Gtk.ListStore(str)
        self.store.append(["L"])
        self.store.append(["M"])
        self.store.append(["Q"])
        self.store.append(["H"])

        self.error_correction_combo = Gtk.ComboBox.new_with_model(self.store)

        

        # Buttons
        self.generate_button = Gtk.Button(label="Generate")
        self.clear_button = Gtk.Button(label="Clear")

        # Layout
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.append(self.data_label)
        vbox.append(self.data_entry)
        vbox.append(self.filename_label)
        vbox.append(self.filename_entry)
        vbox.append(self.box_size_label)
        vbox.append(self.box_size_entry)
        vbox.append(self.border_label)
        vbox.append(self.border_entry)
        vbox.append(self.error_correction_label)
        vbox.append(self.error_correction_combo)
        vbox.append(self.generate_button)
        vbox.append(self.clear_button)

        self.add(vbox)
        #self.set_child(vbox)

        # Connect signals
        self.generate_button.connect("clicked", self.on_generate_clicked)
        self.clear_button.connect("clicked", self.on_clear_clicked)

    def on_generate_clicked(self, widget):
        data = self.data_entry.get_text()
        filename = self.filename_entry.get_text() or "qrcode.png"
        box_size = int(self.box_size_entry.get_text()) or 10
        border = int(self.border_entry.get_text()) or 4
        error_correction = self.error_correction_combo.get_active().upper()

        generate_qr_code(data, filename, box_size, border, error_correction)

    def on_clear_clicked(self, widget):
        self.data_entry.set_text("")
        self.filename_entry.set_text("")
        self.box_size_entry.set_text("10")
        self.border_entry.set_text("4")
        self.error_correction_combo.set_active(0)  # Reset to default

app = QRCodeGeneratorWindow()
app.run(sys.argv)


