import panel as pn
from panel.template import FastListTemplate

def build_template(page1, page2, page3, select_exp_id, select_stud):
    pages = {"Page 1": page1, "Page 2": page2, "Page 3": page3}
    main_area = pn.Column(pages["Page 1"].view())

    def show_page(page_instance):
        main_area.clear()
        main_area.append(page_instance.view())

    page1_button = pn.widgets.Button(name="General Information")
    page2_button = pn.widgets.Button(name="Group Information")
    page3_button = pn.widgets.Button(name="Competencies Information")

    page1_button.on_click(lambda _: show_page(pages["Page 1"]))
    page2_button.on_click(lambda _: show_page(pages["Page 2"]))
    page3_button.on_click(lambda _: show_page(pages["Page 3"]))

    template = FastListTemplate(
        title="LEDA",
        header=[page1_button, page2_button, page3_button],
        sidebar=[pn.Column(select_exp_id, select_stud)],
        main=[main_area],
    )
    return template
