import flet as ft
import json
import os
from datetime import datetime, timedelta

from flet_android_notifications import FletAndroidNotifications


def main(page: ft.Page):
    page.title = "My Notebook"
    page.padding = 0
    page.spacing = 0
    page.bgcolor = "#F7F7FB"

    data_file = "notebook_data.json"

    tasks = []
    notes = []
    user_name = ""

    notifications = FletAndroidNotifications()

    RED = "#E63946"
    RED_DARK = "#C92F3B"
    RED_LIGHT = "#FFF0F1"
    PINK_LIGHT = "#FFE8EA"
    WHITE = "#FFFFFF"
    BACKGROUND = "#F7F7FB"
    TEXT = "#202124"
    GREY = "#777777"
    LIGHT_GREY = "#E8E8EF"
    BLUE_LIGHT = "#F0F3FF"
    YELLOW_LIGHT = "#FFF7E8"

    content = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        spacing=0
    )

    def load_data():
        nonlocal tasks, notes, user_name

        if not os.path.exists(data_file):
            return

        try:
            with open(data_file, "r", encoding="utf-8") as file:
                data = json.load(file)

            tasks = data.get("tasks", [])
            notes = data.get("notes", [])
            user_name = data.get("user_name", "")

        except Exception:
            tasks = []
            notes = []
            user_name = ""

    def save_data():
        data = {
            "user_name": user_name,
            "tasks": tasks,
            "notes": notes
        }

        try:
            with open(data_file, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
        except Exception as error:
            print("Could not save data:", error)

    def get_time():
        return datetime.now().strftime("%d %b %Y, %I:%M %p")

    def show_message(message):
        try:
            page.show_dialog(
                ft.SnackBar(
                    content=ft.Text(message)
                )
            )
        except Exception:
            print(message)

    def section_title(title, subtitle=None):
        controls = [
            ft.Text(
                title,
                size=27,
                weight=ft.FontWeight.BOLD,
                color=TEXT
            )
        ]

        if subtitle:
            controls.append(
                ft.Text(
                    subtitle,
                    size=13,
                    color=GREY
                )
            )

        return ft.Column(
            controls=controls,
            spacing=3
        )

    def make_card(child, padding=16, color=WHITE):
        return ft.Container(
            content=child,
            padding=padding,
            margin=ft.Margin(bottom=10),
            bgcolor=color,
            border_radius=18,
            border=ft.Border.all(1, LIGHT_GREY),
            width=float("inf")
        )

    def ask_name():
        name_box = ft.TextField(
            label="Your name",
            hint_text="Enter your name",
            autofocus=True,
            border_radius=14
        )

        def save_name(e):
            nonlocal user_name

            name = (name_box.value or "").strip()

            if not name:
                show_message("Please enter your name.")
                return

            user_name = name
            save_data()

            dialog.open = False
            page.update()

            show_home()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                "Welcome to My Notebook 👋",
                weight=ft.FontWeight.BOLD
            ),
            content=ft.Column(
                controls=[
                    ft.Text("Let's personalize your notebook."),
                    name_box
                ],
                tight=True,
                spacing=12
            ),
            actions=[
                ft.Button(
                    content=ft.Text("Continue"),
                    bgcolor=RED,
                    color=WHITE,
                    on_click=save_name
                )
            ]
        )

        page.show_dialog(dialog)

    def show_home():
        content.controls.clear()

        greeting = user_name if user_name else "there"

        header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text("📓", size=30),
                        width=58,
                        height=58,
                        alignment=ft.Alignment.CENTER,
                        bgcolor=PINK_LIGHT,
                        border_radius=18
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                f"Hello, {greeting} 👋",
                                size=22,
                                weight=ft.FontWeight.BOLD,
                                color=TEXT
                            ),
                            ft.Text(
                                "Ready to get things done?",
                                size=13,
                                color=GREY
                            )
                        ],
                        spacing=2,
                        expand=True
                    ),
                    ft.Container(
                        content=ft.IconButton(
                            icon=ft.Icons.SETTINGS_OUTLINED,
                            icon_color=TEXT,
                            on_click=lambda e: show_settings()
                        ),
                        bgcolor=WHITE,
                        border_radius=15
                    )
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=18
        )

        content.controls.append(header)

        task_stat = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        str(len(tasks)),
                        size=29,
                        weight=ft.FontWeight.BOLD,
                        color=RED
                    ),
                    ft.Text(
                        "Tasks",
                        size=13,
                        color=GREY
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2
            ),
            expand=True,
            padding=18,
            bgcolor=RED_LIGHT,
            border_radius=18
        )

        note_stat = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        str(len(notes)),
                        size=29,
                        weight=ft.FontWeight.BOLD,
                        color="#5969D9"
                    ),
                    ft.Text(
                        "Notes",
                        size=13,
                        color=GREY
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2
            ),
            expand=True,
            padding=18,
            bgcolor=BLUE_LIGHT,
            border_radius=18
        )

        content.controls.append(
            ft.Container(
                content=ft.Row(
                    controls=[
                        task_stat,
                        note_stat
                    ],
                    spacing=12
                ),
                padding=18
            )
        )

        content.controls.append(
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "Quick actions",
                            size=19,
                            weight=ft.FontWeight.BOLD,
                            color=TEXT
                        ),
                        ft.Row(
                            controls=[
                                ft.Container(
                                    content=ft.Button(
                                        content=ft.Text("➕  Task"),
                                        expand=True,
                                        bgcolor=RED,
                                        color=WHITE,
                                        height=48,
                                        on_click=show_create_task
                                    ),
                                    expand=True
                                ),
                                ft.Container(
                                    content=ft.Button(
                                        content=ft.Text("📝  Note"),
                                        expand=True,
                                        bgcolor=WHITE,
                                        color=TEXT,
                                        height=48,
                                        on_click=show_create_note
                                    ),
                                    expand=True
                                )
                            ],
                            spacing=10
                        )
                    ],
                    spacing=12
                ),
                padding=18
            )
        )

        recent_controls = [
            ft.Text(
                "Recent activity",
                size=19,
                weight=ft.FontWeight.BOLD,
                color=TEXT
            )
        ]

        recent_items = []

        for task in tasks[:3]:
            recent_items.append(
                make_card(
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Icon(
                                    ft.Icons.CHECK,
                                    color=WHITE,
                                    size=17
                                ),
                                width=32,
                                height=32,
                                alignment=ft.Alignment.CENTER,
                                bgcolor=RED,
                                border_radius=10
                            ),
                            ft.Text(
                                task.get("text", ""),
                                size=15,
                                expand=True,
                                max_lines=2,
                                overflow=ft.TextOverflow.ELLIPSIS
                            )
                        ],
                        spacing=10
                    ),
                    padding=12
                )
            )

        for note in notes[:3]:
            recent_items.append(
                make_card(
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Text("📝", size=17),
                                width=32,
                                height=32,
                                alignment=ft.Alignment.CENTER,
                                bgcolor=BLUE_LIGHT,
                                border_radius=10
                            ),
                            ft.Text(
                                note.get("text", ""),
                                size=15,
                                expand=True,
                                max_lines=2,
                                overflow=ft.TextOverflow.ELLIPSIS
                            )
                        ],
                        spacing=10
                    ),
                    padding=12
                )
            )

        if recent_items:
            recent_controls.extend(recent_items)
        else:
            recent_controls.append(
                ft.Text(
                    "Nothing here yet. Start writing!",
                    color=GREY
                )
            )

        content.controls.append(
            ft.Container(
                content=ft.Column(
                    controls=recent_controls,
                    spacing=5
                ),
                padding=18
            )
        )

        page.update()

    def choose_reminder(task, after_save=None):
        current_reminder = task.get("reminder")
        selected_datetime = None

        if current_reminder:
            try:
                selected_datetime = datetime.fromisoformat(
                    current_reminder
                )
            except Exception:
                selected_datetime = None

        def open_date_picker(e):
            today = datetime.now()

            def date_changed(ev):
                nonlocal selected_datetime

                value = date_picker.value

                if value:
                    if isinstance(value, datetime):
                        selected_date = value.date()
                    else:
                        selected_date = value

                    if selected_datetime:
                        selected_time = selected_datetime.time()
                    else:
                        selected_time = datetime.now().time()

                    selected_datetime = datetime(
                        selected_date.year,
                        selected_date.month,
                        selected_date.day,
                        selected_time.hour,
                        selected_time.minute
                    )

                    refresh_text()

            date_picker = ft.DatePicker(
                current_date=today,
                first_date=today,
                last_date=datetime(
                    today.year + 5,
                    12,
                    31
                ),
                on_change=date_changed
            )

            page.show_dialog(date_picker)

        def open_time_picker(e):
            def time_changed(ev):
                nonlocal selected_datetime

                value = time_picker.value

                if value:
                    base_date = (
                        selected_datetime.date()
                        if selected_datetime
                        else datetime.now().date()
                    )

                    selected_datetime = datetime(
                        base_date.year,
                        base_date.month,
                        base_date.day,
                        value.hour,
                        value.minute
                    )

                    refresh_text()

            time_picker = ft.TimePicker(
                on_change=time_changed
            )

            page.show_dialog(time_picker)

        async def save_reminder(e):
            if selected_datetime is None:
                show_message("Choose a date and time first.")
                return

            minimum_time = datetime.now() + timedelta(minutes=3)

            if selected_datetime < minimum_time:
                show_message(
                    "Please choose a time at least 3 minutes from now."
                )
                return

            try:
                await notifications.request_permissions()
            except Exception:
                pass

            try:
                exact_allowed = (
                    await notifications.request_exact_alarm_permission()
                )
            except Exception:
                exact_allowed = False

            notification_id = int(
                datetime.now().timestamp() * 1000
            ) % 2147480000

            try:
                await notifications.schedule_notification(
                    notification_id=notification_id,
                    title="📓 My Notebook Reminder",
                    body=task.get(
                        "text",
                        "You have a task."
                    ),
                    scheduled_time=selected_datetime,
                    importance="high",
                    play_sound=True,
                    enable_vibration=True,
                    schedule_mode=(
                        "exact_allow_while_idle"
                        if exact_allowed
                        else "inexact_allow_while_idle"
                    ),
                    payload=str(notification_id)
                )

                task["reminder"] = selected_datetime.isoformat()
                task["notification_id"] = notification_id

                save_data()

                dialog.open = False
                page.update()

                show_message("🔔 Reminder set successfully!")

                if after_save:
                    after_save()

            except Exception as error:
                task["reminder"] = selected_datetime.isoformat()
                task["notification_id"] = None

                save_data()

                dialog.open = False
                page.update()

                show_message(
                    "Reminder saved, but notification scheduling failed. "
                    "Test notifications on Android."
                )

                print("Notification error:", error)

                if after_save:
                    after_save()

        async def remove_reminder(e):
            notification_id = task.get("notification_id")

            if notification_id:
                try:
                    await notifications.cancel(
                        int(notification_id)
                    )
                except Exception:
                    pass

            task["reminder"] = None
            task["notification_id"] = None

            save_data()

            dialog.open = False
            page.update()

            if after_save:
                after_save()

        current_text = ft.Text(
            (
                selected_datetime.strftime(
                    "%d %b %Y • %I:%M %p"
                )
                if selected_datetime
                else "No reminder selected"
            ),
            size=14,
            color=GREY
        )

        def refresh_text():
            current_text.value = (
                selected_datetime.strftime(
                    "%d %b %Y • %I:%M %p"
                )
                if selected_datetime
                else "No reminder selected"
            )

            page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                controls=[
                    ft.Icon(
                        ft.Icons.NOTIFICATIONS_ACTIVE,
                        color=RED
                    ),
                    ft.Text(
                        "Task Reminder",
                        weight=ft.FontWeight.BOLD
                    )
                ]
            ),
            content=ft.Column(
                controls=[
                    current_text,
                    ft.Row(
                        controls=[
                            ft.Button(
                                content=ft.Text("Date"),
                                icon=ft.Icons.CALENDAR_MONTH,
                                on_click=open_date_picker,
                                expand=True
                            ),
                            ft.Button(
                                content=ft.Text("Time"),
                                icon=ft.Icons.ACCESS_TIME,
                                on_click=open_time_picker,
                                expand=True
                            )
                        ],
                        spacing=8
                    )
                ],
                tight=True,
                spacing=14
            ),
            actions=[
                ft.TextButton(
                    "Remove",
                    on_click=remove_reminder
                ),
                ft.Button(
                    content=ft.Text("Save Reminder"),
                    bgcolor=RED,
                    color=WHITE,
                    on_click=save_reminder
                )
            ]
        )

        page.show_dialog(dialog)

    def show_create_task(e=None):
        content.controls.clear()

        text_box = ft.TextField(
            label="Task",
            hint_text="What do you need to do?",
            multiline=True,
            min_lines=3,
            max_lines=6,
            border_radius=14
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

        reminder_data = {
            "datetime": None
        }

        reminder_label = ft.Text(
            "No reminder set",
            size=13,
            color=GREY
        )

        def update_reminder_label():
            selected = reminder_data["datetime"]

            if selected:
                reminder_label.value = (
                    "🔔 "
                    + selected.strftime(
                        "%d %b %Y • %I:%M %p"
                    )
                )
            else:
                reminder_label.value = "No reminder set"

            page.update()

        def choose_date(e):
            today = datetime.now()

            def changed(ev):
                value = date_picker.value

                if value:
                    if isinstance(value, datetime):
                        chosen = value.date()
                    else:
                        chosen = value

                    current = reminder_data["datetime"]

                    if current:
                        selected_time = current.time()
                    else:
                        selected_time = datetime.now().time()

                    reminder_data["datetime"] = datetime(
                        chosen.year,
                        chosen.month,
                        chosen.day,
                        selected_time.hour,
                        selected_time.minute
                    )

                    update_reminder_label()

            date_picker = ft.DatePicker(
                current_date=today,
                first_date=today,
                last_date=datetime(
                    today.year + 5,
                    12,
                    31
                ),
                on_change=changed
            )

            page.show_dialog(date_picker)

        def choose_time(e):
            def changed(ev):
                value = time_picker.value

                if value:
                    current = reminder_data["datetime"]

                    if current:
                        selected_date = current.date()
                    else:
                        selected_date = datetime.now().date()

                    reminder_data["datetime"] = datetime(
                        selected_date.year,
                        selected_date.month,
                        selected_date.day,
                        value.hour,
                        value.minute
                    )

                    update_reminder_label()

            time_picker = ft.TimePicker(
                on_change=changed
            )

            page.show_dialog(time_picker)

        def clear_reminder(e):
            reminder_data["datetime"] = None
            update_reminder_label()

        async def save_task(e):
            text = (text_box.value or "").strip()

            if not text:
                show_message("Please write a task first.")
                return

            reminder_dt = reminder_data["datetime"]

            if reminder_dt:
                minimum_time = datetime.now() + timedelta(minutes=3)

                if reminder_dt < minimum_time:
                    show_message(
                        "Please choose a time at least 3 minutes from now."
                    )
                    return

            task = {
                "text": text,
                "completed": False,
                "category": category_box.value or "General",
                "priority": priority_box.value or "Medium",
                "time": get_time(),
                "reminder": (
                    reminder_dt.isoformat()
                    if reminder_dt
                    else None
                ),
                "notification_id": None
            }

            tasks.insert(0, task)

            if reminder_dt:
                try:
                    await notifications.request_permissions()
                except Exception:
                    pass

                try:
                    exact_allowed = (
                        await notifications.request_exact_alarm_permission()
                    )
                except Exception:
                    exact_allowed = False

                notification_id = int(
                    datetime.now().timestamp() * 1000
                ) % 2147480000

                try:
                    await notifications.schedule_notification(
                        notification_id=notification_id,
                        title="📓 My Notebook Reminder",
                        body=text,
                        scheduled_time=reminder_dt,
                        importance="high",
                        play_sound=True,
                        enable_vibration=True,
                        schedule_mode=(
                            "exact_allow_while_idle"
                            if exact_allowed
                            else "inexact_allow_while_idle"
                        ),
                        payload=str(notification_id)
                    )

                    task["notification_id"] = notification_id

                except Exception as error:
                    task["reminder"] = None
                    task["notification_id"] = None

                    print(
                        "Notification scheduling error:",
                        error
                    )

                    save_data()
                    show_tasks()

                    show_message(
                        "Task saved, but notification scheduling failed. "
                        "Test the reminder on Android."
                    )

                    return

            save_data()
            show_tasks()

        content.controls.extend([
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            on_click=lambda e: show_tasks()
                        ),
                        ft.Text(
                            "NEW TASK",
                            size=25,
                            weight=ft.FontWeight.BOLD
                        )
                    ]
                ),
                padding=15
            ),
            ft.Container(
                content=ft.Column(
                    controls=[
                        text_box,
                        category_box,
                        priority_box,
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Container(
                                                content=ft.Icon(
                                                    ft.Icons.NOTIFICATIONS_ACTIVE,
                                                    color=RED
                                                ),
                                                width=42,
                                                height=42,
                                                alignment=ft.Alignment.CENTER,
                                                bgcolor=PINK_LIGHT,
                                                border_radius=13
                                            ),
                                            ft.Column(
                                                controls=[
                                                    ft.Text(
                                                        "Reminder",
                                                        size=17,
                                                        weight=ft.FontWeight.BOLD
                                                    ),
                                                    reminder_label
                                                ],
                                                spacing=2,
                                                expand=True
                                            )
                                        ],
                                        spacing=10
                                    ),
                                    ft.Row(
                                        controls=[
                                            ft.Button(
                                                content=ft.Text("Choose date"),
                                                icon=ft.Icons.CALENDAR_MONTH,
                                                on_click=choose_date,
                                                expand=True
                                            ),
                                            ft.Button(
                                                content=ft.Text("Choose time"),
                                                icon=ft.Icons.ACCESS_TIME,
                                                on_click=choose_time,
                                                expand=True
                                            )
                                        ],
                                        spacing=8
                                    ),
                                    ft.TextButton(
                                        "Remove reminder",
                                        on_click=clear_reminder
                                    )
                                ],
                                spacing=10
                            ),
                            padding=16,
                            bgcolor="#FFF4F5",
                            border_radius=18,
                            border=ft.Border.all(
                                1,
                                "#FFE0E3"
                            )
                        ),
                        ft.Button(
                            content=ft.Text("Save Task"),
                            icon=ft.Icons.SAVE,
                            height=52,
                            bgcolor=RED,
                            color=WHITE,
                            on_click=save_task
                        )
                    ],
                    spacing=14
                ),
                padding=18
            )
        ])

        page.update()

    def delete_confirm(title, message, action):
        def cancel(e):
            dialog.open = False
            page.update()

        def confirm(e):
            dialog.open = False
            page.update()
            action()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                title,
                weight=ft.FontWeight.BOLD
            ),
            content=ft.Text(message),
            actions=[
                ft.TextButton(
                    "Cancel",
                    on_click=cancel
                ),
                ft.Button(
                    content=ft.Text("Delete"),
                    bgcolor=RED,
                    color=WHITE,
                    on_click=confirm
                )
            ]
        )

        page.show_dialog(dialog)

    def make_task_card(number, task):
        completed = task.get("completed", False)
        reminder = task.get("reminder")

        task_text = ft.Text(
            f"{number}. {task.get('text', '')}",
            size=16,
            expand=True,
            max_lines=5,
            overflow=ft.TextOverflow.ELLIPSIS
        )

        if completed:
            task_text.style = ft.TextStyle(
                decoration=ft.TextDecoration.LINE_THROUGH,
                color="#999999"
            )

        def mark(e):
            task["completed"] = not task.get(
                "completed",
                False
            )

            save_data()
            show_tasks()

        def edit():
            edit_box = ft.TextField(
                value=task.get("text", ""),
                multiline=True,
                min_lines=3,
                max_lines=6,
                border_radius=14
            )

            def save_edit(e):
                new_text = (edit_box.value or "").strip()

                if not new_text:
                    show_message("Task cannot be empty.")
                    return

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
                title=ft.Text("Edit Task"),
                content=edit_box,
                actions=[
                    ft.TextButton(
                        "Cancel",
                        on_click=close
                    ),
                    ft.Button(
                        content=ft.Text("Save"),
                        bgcolor=RED,
                        color=WHITE,
                        on_click=save_edit
                    )
                ]
            )

            page.show_dialog(dialog)

        async def actually_delete():
            notification_id = task.get("notification_id")

            if notification_id:
                try:
                    await notifications.cancel(
                        int(notification_id)
                    )
                except Exception:
                    pass

            if task in tasks:
                tasks.remove(task)

            save_data()
            show_tasks()

        def delete():
            def run_delete():
                page.run_task(actually_delete)

            delete_confirm(
                "Delete Task?",
                "This task will be permanently deleted.",
                run_delete
            )

        gesture_text = ft.GestureDetector(
            content=task_text,
            on_double_tap=lambda e: edit(),
            on_long_press=lambda e: delete()
        )

        def reminder_button(e):
            choose_reminder(
                task,
                after_save=show_tasks
            )

        notification_button = ft.Container(
            content=ft.IconButton(
                icon=(
                    ft.Icons.NOTIFICATIONS_ACTIVE
                    if reminder
                    else ft.Icons.NOTIFICATIONS_NONE_OUTLINED
                ),
                icon_color=(
                    RED
                    if reminder
                    else GREY
                ),
                icon_size=22,
                tooltip=(
                    "Change reminder"
                    if reminder
                    else "Set reminder"
                ),
                on_click=reminder_button
            ),
            width=45,
            height=45,
            alignment=ft.Alignment.CENTER,
            bgcolor=(
                PINK_LIGHT
                if reminder
                else "#F2F2F5"
            ),
            border_radius=14
        )

        reminder_label = None

        if reminder:
            try:
                reminder_dt = datetime.fromisoformat(
                    reminder
                )

                reminder_label = ft.Row(
                    controls=[
                        ft.Icon(
                            ft.Icons.ACCESS_TIME,
                            size=14,
                            color=RED
                        ),
                        ft.Text(
                            reminder_dt.strftime(
                                "%d %b • %I:%M %p"
                            ),
                            size=11,
                            color=GREY
                        )
                    ],
                    spacing=4
                )

            except Exception:
                reminder_label = None

        details = [
            ft.Text(
                f"{task.get('category', 'General')} • "
                f"{task.get('priority', 'Medium')}",
                size=11,
                color=GREY
            ),
            ft.Text(
                task.get("time", ""),
                size=10,
                color="#999999"
            )
        ]

        if reminder_label:
            details.append(reminder_label)

        task_body = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        gesture_text,
                        ft.IconButton(
                            icon=(
                                ft.Icons.CHECK_CIRCLE
                                if completed
                                else ft.Icons.CHECK_CIRCLE_OUTLINE
                            ),
                            icon_color=(
                                RED
                                if completed
                                else GREY
                            ),
                            tooltip="Mark complete",
                            on_click=mark
                        )
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.START
                ),
                *details
            ],
            spacing=5,
            expand=True
        )

        card = ft.Container(
            content=ft.Row(
                controls=[
                    notification_button,
                    task_body
                ],
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.START
            ),
            padding=13,
            margin=ft.Margin(bottom=10),
            bgcolor=WHITE,
            border_radius=18,
            border=ft.Border.all(
                1,
                LIGHT_GREY
            ),
            width=float("inf")
        )

        content.controls.append(card)

    def show_tasks():
        content.controls.clear()

        content.controls.append(
            ft.Container(
                content=ft.Row(
                    controls=[
                        section_title(
                            "My Tasks",
                            f"{len(tasks)} saved task(s)"
                        ),
                        ft.Container(
                            content=ft.IconButton(
                                icon=ft.Icons.ADD,
                                icon_color=WHITE,
                                icon_size=25,
                                on_click=show_create_task
                            ),
                            width=48,
                            height=48,
                            alignment=ft.Alignment.CENTER,
                            bgcolor=RED,
                            border_radius=15
                        )
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=18
            )
        )

        if not tasks:
            content.controls.append(
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(
                                content=ft.Icon(
                                    ft.Icons.CHECKLIST,
                                    size=45,
                                    color=RED
                                ),
                                width=80,
                                height=80,
                                alignment=ft.Alignment.CENTER,
                                bgcolor=RED_LIGHT,
                                border_radius=25
                            ),
                            ft.Text(
                                "No tasks yet",
                                size=20,
                                weight=ft.FontWeight.BOLD
                            ),
                            ft.Text(
                                "Tap + to add your first task.",
                                color=GREY
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=8
                    ),
                    padding=40,
                    alignment=ft.Alignment.CENTER
                )
            )
        else:
            for number, task in enumerate(tasks, start=1):
                make_task_card(number, task)

        page.update()

    def show_create_note(e=None):
        content.controls.clear()

        text_box = ft.TextField(
            label="Note",
            hint_text="Write anything here...",
            multiline=True,
            min_lines=8,
            max_lines=15,
            border_radius=14
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
            text = (text_box.value or "").strip()

            if not text:
                show_message("Please write a note first.")
                return

            notes.insert(
                0,
                {
                    "text": text,
                    "category": category_box.value or "General",
                    "time": get_time()
                }
            )

            save_data()
            show_notes()

        content.controls.extend([
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            on_click=lambda e: show_notes()
                        ),
                        ft.Text(
                            "NEW NOTE",
                            size=25,
                            weight=ft.FontWeight.BOLD
                        )
                    ]
                ),
                padding=15
            ),
            ft.Container(
                content=ft.Column(
                    controls=[
                        text_box,
                        category_box,
                        ft.Button(
                            content=ft.Text("Save Note"),
                            icon=ft.Icons.SAVE,
                            height=52,
                            bgcolor=RED,
                            color=WHITE,
                            on_click=save_note
                        )
                    ],
                    spacing=14
                ),
                padding=18
            )
        ])

        page.update()

    def make_note_card(number, note):
        text = ft.Text(
            f"{number}. {note.get('text', '')}",
            size=16,
            expand=True,
            max_lines=7,
            overflow=ft.TextOverflow.ELLIPSIS
        )

        def edit():
            edit_box = ft.TextField(
                value=note.get("text", ""),
                multiline=True,
                min_lines=5,
                max_lines=10,
                border_radius=14
            )

            def save_edit(e):
                new_text = (edit_box.value or "").strip()

                if not new_text:
                    show_message("Note cannot be empty.")
                    return

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
                title=ft.Text("Edit Note"),
                content=edit_box,
                actions=[
                    ft.TextButton(
                        "Cancel",
                        on_click=close
                    ),
                    ft.Button(
                        content=ft.Text("Save"),
                        bgcolor=RED,
                        color=WHITE,
                        on_click=save_edit
                    )
                ]
            )

            page.show_dialog(dialog)

        def delete():
            def remove():
                if note in notes:
                    notes.remove(note)

                save_data()
                show_notes()

            delete_confirm(
                "Delete Note?",
                "This note will be permanently deleted.",
                remove
            )

        gesture_text = ft.GestureDetector(
            content=text,
            on_double_tap=lambda e: edit(),
            on_long_press=lambda e: delete()
        )

        content.controls.append(
            ft.Container(
                content=ft.Column(
                    controls=[
                        gesture_text,
                        ft.Text(
                            note.get("category", "General"),
                            size=11,
                            color=GREY
                        ),
                        ft.Text(
                            note.get("time", ""),
                            size=10,
                            color="#999999"
                        )
                    ],
                    spacing=5
                ),
                padding=14,
                margin=ft.Margin(bottom=10),
                bgcolor=WHITE,
                border_radius=18,
                border=ft.Border.all(
                    1,
                    LIGHT_GREY
                ),
                width=float("inf")
            )
        )

    def show_notes():
        content.controls.clear()

        content.controls.append(
            ft.Container(
                content=ft.Row(
                    controls=[
                        section_title(
                            "My Notes",
                            f"{len(notes)} saved note(s)"
                        ),
                        ft.Container(
                            content=ft.IconButton(
                                icon=ft.Icons.ADD,
                                icon_color=WHITE,
                                icon_size=25,
                                on_click=show_create_note
                            ),
                            width=48,
                            height=48,
                            alignment=ft.Alignment.CENTER,
                            bgcolor=RED,
                            border_radius=15
                        )
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=18
            )
        )

        if not notes:
            content.controls.append(
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(
                                content=ft.Text(
                                    "📝",
                                    size=38
                                ),
                                width=80,
                                height=80,
                                alignment=ft.Alignment.CENTER,
                                bgcolor=BLUE_LIGHT,
                                border_radius=25
                            ),
                            ft.Text(
                                "No notes yet",
                                size=20,
                                weight=ft.FontWeight.BOLD
                            ),
                            ft.Text(
                                "Tap + to write something.",
                                color=GREY
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=8
                    ),
                    padding=40,
                    alignment=ft.Alignment.CENTER
                )
            )
        else:
            for number, note in enumerate(notes, start=1):
                make_note_card(number, note)

        page.update()

    def show_search():
        content.controls.clear()

        search = ft.TextField(
            hint_text="Search your notebook...",
            prefix_icon=ft.Icons.SEARCH,
            border_radius=14
        )

        results = ft.Column(
            spacing=8
        )

        def perform_search(e):
            results.controls.clear()

            query = (search.value or "").lower().strip()

            if not query:
                page.update()
                return

            found = False

            for number, task in enumerate(tasks, start=1):
                if query in task.get(
                    "text",
                    ""
                ).lower():

                    found = True

                    results.controls.append(
                        make_card(
                            ft.Row(
                                controls=[
                                    ft.Icon(
                                        ft.Icons.CHECK,
                                        color=RED
                                    ),
                                    ft.Text(
                                        f"Task {number}: "
                                        f"{task.get('text', '')}",
                                        expand=True
                                    )
                                ]
                            ),
                            padding=13
                        )
                    )

            for number, note in enumerate(notes, start=1):
                if query in note.get(
                    "text",
                    ""
                ).lower():

                    found = True

                    results.controls.append(
                        make_card(
                            ft.Row(
                                controls=[
                                    ft.Text("📝"),
                                    ft.Text(
                                        f"Note {number}: "
                                        f"{note.get('text', '')}",
                                        expand=True
                                    )
                                ]
                            ),
                            padding=13
                        )
                    )

            if not found:
                results.controls.append(
                    ft.Text(
                        "Nothing found.",
                        color=GREY
                    )
                )

            page.update()

        search.on_change = perform_search

        content.controls.extend([
            ft.Container(
                content=section_title(
                    "Search",
                    "Find anything you've saved."
                ),
                padding=18
            ),
            ft.Container(
                content=search,
                padding=18
            ),
            ft.Container(
                content=results,
                padding=18
            )
        ])

        page.update()

    def show_settings():
        content.controls.clear()

        theme_switch = ft.Switch(
            label="Dark mode",
            value=(
                page.theme_mode == ft.ThemeMode.DARK
            )
        )

        def change_theme(e):
            page.theme_mode = (
                ft.ThemeMode.DARK
                if theme_switch.value
                else ft.ThemeMode.LIGHT
            )

            page.update()

        theme_switch.on_change = change_theme

        def change_name(e):
            ask_name()

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

        premium_card = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Text(
                                    "⭐",
                                    size=25
                                ),
                                width=45,
                                height=45,
                                alignment=ft.Alignment.CENTER,
                                bgcolor="#FFEBC1",
                                border_radius=13
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        "Notebook Premium",
                                        size=18,
                                        weight=ft.FontWeight.BOLD
                                    ),
                                    ft.Text(
                                        "₦500 / month",
                                        size=13,
                                        color=GREY
                                    )
                                ],
                                spacing=2,
                                expand=True
                            )
                        ]
                    ),
                    ft.Divider(),
                    ft.Text(
                        "Premium features",
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Text(
                        "• Advanced reminders\n"
                        "• More customization\n"
                        "• Premium notebook tools\n"
                        "• More productivity features"
                    ),
                    ft.Button(
                        content=ft.Text("View Premium"),
                        icon=ft.Icons.STAR_OUTLINE,
                        bgcolor=RED,
                        color=WHITE,
                        on_click=lambda e: show_premium()
                    )
                ],
                spacing=8
            ),
            padding=17,
            bgcolor=YELLOW_LIGHT,
            border_radius=18,
            border=ft.Border.all(
                1,
                "#F3D99A"
            )
        )

        content.controls.extend([
            ft.Container(
                content=section_title(
                    "Settings",
                    "Make Notebook feel like yours."
                ),
                padding=18
            ),
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Icon(
                                ft.Icons.PERSON_OUTLINE,
                                color=RED
                            ),
                            width=42,
                            height=42,
                            alignment=ft.Alignment.CENTER,
                            bgcolor=RED_LIGHT,
                            border_radius=13
                        ),
                        ft.Text(
                            user_name
                            if user_name
                            else "Set your name",
                            expand=True
                        ),
                        ft.IconButton(
                            icon=ft.Icons.EDIT_OUTLINED,
                            on_click=change_name
                        )
                    ],
                    spacing=10
                ),
                padding=15,
                margin=ft.Margin(
                    left=18,
                    right=18,
                    bottom=12
                ),
                bgcolor=WHITE,
                border_radius=18,
                border=ft.Border.all(
                    1,
                    LIGHT_GREY
                )
            ),
            ft.Container(
                content=theme_switch,
                padding=14,
                margin=ft.Margin(
                    left=18,
                    right=18,
                    bottom=12
                ),
                bgcolor=WHITE,
                border_radius=18,
                border=ft.Border.all(
                    1,
                    LIGHT_GREY
                )
            ),
            ft.Container(
                content=premium_card,
                padding=18
            ),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "Storage",
                            size=18,
                            weight=ft.FontWeight.BOLD
                        ),
                        ft.Text(
                            f"{len(tasks)} tasks • "
                            f"{len(notes)} notes",
                            color=GREY
                        ),
                        ft.Button(
                            content=ft.Text("Clear All Data"),
                            icon=ft.Icons.DELETE_FOREVER,
                            bgcolor=RED,
                            color=WHITE,
                            on_click=clear_all
                        )
                    ],
                    spacing=8
                ),
                padding=18,
                margin=ft.Margin(
                    left=18,
                    right=18,
                    top=12,
                    bottom=30
                ),
                bgcolor=WHITE,
                border_radius=18,
                border=ft.Border.all(
                    1,
                    LIGHT_GREY
                )
            )
        ])

        page.update()

    def show_premium():
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                "⭐ Notebook Premium",
                weight=ft.FontWeight.BOLD
            ),
            content=ft.Column(
                controls=[
                    ft.Text(
                        "₦500 / month",
                        size=25,
                        weight=ft.FontWeight.BOLD,
                        color=RED
                    ),
                    ft.Text(
                        "Premium payment will be connected later."
                    ),
                    ft.Text(
                        "For now, Premium remains a preview."
                    )
                ],
                tight=True,
                spacing=10
            ),
            actions=[
                ft.TextButton(
                    "Close",
                    on_click=lambda e: (
                        setattr(
                            dialog,
                            "open",
                            False
                        ),
                        page.update()
                    )
                )
            ]
        )

        page.show_dialog(dialog)

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
                selected_icon=ft.Icons.SEARCH,
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
        ft.SafeArea(
            content=content,
            expand=True
        ),
        navigation
    )

    if not user_name:
        page.update()
        ask_name()
    else:
        show_home()


ft.run(main)