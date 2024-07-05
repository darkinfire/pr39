import os
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.label import Label



class CameraApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        self.main_screen_button = Button(text='Перейти на основной экран', size_hint=(1, None), height=50)
        self.main_screen_button.bind(on_press=self.show_main_screen)
        self.layout.add_widget(self.main_screen_button)

        self.camera_button = Button(text='Открыть камеру', size_hint=(1, None), height=50)
        self.camera_button.bind(on_press=self.open_camera)
        self.layout.add_widget(self.camera_button)

        return self.layout

    def open_camera(self, instance):
        self.camera = Camera(play=True)
        self.camera.bind(on_texture=self.capture_image)
        self.layout.clear_widgets()
        self.layout.add_widget(self.camera)

    def capture_image(self, camera, texture):
        current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        image_name = f'photo_{current_time}.jpg'

        image_path = os.path.join('./photos', image_name)
        camera.export_to_png(image_path)
        self.show_capture_popup(image_path)

        self.camera.play = False
        self.layout.clear_widgets()
        self.layout.add_widget(self.main_screen_button)
        self.layout.add_widget(self.camera_button)

    def show_capture_popup(self, image_path):
        image = Image(source=image_path)
        popup_layout = BoxLayout(orientation='vertical')
        popup_layout.add_widget(image)

        creation_time_label = Label(text=f'Дата и время создания: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        popup_layout.add_widget(creation_time_label)

        popup = Popup(title='Сохранено!', content=popup_layout, size_hint=(None, None), size=(400, 400))
        popup.open()

    def show_main_screen(self, instance):
        self.layout.clear_widgets()
        self.layout.add_widget(self.main_screen_button)
        self.layout.add_widget(self.camera_button)


if __name__ == '__main__':
    if not os.path.exists('./photos'):
        os.makedirs('./photos')
    CameraApp().run()
