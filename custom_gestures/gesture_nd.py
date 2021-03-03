from kivy.gesture import GestureDatabase
from kivy.garden.navigationdrawer import NavigationDrawer as ND
from kivy.gesture import Gesture

# 生成的手势字符串
gesture_strings = {
    'top_to_bottom_line':'eNptl2tQlFUYxxcvqGQBooYoQWW6lindL2a7lbXdJURbBRQW3lwEYZ+9KKgHQQ26WCJhiIZShlommRRh4YjD4EzNVBRdjKjB8UszlVnTB0c/2Nl3nmfmP2fcOQMvv/2dPc/5v897gOqRhSXFayrnrLRC4UjQivPwd3LMqqEYRSOc3tEOh2NtcVHYTyM97qmXo69hb6yGfqt4pT9Mozzuklb9o2OEN15/5U9aEQiWF0UKwzTa444NDZ7srp7nHaPfDoWD5SVWiGLzaMwVl15kC3E0VhcwTlGc014rUF5cFg7RVXk03nnFaZlRIY6u1rOuURTv9MboWRWU4HFtbupPavraYYNKSvS4fulomdrRkhzx+aP2BEVJTr/2tg45pw3NqPZr42df3RRfnRgTFU0yjZ/aOpvaOuvZmKzoWtP4YU/v4j29mWwkK5piGgPRwvoT2EhRNNU0vq0f0qOfjWmKUk3jm6SBtKSBdDauU5RmG+H95yfu/8sRNb6kAyl0QFZJV3S9aZy6EDv5QqwYNyi60Tbc/zoS/vndNnqrrKQqS4zpim6KGicCqwIJq0K2cbwrmNoVFGOGopmm0dmXMbkvQwynolm2UVNZn1i53d7L4axTqVmnHGzcrOgW09jROHtS42wxZiu61TBOVJwNJJ8lMeYommsa+7LHJmWPlcQyFN1mGkfP5U44lyvG7YruMI3jOa7UHJfs5U5Fd5nGyYZLiQ2XpIPuVnSPafS1ntnRemYnG/cqus80vkjZ1JyySYz7Fc0zja+621u62w+y8YCi+abRv3umHqfZeFCRyzS++3O+HtJjbkUPmcb3y/9o1IONhxU9Yho/Xpy+5OJ0LxsLFD1qGqc7/4sONh5T5DGNwVDfslBfLhuPK3rCNH5dmq7HEBtPKnrKNH6rOaTHMBtPK3rGNIYXLKzXg41nFS00jTOlg9tLBxsiPss7PnpeFQYtq4yPn8w8es7pcZe67FPQ497YHz33YmopC2FPFDpqaRHCvfZFLWUjrGdzMcJqhksQBhg+r2G+fa1hJkMvQjfDpQjTGS5DmMAwB6GDYS7AqvMM8xAOM1yOsJ/hCoQ9nFI+wiNsFiDcxin5EEoghQglkCKEEoiFUAJ5AeFcXmglQknJj1BSKkYoKa0CqCSlEoQSSClC6ZDVCCWQMoStDMsRSiABhPkMCaHsPYgwg2EIYRoHEoau23Ceb1wEodz3NRqm8/QNUvxahFJ8BUIpvhKh3Lh1GtqXMRpKnesRyu3YAHC9JK8QSshVCKWkjfqPlmFefb30UjXChRxIDUIpaRNCKWmzhj280Lq/efoWhFLSiwilpFqEklIdQknpJYTStC8jlP58BWClrP4qwo1c51aEstBrCGWbrwOskPbehlCaoR6h7Gg7Qjc3WAPCeC7pDYBr5RY3IpQd7UAoeb6JUFZvQiiPzE6E8sg0I5SQdyGUkHcDXCO/Ed5CKId/C0IpaQ9CKWkvQhdPb0Uot+NtgBE5ad9BKIHsQyg9/y5C2XsbQjkq9yOU1Q8ADMvJcBChrP4eQtn7+wgzufhDCCX5DwCG5Fw6jPAE19mOUBb6EKFs8wjA4GWe/hFCae+jCKXrOhDKNj9GKCF/glAerk75v0mfIUE5WD5FKGdyF0JJ/piG1fKZ0oqfWRFfgXecvg6Xl1rBgrJCiz73uI41R1+7vKP0G2UFqy3q9kZ9Oh7xzfkf8O5LNA==',
    'left_to_right_line':'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',
    'right_to_left_line': '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',
}

# 存储数据
gestures = GestureDatabase()
for name, gesture_string in gesture_strings.items():
    gesture = gestures.str_to_gesture(gesture_string)
    gesture.name = name
    gestures.add_gesture(gesture)


class GestureBox(ND):

    def __init__(self, **kwargs):
        for name in gesture_strings:
            self.register_event_type('on_{}'.format(name))
        super(GestureBox, self).__init__(**kwargs)

    def on_left_to_right_line(self):
        pass

    def on_right_to_left_line(self):
        pass

    def on_bottom_to_top_line(self):
        pass

    def on_top_to_bottom_line(self):
        pass

    def on_touch_down(self, touch):
        touch.ud['gesture_path'] = [(touch.x, touch.y)]
        super(GestureBox, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        try:
            # touch.ud['line'].points += [touch.x, touch.y]
            touch.ud['gesture_path'].append((touch.x, touch.y))
            super(GestureBox, self).on_touch_move(touch)
        except (KeyError) as e:
            print('KeyError has excepted')

    def on_touch_up(self, touch):
        # 判断是否匹配
        if 'gesture_path' in touch.ud:
            # 创建一个手势
            gesture = Gesture()
            # 添加移动坐标
            gesture.add_stroke(touch.ud['gesture_path'])
            # 标准化大小
            gesture.normalize()
            # 匹配手势,minscore:手势灵敏度
            match = gestures.find(gesture, minscore=0.5)
            if match:
                print("{} happened".format(match[1].name))
                self.dispatch('on_{}'.format(match[1].name))
        super(GestureBox, self).on_touch_up(touch)
