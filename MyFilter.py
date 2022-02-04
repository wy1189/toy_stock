import justpy as jp
import lorem


class QDialog(jp.QDiv):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        div = self
        div_class = kwargs.get("classes")
        button_label = kwargs.get("label")
        div.classes = div_class
        c1 = jp.QBtn(label=button_label, color="primary", a=div)
        c2 = jp.QDialog(persistent=False, name="alert_dialog", a=div)
        c1.dialog = c2
        c1.on("click", self.open_dialog)
        c3 = jp.QCard(a=c2)
        c4 = jp.QCardSection(a=c3)
        jp.QDiv(classes="text-h6", text="Alert", a=c4)
        jp.QCardSection(a=c3, text=lorem.text())
        c5 = jp.QCardActions(align="right", a=c3)
        jp.QBtn(label="OK", color="primary", flat=True, v_close_popup=True, a=c5)

    @staticmethod
    def open_dialog(self, msg):
        self.dialog.value = True


class MyFilter(jp.QDiv):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        div = self
        div_class = kwargs.get("classes")
        button_label = kwargs.get("label")
        div.classes = div_class
        c1 = jp.QBtn(label=button_label, color="primary", a=div)
        c2 = jp.QDialog(persistent=False, name="alert_dialog", full_width=True, a=div)
        c1.dialog = c2
        c1.on("click", self.open_dialog)
        c3 = jp.QCard(a=c2)
        c4 = jp.QCardSection(a=c3)
        jp.QDiv(classes="text-h6", text="Alert", a=c4)
        c5 = jp.QCardSection(a=c3, classes="q-gutter-sm row wrap justify-start items-start content-start")
        filter_options = kwargs.get("options", [["test 1", "test 2"]])
        self.filter_list = []
        for option in filter_options:
            self.filter_list.append(
                jp.QSelect(a=c5, outlined=True, square=True, fill_input=False,
                           dense=True, clearable=True, use_input=False, item_aligned=True, options_dense=True,
                           options=option.get("options", []),
                           label=option.get("label", ""),
                           multiple=option.get("multiple", False),
                           style=option.get("style"))
            )
        for select in self.filter_list:
            select.on("input", self.align_select)
        c6 = jp.QCardActions(align="right", a=c3)
        jp.QBtn(label="OK", color="primary", flat=True, v_close_popup=True, a=c6)

    @staticmethod
    def open_dialog(self, msg):
        self.dialog.value = True

    @staticmethod
    def align_select(self, msg):
        if isinstance(self.value, list):
            self.value = sorted(self.value)


async def dialog_test():
    wp = jp.QuasarPage()
    QDialog(a=wp, classes="q-pa-md q-gutter-sm", label="Alert")
    option_dict = [{
        "label": "test 1",
        "options": [x for x in "abcdefg"],
        "multiple": True,
        "style": "width: 200px"
        }, {
        "label": "test 2",
        "options": list(range(1, 11)),
        "multiple": True,
        "style": "width: 200px"
        }, {
        "label": "test 3",
        "options": ["abc", "def", "ghi"],
        "multiple": False,
        "style": "width: 200px"
        }
    ]
    temp = MyFilter(a=wp, classes="q-pa-md q-gutter-sm", label="Filter", options=option_dict)
    print(temp.filter_list)
    return wp


jp.justpy(dialog_test)