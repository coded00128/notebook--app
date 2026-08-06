import flet as ft
import json
import os
from datetime import datetime


def main(page: ft.Page):

    page.title = "My Notebook"
    page.padding = 0
    page.spacing = 0
    page.window.width = 400
    page.window.height = 750

    data_file = "notebook_data.json"

    tasks = []
    notes = []

    current_screen = "home"


    def load_data():

        nonlocal tasks, notes

        if os.path.exists(data_file):

            try:

                with open(
                    data_file,
                    "r",
                    encoding="utf-8"
                ) as file:

                    data = json.load(file)

                    tasks = data.get(
                        "tasks",
                        []
                    )

                    notes = data.get(
                        "notes",
                        []
                    )

            except:

                tasks = []
                notes = []


    def save_data():

        data = {
            "tasks": tasks,
            "notes": notes
        }

        with open(
            data_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )


    def get_time():

        return datetime.now().strftime(
            "%d %b %Y, %I:%M %p"
        )


    content = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO
    )


    def show_message(text):

        snack = ft.SnackBar(
            content=ft.Text(text)
        )

        page.overlay.append(snack)

        snack.open = True

        page.update()


    def go_home(e=None):

        nonlocal current_screen

        current_screen = "home"

        show_home()


    def show_home():

        content.controls.clear()

        content.controls.append(

            ft.Container(

                content=ft.Column(

                    controls=[

                        ft.Text(
                            "📓",
                            size=45
                        ),

                        ft.Text(
                            "MY NOTEBOOK",
                            size=28,
                            weight=ft.FontWeight.BOLD
                        ),

                        ft.Text(
                            "Write it. Save it. Remember it.",
                            size=14
                        )

                    ],

                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                    spacing=3

                ),

                padding=20

            )

        )


        content.controls.append(

            ft.Row(

                controls=[

                    ft.Container(

                        content=ft.Column(

                            controls=[

                                ft.Text(
                                    str(len(tasks)),
                                    size=25,
                                    weight=ft.FontWeight.BOLD
                                ),

                                ft.Text("Tasks")

                            ],

                            horizontal_alignment=ft.CrossAxisAlignment.CENTER

                        ),

                        padding=15,

                        expand=True,

                        border=ft.Border.all(1),

                        border_radius=12

                    ),

                    ft.Container(

                        content=ft.Column(

                            controls=[

                                ft.Text(
                                    str(len(notes)),
                                    size=25,
                                    weight=ft.FontWeight.BOLD
                                ),

                                ft.Text("Notes")

                            ],

                            horizontal_alignment=ft.CrossAxisAlignment.CENTER

                        ),

                        padding=15,

                        expand=True,

                        border=ft.Border.all(1),

                        border_radius=12

                    )

                ]

            )

        )


        content.controls.append(

            ft.Container(

                content=ft.Column(

                    controls=[

                        ft.Text(
                            "What would you like to do?",
                            size=19,
                            weight=ft.FontWeight.BOLD
                        ),

                        ft.Row(

                            controls=[

                                ft.ElevatedButton(

                                    "➕ Task",

                                    on_click=lambda e:
                                    show_create_task()

                                ),

                                ft.ElevatedButton(

                                    "📝 Note",

                                    on_click=lambda e:
                                    show_create_note()

                                )

                            ]

                        )

                    ]

                ),

                padding=20

            )

        )


        content.controls.append(

            ft.Text(

                "Recent activity",

                size=20,

                weight=ft.FontWeight.BOLD

            )

        )


        recent = []


        for task in tasks[:3]:

            recent.append(

                ft.Container(

                    content=ft.Text(

                        "✓ " + task["text"]

                    ),

                    padding=10,

                    border=ft.Border.all(1),

                    border_radius=10

                )

            )


        for note in notes[:3]:

            recent.append(

                ft.Container(

                    content=ft.Text(

                        "📖 " + note["text"]

                    ),

                    padding=10,

                    border=ft.Border.all(1),

                    border_radius=10

                )

            )


        if recent:

            content.controls.extend(recent)

        else:

            content.controls.append(

                ft.Text(

                    "Nothing here yet. Start writing!"

                )

            )


        page.update()


    def show_create_task(e=None):

        content.controls.clear()


        text_box = ft.TextField(

            label="Task",

            hint_text="What do you need to do?",

            multiline=True,

            min_lines=3,

            max_lines=6,

            border_radius=12

        )


        category_box = ft.Dropdown(

            label="Category",

            value="General",

            options=[

                ft.DropdownOption("General"),

                ft.DropdownOption("School"),

                ft.DropdownOption("Personal"),

                ft.DropdownOption("Work"),

                ft.DropdownOption("Ideas")

            ]

        )


        priority_box = ft.Dropdown(

            label="Priority",

            value="Medium",

            options=[

                ft.DropdownOption("High"),

                ft.DropdownOption("Medium"),

                ft.DropdownOption("Low")

            ]

        )


        def save_task(e):

            text = text_box.value.strip()


            if text == "":

                show_message(
                    "Please write a task first."
                )

                return


            tasks.insert(

                0,

                {

                    "text": text,

                    "completed": False,

                    "category": category_box.value,

                    "priority": priority_box.value,

                    "time": get_time()

                }

            )


            save_data()

            show_message("Task saved!")

            show_tasks()


        content.controls.extend([

            ft.Row(

                controls=[

                    ft.IconButton(

                        icon=ft.Icons.ARROW_BACK,

                        on_click=lambda e:
                        show_tasks()

                    ),

                    ft.Text(

                        "NEW TASK",

                        size=25,

                        weight=ft.FontWeight.BOLD

                    )

                ]

            ),

            text_box,

            category_box,

            priority_box,

            ft.ElevatedButton(

                "Save Task",

                icon=ft.Icons.SAVE,

                on_click=save_task

            )

        ])


        page.update()


    def show_create_note(e=None):

        content.controls.clear()


        text_box = ft.TextField(

            label="Note",

            hint_text="Write anything here...",

            multiline=True,

            min_lines=8,

            max_lines=15,

            border_radius=12

        )


        category_box = ft.Dropdown(

            label="Category",

            value="General",

            options=[

                ft.DropdownOption("General"),

                ft.DropdownOption("School"),

                ft.DropdownOption("Personal"),

                ft.DropdownOption("Work"),

                ft.DropdownOption("Ideas")

            ]

        )


        def save_note(e):

            text = text_box.value.strip()


            if text == "":

                show_message(
                    "Please write a note first."
                )

                return


            notes.insert(

                0,

                {

                    "text": text,

                    "category": category_box.value,

                    "time": get_time()

                }

            )


            save_data()

            show_message("Note saved!")

            show_notes()


        content.controls.extend([

            ft.Row(

                controls=[

                    ft.IconButton(

                        icon=ft.Icons.ARROW_BACK,

                        on_click=lambda e:
                        show_notes()

                    ),

                    ft.Text(

                        "NEW NOTE",

                        size=25,

                        weight=ft.FontWeight.BOLD

                    )

                ]

            ),

            text_box,

            category_box,

            ft.ElevatedButton(

                "Save Note",

                icon=ft.Icons.SAVE,

                on_click=save_note

            )

        ])


        page.update()


    def delete_confirm(

        title,

        message,

        action

    ):

        def cancel(e):

            dialog.open = False

            page.update()


        def confirm(e):

            dialog.open = False

            action()

            page.update()


        dialog = ft.AlertDialog(

            modal=True,

            title=ft.Text(title),

            content=ft.Text(message),

            actions=[

                ft.TextButton(

                    "Cancel",

                    on_click=cancel

                ),

                ft.ElevatedButton(

                    "Delete",

                    on_click=confirm

                )

            ]

        )


        page.overlay.append(dialog)

        dialog.open = True

        page.update()


    def show_tasks():

        nonlocal current_screen

        current_screen = "tasks"

        content.controls.clear()


        content.controls.append(

            ft.Row(

                controls=[

                    ft.Text(

                        "MY TASKS",

                        size=27,

                        weight=ft.FontWeight.BOLD,

                        expand=True

                    ),

                    ft.IconButton(

                        icon=ft.Icons.ADD,

                        on_click=show_create_task

                    )

                ]

            )

        )


        if not tasks:

            content.controls.append(

                ft.Text(

                    "No tasks yet."

                )

            )

        else:

            for number, task in enumerate(

                tasks,

                start=1

            ):

                make_task_card(

                    number,

                    task

                )


        page.update()


    def make_task_card(number, task):

        text = ft.Text(

            f"{number}. {task['text']}",

            size=17,

            expand=True

        )


        if task.get("completed", False):

            text.style = ft.TextStyle(

                decoration=
                ft.TextDecoration.LINE_THROUGH

            )


        def mark(e):

            task["completed"] = not task.get(

                "completed",

                False

            )

            save_data()

            show_tasks()


        def edit(e):

            edit_box = ft.TextField(

                value=task["text"],

                multiline=True,

                min_lines=3,

                max_lines=6

            )


            def save_edit(e):

                new_text = edit_box.value.strip()


                if new_text:

                    task["text"] = new_text

                    save_data()

                    dialog.open = False

                    page.update()

                    show_tasks()


            def close(e):

                dialog.open = False

                page.update()


            dialog = ft.AlertDialog(

                modal=True,

                title=ft.Text(
                    "Edit Task"
                ),

                content=edit_box,

                actions=[

                    ft.TextButton(

                        "Cancel",

                        on_click=close

                    ),

                    ft.ElevatedButton(

                        "Save",

                        on_click=save_edit

                    )

                ]

            )


            page.overlay.append(dialog)

            dialog.open = True

            page.update()


        def delete(e):

            def remove():

                tasks.remove(task)

                save_data()

                show_tasks()


            delete_confirm(

                "Delete Task?",

                "This task will be permanently deleted.",

                remove

            )


        priority = task.get(

            "priority",

            "Medium"

        )


        category = task.get(

            "category",

            "General"

        )


        time = task.get(

            "time",

            ""

        )


        card = ft.Container(

            content=ft.Column(

                controls=[

                    ft.Row(

                        controls=[

                            text

                        ]

                    ),

                    ft.Text(

                        f"{category} • {priority}",

                        size=12

                    ),

                    ft.Text(

                        time,

                        size=11

                    ),

                    ft.Row(

                        controls=[

                            ft.IconButton(

                                icon=ft.Icons.CHECK_CIRCLE_OUTLINE,

                                tooltip="Complete",

                                on_click=mark

                            ),

                            ft.IconButton(

                                icon=ft.Icons.EDIT,

                                tooltip="Edit",

                                on_click=edit

                            ),

                            ft.IconButton(

                                icon=ft.Icons.DELETE,

                                tooltip="Delete",

                                on_click=delete

                            )

                        ]

                    )

                ]

            ),

            padding=12,

            border=ft.Border.all(1),

            border_radius=12

        )


        content.controls.append(card)


    def show_notes():

        nonlocal current_screen
        current_screen = "notes"

        content.controls.clear()


        content.controls.append(

            ft.Row(

                controls=[

                    ft.Text(

                        "MY NOTES",

                        size=27,

                        weight=ft.FontWeight.BOLD,

                        expand=True

                    ),

                    ft.IconButton(

                        icon=ft.Icons.ADD,

                        on_click=show_create_note

                    )

                ]

            )

        )


        if not notes:

            content.controls.append(

                ft.Text(

                    "No notes yet."

                )

            )

        else:

            for number, note in enumerate(

                notes,

                start=1

            ):

                make_note_card(

                    number,

                    note

                )


        page.update()


    def make_note_card(number, note):

        text = ft.Text(

            f"{number}. {note['text']}",

            size=17,

            expand=True

        )


        def edit(e):

            edit_box = ft.TextField(

                value=note["text"],

                multiline=True,

                min_lines=5,

                max_lines=10

            )


            def save_edit(e):

                new_text = edit_box.value.strip()


                if new_text:

                    note["text"] = new_text

                    save_data()

                    dialog.open = False

                    page.update()

                    show_notes()


            def close(e):

                dialog.open = False

                page.update()


            dialog = ft.AlertDialog(

                modal=True,

                title=ft.Text(
                    "Edit Note"
                ),

                content=edit_box,

                actions=[

                    ft.TextButton(

                        "Cancel",

                        on_click=close

                    ),

                    ft.ElevatedButton(

                        "Save",

                        on_click=save_edit

                    )

                ]

            )


            page.overlay.append(dialog)

            dialog.open = True

            page.update()


        def delete(e):

            def remove():

                notes.remove(note)

                save_data()

                show_notes()


            delete_confirm(

                "Delete Note?",

                "This note will be permanently deleted.",

                remove

            )


        category = note.get(

            "category",

            "General"

        )


        time = note.get(

            "time",

            ""

        )


        card = ft.Container(

            content=ft.Column(

                controls=[

                    text,

                    ft.Text(

                        category,

                        size=12

                    ),

                    ft.Text(

                        time,

                        size=11

                    ),

                    ft.Row(

                        controls=[

                            ft.IconButton(

                                icon=ft.Icons.EDIT,

                                tooltip="Edit",

                                on_click=edit

                            ),

                            ft.IconButton(

                                icon=ft.Icons.DELETE,

                                tooltip="Delete",

                                on_click=delete

                            )

                        ]

                    )

                ]

            ),

            padding=12,

            border=ft.Border.all(1),

            border_radius=12

        )


        content.controls.append(card)


    def show_search():

        content.controls.clear()


        search = ft.TextField(

            hint_text="Search your notebook...",

            prefix_icon=ft.Icons.SEARCH,

            border_radius=12

        )


        results = ft.Column(

            spacing=10

        )


        def perform_search(e):

            results.controls.clear()

            query = search.value.lower().strip()


            if not query:

                page.update()

                return


            found = False


            for number, task in enumerate(

                tasks,

                start=1

            ):

                if query in task["text"].lower():

                    found = True

                    results.controls.append(

                        ft.Container(

                            content=ft.Text(

                                f"✓ Task {number}: "
                                f"{task['text']}"

                            ),

                            padding=12,

                            border=ft.Border.all(1),

                            border_radius=10

                        )

                    )


            for number, note in enumerate(

                notes,

                start=1

            ):

                if query in note["text"].lower():

                    found = True

                    results.controls.append(

                        ft.Container(

                            content=ft.Text(

                                f"📖 Note {number}: "
                                f"{note['text']}"

                            ),

                            padding=12,

                            border=ft.Border.all(1),

                            border_radius=10

                        )

                    )


            if not found:

                results.controls.append(

                    ft.Text(

                        "Nothing found."

                    )

                )


            page.update()


        search.on_change = perform_search


        content.controls.extend([

            ft.Text(

                "SEARCH",

                size=27,

                weight=ft.FontWeight.BOLD

            ),

            search,

            results

        ])


        page.update()


    def show_settings():

        content.controls.clear()


        theme_switch = ft.Switch(

            label="Dark mode",

            value=page.theme_mode == ft.ThemeMode.DARK

        )


        def change_theme(e):

            if theme_switch.value:

                page.theme_mode = ft.ThemeMode.DARK

            else:

                page.theme_mode = ft.ThemeMode.LIGHT

            page.update()


        theme_switch.on_change = change_theme


        def clear_all(e):

            def remove_all():

                tasks.clear()

                notes.clear()

                save_data()

                show_home()


            delete_confirm(

                "Clear Everything?",

                "All tasks and notes will be permanently deleted.",

                remove_all

            )


        content.controls.extend([

            ft.Text(

                "SETTINGS",

                size=27,

                weight=ft.FontWeight.BOLD

            ),

            ft.Container(

                content=theme_switch,

                padding=10,

                border=ft.Border.all(1),

                border_radius=12

            ),

            ft.Divider(),

            ft.Text(

                "Storage",

                size=18,

                weight=ft.FontWeight.BOLD

            ),

            ft.Text(

                f"{len(tasks)} tasks • "
                f"{len(notes)} notes"

            ),

            ft.ElevatedButton(

                "Clear All Data",

                icon=ft.Icons.DELETE_FOREVER,

                on_click=clear_all

            )

        ])


        page.update()


    def navigation_change(e):

        index = e.control.selected_index


        if index == 0:

            show_home()

        elif index == 1:

            show_tasks()

        elif index == 2:

            show_notes()

        elif index == 3:

            show_search()

        elif index == 4:

            show_settings()


    navigation = ft.NavigationBar(

        selected_index=0,

        on_change=navigation_change,

        destinations=[

            ft.NavigationBarDestination(

                icon=ft.Icons.HOME_OUTLINED,

                selected_icon=ft.Icons.HOME,

                label="Home"

            ),

            ft.NavigationBarDestination(

                icon=ft.Icons.CHECK_BOX_OUTLINED,

                selected_icon=ft.Icons.CHECK_BOX,

                label="Tasks"

            ),

            ft.NavigationBarDestination(

                icon=ft.Icons.BOOK_OUTLINED,

                selected_icon=ft.Icons.BOOK,

                label="Notes"

            ),

            ft.NavigationBarDestination(

                icon=ft.Icons.SEARCH,

                label="Search"

            ),

            ft.NavigationBarDestination(

                icon=ft.Icons.SETTINGS_OUTLINED,

                selected_icon=ft.Icons.SETTINGS,

                label="Settings"

            )

        ]

    )


    load_data()

    page.add(

        content,

        navigation

    )

    show_home()


ft.run(main)