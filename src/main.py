#!/usr/bin/python3
# -*- coding: utf-8 -*-
import gi
import os
import json
from datetime import date
from pathlib import Path
import sys
sys.path.append("/app")
from translations.en import *
gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

today = date.today()

from gi.repository import Adw, Gio, Gtk, Gdk, GLib, GObject

Adw.init()

class DialogSelecFolder(Gtk.FileChooserDialog):
    home = Path.home()

    def __init__(self, parent, select_multiple):
        super().__init__(transient_for=parent, use_header_bar=True)
        self.select_multiple = select_multiple

        self.set_action(action=Gtk.FileChooserAction.OPEN)
        title = 'Choose some archives' if self.select_multiple else 'Choose an archive'
        self.set_title(title=title)
        self.set_modal(modal=True)
        self.set_select_multiple(select_multiple=self.select_multiple)
        self.connect('response', self.dialog_response)
        self.set_current_folder(
            Gio.File.new_for_path(path=str(self.home)),
        )

        self.add_buttons(
            '_Cancel', Gtk.ResponseType.CANCEL,
            '_Select', Gtk.ResponseType.OK
        )
        btn_select = self.get_widget_for_response(
            response_id=Gtk.ResponseType.OK,
        )
        # Adicionando estilo no botão.
        btn_select.get_style_context().add_class(class_name='suggested-action')
        btn_cancel = self.get_widget_for_response(
            response_id=Gtk.ResponseType.CANCEL,
        )
        btn_cancel.get_style_context().add_class(class_name='destructive-action')

        txt_filter = Gtk.FileFilter()
        txt_filter.set_name(name='Tar Gzip archive')
        txt_filter.add_pattern(pattern='*.tar.gz')
        txt_filter.add_mime_type(mime_type='archive')
        self.add_filter(filter=txt_filter)

        self.show()

    def dialog_response(self, widget, response):
        # Verificando qual botão foi pressionado.
        if response == Gtk.ResponseType.OK:
            if self.select_multiple:
                gliststore = self.get_files()
                for glocalfile in gliststore:
                    print(f' {glocalfile.get_path()}\n')
            else:
                glocalfile = self.get_file()
                print(f' {glocalfile.get_path()}')
                with open(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.save-desktop-configuration/data/file.json', 'w') as f:
                    f.write('{\n')
                    f.write(f' "file-path": " { glocalfile.get_path() } "')
                    f.write('\n}')
        widget.close()

class DesktopWindow(Gtk.ApplicationWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_title(title=appname)
        self.set_default_size(width=int(1000 / 2), height=int(450 / 2))
        self.set_size_request(width=int(1000 / 2), height=int(450 / 2))

        headerbar = Gtk.HeaderBar.new()
        self.set_titlebar(titlebar=headerbar)

        menu_button_model = Gio.Menu()
        menu_button_model.append(about_app, 'app.about')

        menu_button = Gtk.MenuButton.new()
        menu_button.set_icon_name(icon_name='open-menu-symbolic')
        menu_button.set_menu_model(menu_model=menu_button_model)
        headerbar.pack_end(child=menu_button)

        self.mainBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.mainBox.set_margin_start(10)
        self.mainBox.set_margin_end(10)
        self.set_child(child=self.mainBox)

        listbox = Gtk.ListBox.new()
        listbox.set_selection_mode(mode=Gtk.SelectionMode.NONE)
        listbox.get_style_context().add_class(class_name='boxed-list')
        self.mainBox.append(listbox)
        
        # Save actual configuration
        adw_expander_row = Adw.ExpanderRow.new()
        adw_expander_row.set_icon_name(icon_name='edit-find-symbolic')
        adw_expander_row.set_title(title=save_actual_config)
        listbox.append(child=adw_expander_row)
        
        # Apply saved configuration
        adw_expander_row_1 = Adw.ExpanderRow.new()
        adw_expander_row_1.set_icon_name(icon_name='edit-find-symbolic')
        adw_expander_row_1.set_title(title=apply_saved_config)
        adw_expander_row_1.set_subtitle(subtitle=apply_saved_config_desc)
        listbox.append(child=adw_expander_row_1)

        # Adw ActionRow0: Save actual configuration
        # Combobox
        types = [
            select, 'GNOME', 'KDE Plasma'
        ]
        combobox_text = Gtk.ComboBoxText.new()
        for text in types:
            combobox_text.append_text(text=text)
        combobox_text.set_active(index_=0)
        combobox_text.connect('changed', self.on_combo_box_text_changed)
        adw_action_row_0 = Adw.ActionRow.new()
        adw_action_row_0.set_icon_name(icon_name='desktop-symbolic')
        adw_action_row_0.set_title(title=de)
        adw_action_row_0.add_suffix(widget=combobox_text)
        adw_expander_row.add_row(child=adw_action_row_0)

        # Adw ActionRow1: Apply saved configuration
        types = [
            select, 'GNOME', 'KDE Plasma'
        ]
        combobox_text_b = Gtk.ComboBoxText.new()
        for text in types:
            combobox_text_b.append_text(text=text)
        combobox_text_b.set_active(index_=0)
        combobox_text_b.connect('changed', self.on_combo_box_text_b_changed)
        adw_action_row_1 = Adw.ActionRow.new()
        adw_action_row_1.set_icon_name(icon_name='desktop-symbolic')
        adw_action_row_1.set_title(title=de)
        adw_action_row_1.add_suffix(widget=combobox_text_b)
        adw_expander_row_1.add_row(child=adw_action_row_1)
        
        self.entry = Adw.EntryRow()

        self.o_btn = Gtk.Button.new_from_icon_name('folder-symbolic')
        btnc_o = self.o_btn.get_style_context()
        btnc_o.add_class('suggested-action')
        self.o_btn.connect('clicked', self.on_o_btn_clicked)
        adw_action_row_0 = Adw.ActionRow.new()
        adw_action_row_0.set_icon_name(icon_name='cd-symbolic')
        adw_action_row_0.set_title(title=path)
        adw_action_row_0.add_suffix(widget=self.entry)
        adw_action_row_0.add_suffix(widget=self.o_btn)
        adw_expander_row_1.add_row(child=adw_action_row_0)

        self.toast_overlay = Adw.ToastOverlay.new()
        self.toast_overlay.set_margin_top(margin=12)
        self.toast_overlay.set_margin_end(margin=12)
        self.toast_overlay.set_margin_bottom(margin=12)
        self.toast_overlay.set_margin_start(margin=12)
        self.mainBox.append(child=self.toast_overlay)
        
        self.button = Gtk.Button.new_with_label(label=apply)
        self.button_style_context = self.button.get_style_context()
        self.button_style_context.add_class('suggested-action')
        self.button_style_context.add_class('pill')
        self.button.set_valign(align=Gtk.Align.CENTER)
        self.button.set_vexpand(expand=True)
        self.button.connect('clicked', self.on_button_clicked)
        self.toast_overlay.set_child(child=self.button)
        
        self.check_button = Gtk.CheckButton.new_with_label(label='....')

        self.toast = Adw.Toast.new(title='')
        self.toast.connect('dismissed', self.on_toast_dismissed)
        
    def on_o_btn_clicked(self, obtn):
        select_multiple = self.check_button.get_active()
        DialogSelecFolder(parent=self, select_multiple=select_multiple)
        self.file()
    
    def file(self):
        with open(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.save-desktop-configuration/data/file.json') as f:
            jF = json.load(f)
        file = jF["file-path"]
        self.entry.set_text(file)

    def on_combo_box_text_changed(self, comboboxtext):
        with open(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.save-desktop-configuration/data/values.json', 'w') as s:
            s.write('{\n "de": "%s"\n}' % comboboxtext.get_active_text())

    def on_combo_box_text_b_changed(self, comboboxtextb):
        with open(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.save-desktop-configuration/data/values.json', 'w') as s:
            s.write('{\n "de": "%s-apply"\n}' % comboboxtextb.get_active_text())

    def on_button_clicked(self, button):
        button.set_sensitive(sensitive=False)
        self.save()
        self.toast_overlay.add_toast(self.toast)

    def save(self):
        with open(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.save-desktop-configuration/data/values.json') as s:
            jS = json.load(s)
        de = jS["de"]
        # GNOME - Save Config
        if de == "GNOME":
            if not os.path.exists(os.path.expanduser('~') + '/DesktopSavers'):
                os.mkdir(os.path.expanduser('~') + '/DesktopSavers')
            if not os.path.exists(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.save-desktop-configuration/data/GNOME'):
                os.makedirs(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.save-desktop-configuration/data/GNOME')
            os.chdir(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.save-desktop-configuration/data')
            os.system('cp ~/.config/dconf/user ./GNOME && tar --gzip -cf %s.tar.gz ./GNOME && mkdir -p ~/DesktopSavers/%s && cp %s.tar.gz $HOME/DesktopSavers/%s/' % (today, today, today, today))
        # GNOME - Apply config
        elif de == "GNOME-apply":
            entry = self.entry.get_text()
            os.system('cp %s ' % entry + os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.save-desktop-configuration/cache/tmp/ && cd ~/.var/app/com.github.vikdevelop.save-desktop-configuration/cache/tmp/ && tar -xf *.tar.gz')
            if os.path.exists(os.path.expanduser('~')+ '/.config/dconf'):
                os.system('rm -rf ~/.config/dconf')
            os.system('cd ~/.var/app/com.github.vikdevelop.save-desktop-configuration/cache/tmp/ && mkdir -p ~/.config/dconf && cp ./GNOME/user ~/.config/dconf/')
            os.system('rm ~/.var/app/com.github.vikdevelop.save-desktop-configuration/cache/tmp/GNOME')
        # KDE Plasma -Apply config
        elif de == "KDE Plasma-apply":
            entry = self.entry.get_text()
            os.system('cp %s ' % entry + os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.save-desktop-configuration/cache/tmp/ && cd ~/.var/app/com.github.vikdevelop.save-desktop-configuration/cache/tmp/ && tar -xf *.tar.gz && cp -r -f ./KDE_Plasma/* ~/.config/')
            os.system('rm ~/.var/app/com.github.vikdevelop.save-desktop-configuration/cache/tmp/KDE_Plasma')
        # KDE Plasma - Save config
        elif de == "KDE Plasma":
            if not os.path.exists(os.path.expanduser('~') + '/DesktopSavers'):
                os.mkdir(os.path.expanduser('~') + '/DesktopSavers')
            if not os.path.exists(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.save-desktop-configuration/data/KDE_Plasma'):
                os.makedirs(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.save-desktop-configuration/data/KDE_Plasma')
            os.chdir(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.save-desktop-configuration/data')
            os.system('cp ~/.config/kdeglobals ./KDE_Plasma/ && ~/.config/kscreenlockerrc ./KDE_Plasma/ && cp ~/.config/kwinrc ./KDE_Plasma/ && cp ~/.config/gtkrc ./KDE_Plasma/ && cp ~/.config/gtkrc-2.0 ./KDE_Plasma/ && cp -R ~/.config/gtk-4.0 ./KDE_Plasma/ && cp -R ~/.config/gtk-3.0 ./KDE_Plasma/ && cp ~/.config/ksplashrc ./KDE_Plasma/ && cp ~/.config/plasmarc ./KDE_Plasma/ && cp ~/.config/breezerc ./KDE_Plasma/ && cp ~/.config/kwinrc ./KDE_Plasma/ && cp ~/.config/kcmfonts ./KDE_Plasma/ && cp ~/.config/kfontinstuirc ./KDE_Plasma/ && cp ~/.config/ksplashrc ./KDE_Plasma/ && cp ~/.config/kglobalshortcutsrc ./KDE_Plasma/')
            os.system('tar --gzip -cf %s.tar.gz ./KDE_Plasma/ && mkdir -p ~/DesktopSavers/%s && cp %s.tar.gz $HOME/DesktopSavers/%s/' % (today, today, today, today))
        # Adw.Toast()
        self.toast.set_title(title=done)
        self.toast.set_button_label(open_folder)

    def on_toast_dismissed(self, toast):
        os.system('xdg-open ~/DesktopSavers')
        self.button.set_sensitive(sensitive=True)

class ExampleApplication(Adw.Application):
    def __init__(self):
        super().__init__(application_id='com.github.vikdevelop.save_desktop_configuration',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

        self.create_action('quit', self.exit_app, ['<primary>q'])
        self.create_action('about', self.on_about_action)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = DesktopWindow(application=self)
        win.present()

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def do_shutdown(self):
        Gtk.Application.do_shutdown(self)

    def on_about_action(self, action, param):
        dialog = Adw.AboutWindow(transient_for=app.get_active_window())
        dialog.set_application_name(appname)
        dialog.set_version("1.0")
        dialog.set_developer_name("vikdevelop")
        dialog.set_license_type(Gtk.License(Gtk.License.GPL_3_0))
        dialog.set_comments(appdesc)
        dialog.set_website("https://github.com/vikdevelop/save_desktop_configuration")
        dialog.set_issue_url("https://github.com/vikdevelop/save_desktop_configuration/issues")
        dialog.set_translator_credits(translator_credits)
        dialog.set_copyright("© 2022 vikdevelop")
        dialog.set_developers(["vikdevelop https://github.com/vikdevelop"])
        dialog.set_application_icon("flatpak-symbolic")
        dialog.show()

    def exit_app(self, action, param):
        self.quit()

    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect('activate', callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f'app.{name}', shortcuts)


if __name__ == '__main__':
    import sys

    app = ExampleApplication()
    app.run(sys.argv)
