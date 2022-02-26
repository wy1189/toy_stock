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


class QInputDate(jp.QInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mask = '####-##-##'
        date_slot = jp.QIcon(name='event', classes='cursor-pointer')
        c2 = jp.QPopupProxy(transition_show='scale', transition_hide='scale', a=date_slot)
        self.date = jp.QDate(mask='YYYY-MM-DD', name='date', a=c2, today_btn=True, range=True)

        self.date.parent = self
        self.date.value = self.value
        self.prepend_slot = date_slot
        self.date.on('input', self.date_time_change)
        self.on('input', self.input_change)

    @staticmethod
    def date_time_change(self, msg):
        print(self.value)
        self.parent.value = self.value
        self.parent.date.value = self.value

    @staticmethod
    def input_change(self, msg):
        self.date.value = self.value


class QDialogSelect(jp.QDiv):
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
        c4 = jp.QCardSection(classes="row justify-between bg-primary", a=c3)
        jp.QDiv(classes="text-h6 text-grey-1", text="Current Filters", a=c4)
        jp.QBtn(label="", icon="close", a=c4,
                color="grey-1", flat=True, round=False, v_close_popup=True)
        c5 = jp.QCardSection(a=c3, classes="q-gutter-sm col wrap justify-start items-start content-start", bordered=True)
        filter_options = kwargs.get("options", [["test 1", "test 2"]])
        self.filter_list = []
        for option in filter_options:
            c6 = jp.QDiv(classes="row justify-start q-ma-lg", a=c5)
            jp.QDiv(
                inner_html=option.get("inner_html", ""),
                classes=option.get("title_classes", ""),
                style=option.get("title_style", "")
            ).add_to(c6)

            jp.QSelect(
                classes="q-px-md w-1/4", outlined=True, square=True, fill_input=False,
                dense=True, clearable=False, use_input=False, item_aligned=True, options_dense=True,
                options=option.get("condition_options", []),
                label=option.get("condition_label", ""),
                style=option.get("condition_style", "width: 200px"),
                use_chips=False
            ).add_to(c6)

            jp.QSelect(
                classes="q-px-md w-1/4", outlined=True, square=True, fill_input=False,
                dense=True, clearable=True, use_input=False, item_aligned=True, options_dense=True,
                options=option.get("value_options", []),
                label=option.get("value_label", ""),
                multiple=option.get("value_multiple", False),
                style=option.get("value_style", "width: 200px"),
                hide_selected=option.get("value_hide_selected", False),
                use_chips=False
            ).add_to(c6)
            self.filter_list.append(c6)
            for select in c6[-1::1]:
                select.on("input", self.align_select)
            for select in c6[1:2]:
                select.on("input", self.show_select)
        self.c5 = c5

    @staticmethod
    def open_dialog(self, msg):
        self.dialog.value = True

    @staticmethod
    def align_select(self, msg):
        if isinstance(self.value, list):
            self.value = sorted(self.value)
            if self.components:
                self.remove_component(self.components[0])
            self.add(jp.QTooltip(text=", ".join(self.value), classes="text-h6"))

    @staticmethod
    def show_select(self, msg):
        print(self.value.value)


class CustomDate(jp.QDiv):
    def __init__(self, **kwargs):
        self.style = 'margin-bottom:25px'
        super().__init__(**kwargs)
        self.form = kwargs.get('form', None)
        self.field_name = kwargs.get('field_name', None)
        self.label = kwargs.get('label', None)
        self.hint = kwargs.get('hint', '')

        kwargs = {
            'filled': True,
            'label': self.label,
            'a': self,
            'model': [self.form, self.field_name],
            'value': ''
        }
        input = jp.QInput(
            **kwargs
        )
        icon1 = jp.QIcon(
            name='event',
            color='blue'
        )
        input.append_slot = icon1
        self.q_popup_proxy = jp.QPopupProxy(
            a=input,
            transition_show="scale",
            transition_hide="scale"
        )
        q_date = jp.QDate(
            mask='YYYY-MM-DD',
            name='date',
            a=self.q_popup_proxy,
            hint=self.hint
        )
        q_date.on('input', self.input_fn)

    async def input_fn(self, msg):
        self.form.data[self.field_name] = msg.target.value
        await self.q_popup_proxy.run_method('hide()', msg.websocket)


async def dialog_test():
    wp = jp.QuasarPage(tailwind=True)
    # QDialog(a=wp, classes="q-pa-md q-gutter-sm", label="Alert")
    numeric_conditions = [
        {"label": "is greater than", "value": "g"},
        {"label": "is greater than or equal to", "value": "geq"},
        {"label": "is equal to", "value": "equal"},
        {"label": "is not equal to", "value": "notequal"},
        {"label": "is less than", "value": "l"},
        {"label": "is less than or equal to", "value": "leq"}
    ]
    string_conditions = [
        {"label": "is equal to", "value": "equal"},
        {"label": "is not equal to", "value": "notequal"},
        {"label": "is like", "value": "like"},
        {"label": "is not like", "value": "notlike"}
    ]
    option_dict = [{
        "inner_html": "<span>Hotel <b>Company Name</b></span>",
        "title_classes": "w-1/4 text-right text-subtitle2",
        "title_style": "height: auto;",
        "condition_options": numeric_conditions,
        "condition_style": "width: 300px",
        "value_label": "Company",
        "value_options": ["Hotel A", "Hotel B", "Hotel C"],
        "value_style": "width: 200px",
        "value_hide_selected": False,
        "value_multiple": False
    }, {
        "inner_html": "<span>Hotel <b>Hotel Name</b></span>",
        "title_classes": "w-1/4 text-right text-subtitle2",
        "title_style": "height: auto;",
        "condition_options": string_conditions,
        "condition_style": "width: 300px",
        "value_label": "Hotel",
        "value_options": ["Hotel A", "Hotel B", "Hotel C"],
        "value_style": "width: 200px",
        "value_hide_selected": False,
        "value_multiple": False
    }, {
        "inner_html": "<span>Hotel <b>City</b></span>",
        "title_classes": "w-1/4 text-right text-subtitle2",
        "title_style": "height: auto;",
        "condition_options": numeric_conditions,
        "condition_style": "width: 300px",
        "value_label": "City",
        "value_options": ["Hotel A", "Hotel B", "Hotel C"],
        "value_style": "width: 200px",
        "value_hide_selected": False,
        "value_multiple": False
    }, {
        "inner_html": "<span>Hotel <b>Country</b></span>",
        "title_classes": "w-1/4 text-right text-subtitle2",
        "title_style": "height: auto;",
        "condition_options": string_conditions,
        "condition_style": "width: 300px",
        "value_label": "Country",
        "value_options": ["Hotel A", "Hotel B", "Hotel C"],
        "value_style": "width: 200px",
        "value_hide_selected": True,
        "value_multiple": True
    }, {
        "inner_html": "<span>Booking <b>Reporting Period</b></span>",
        "title_classes": "w-1/4 text-right text-subtitle2",
        "title_style": "height: auto;",
        "condition_options": [{"label": "Yearly", "value": "YEAR"},
                              {"label": "Quarterly", "value": "QUARTER"},
                              {"label": "Monthly", "value": "MONTH"},
                              {"label": "Weekly", "value": "WEEK"},
                              {"label": "Daily", "value": "DAY"}],
        "condition_style": "width: 300px",
        "value_label": "",
        "value_options": list(range(1, 13)),
        "value_style": "width: 200px",
        "value_hide_selected": False,
        "value_multiple": False
    }, {
        "inner_html": "<span>Booking <b>Stay Date</b></span>",
        "title_classes": "w-1/4 h-auto text-right text-subtitle2",
        # "title_style": "height: auto;",
        "condition_options": string_conditions,
        "condition_style": "width: 300px",
        "value_label": "",
        "value_options": ["a", "b", "c"],
        "value_style": "width: 200px",
        "value_hide_selected": True,
        "value_multiple": False
    }]
    temp = QDialogSelect(a=wp, classes="q-pa-md q-gutter-sm", label="Filter", options=option_dict)
    print(temp.filter_list)

    # f = jp.Form(data={'date': '2021-04-01'})
    # temp.c5.add(CustomDate(filled=True, classes="q-px-md w-1/4", value='2021-04-01 14:44',
    #                        form=f, field_name='date', label="Stay Date", hint="From"))
    temp.c5[-1].remove_component(temp.c5[-1][-1])
    # temp.c5[-1][-1].delete_components()
    # temp.c5[-1][-1] = []
    qdate = QInputDate(style="width: 200px", classes="q-px-md w-1/4", value='2022-02-01',
                       dense=True, outlined=True, square=True, filled=False)
    # temp.c5[-2][-1].add(jp.QTooltip(text=f'1 rating'))
    temp.c5[-1].add(qdate)
    # jp.QInput(a=wp, style="width:200px; height:1px;")

    return wp


jp.justpy(dialog_test, port=9000)