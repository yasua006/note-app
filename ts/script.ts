const main_elem: HTMLElement =
    document.body.querySelector("main");

const handle_note_deletions = async (
    delete_note_btn: HTMLButtonElement
): Promise<void> => {
    const delete_note_btn_id_ending: string =
        delete_note_btn.id.replaceAll(
            "delete-note-btn-",
            ""
        );

    const id: string =
        "note-id-" + delete_note_btn_id_ending;

    const matching_note_id: string =
        main_elem.querySelector("#" + id).textContent;

    const confirm_result: boolean = confirm(
        "Are you sure you want to delete the note? "
    );

    if (!confirm_result) return;

    try {
        const res: Response = await fetch(
            `/delete-note?id=${matching_note_id}`,
            { method: "DELETE" }
        );

        if (!res.ok) {
            throw new Error("Note deletion not ok!");
        }

        // console.info("Delete note result:", res.json());

        location.reload();
    } catch (err) {
        alert(
            "Error: Note deletion failed! Please try again later!"
        );
        throw new Error(
            `Cannot delete matching note! ${err}`
        );
    }
};

const handle_todo_deletions = async (
    delete_todo_btn: HTMLButtonElement
): Promise<void> => {
    const delete_todo_btn_id_ending: string =
        delete_todo_btn.id.replaceAll(
            "delete-todo-btn-",
            ""
        );
    const id: string =
        "todo-id-" + delete_todo_btn_id_ending;

    const matching_todo_id: string =
        main_elem.querySelector("#" + id).textContent;

    const confirm_result: boolean = confirm(
        "Are you sure you want to delete the TODO? "
    );

    if (!confirm_result) return;

    try {
        const res: Response = await fetch(
            `/delete-todo?id=${matching_todo_id}`,
            { method: "DELETE" }
        );

        if (!res.ok) {
            throw new Error("TODO deletion not ok!");
        }

        // console.info("Delete TODO result:", res.json());

        location.reload();
    } catch (err) {
        alert(
            "Error: TODO deletion failed! Please try again later!"
        );
        throw new Error(
            `Cannot delete matching TODO! ${err}`
        );
    }
};

const handle_note_edits = async (
    edit_note_btn: HTMLButtonElement
): Promise<void> => {
    const edit_note_btn_id_ending: string =
        edit_note_btn.id.replaceAll("edit-note-btn-", "");

    const id: string = "note-id-" + edit_note_btn_id_ending;

    const matching_note_id: string =
        main_elem.querySelector("#" + id).textContent;
    const matching_note_title: string = main_elem
        .querySelector("[id^='note-title-']")
        .querySelector("h3").textContent;
    const matching_note_description: string =
        main_elem.querySelector(
            "[id^='note-description-']"
        ).textContent;

    const edit_title_prompt: string = prompt(
        `Current title: ${matching_note_title}`
    );
    const edit_description_prompt: string = prompt(
        `Current description: ${matching_note_description}`
    );

    if (!edit_title_prompt) return;
    if (!edit_description_prompt) return;

    try {
        const res: Response = await fetch(
            `/patch-note?title=${edit_title_prompt}&description=${edit_description_prompt}&id=${matching_note_id}`,
            { method: "PATCH" }
        );

        if (!res.ok) {
            throw new Error("Note editing not ok!");
        }

        // console.info("Edit note result:", res.json());

        location.reload();
    } catch (err) {
        alert(
            "Error: Note editing failed! Please try again later!"
        );
        throw new Error(
            `Cannot edit matching note! ${err}`
        );
    }
};

const handle_todo_edits = async (
    edit_todo_btn: HTMLButtonElement
): Promise<void> => {
    const edit_todo_btn_id_ending: string =
        edit_todo_btn.id.replaceAll("edit-todo-btn-", "");

    const id: string = "todo-id-" + edit_todo_btn_id_ending;

    const matching_todo_id: string =
        main_elem.querySelector("#" + id).textContent;
    const matching_todo_title: string = main_elem
        .querySelector("[id^='todo-title-']")
        .querySelector("h3").textContent;
    const matching_todo_description: string =
        main_elem.querySelector(
            "[id^='todo-description-']"
        ).textContent;
    const matching_task_done: string = main_elem
        .querySelector("[id^='task-done-']")
        .querySelector(
            "input[type='checkbox']"
        ).textContent;

    const edit_title_prompt: string = prompt(
        `Current title: ${matching_todo_title}`
    );
    const edit_description_prompt: string = prompt(
        `Current description: ${matching_todo_description}`
    );
    const edit_task_done_prompt: string = prompt(
        `Current task done: ${matching_task_done}`
    );

    if (!edit_title_prompt) return;
    if (!edit_description_prompt) return;
    if (!edit_task_done_prompt) return;

    try {
        const res: Response = await fetch(
            `/patch-todo?title=${edit_title_prompt}&description=${edit_description_prompt}&task_done=${edit_task_done_prompt}&id=${matching_todo_id}`,
            { method: "PATCH" }
        );

        if (!res.ok) {
            throw new Error("TODO editing not ok!");
        }

        // console.info("Edit TODO result:", res.json());

        location.reload();
    } catch (err) {
        alert(
            "Error: TODO editing failed! Please try again later!"
        );
        throw new Error(
            `Cannot edit matching TODO! ${err}`
        );
    }
};

const edit_requests = async (): Promise<void> => {
    const edit_note_buttons: NodeListOf<HTMLButtonElement> =
        main_elem.querySelectorAll(
            "[id^='edit-note-btn-']"
        );
    const edit_todo_buttons: NodeListOf<HTMLButtonElement> =
        main_elem.querySelectorAll(
            "[id^='edit-todo-btn-']"
        );

    edit_note_buttons.forEach((edit_note_btn) => {
        (edit_note_btn.addEventListener("click", async () =>
            handle_note_edits(edit_note_btn)
        ),
            { passive: true });
    });
    edit_todo_buttons.forEach((edit_todo_btn) => {
        (edit_todo_btn.addEventListener("click", async () =>
            handle_todo_edits(edit_todo_btn)
        ),
            { passive: true });
    });
};

const delete_requests = async (): Promise<void> => {
    const delete_note_buttons: NodeListOf<HTMLButtonElement> =
        main_elem.querySelectorAll(
            "[id^='delete-note-btn-']"
        );
    const delete_todo_buttons: NodeListOf<HTMLButtonElement> =
        main_elem.querySelectorAll(
            "[id^='delete-todo-btn-']"
        );

    delete_note_buttons.forEach(
        (delete_note_btn) => {
            delete_note_btn.addEventListener(
                "click",
                async () =>
                    handle_note_deletions(delete_note_btn)
            );
        },
        { passive: true }
    );
    delete_todo_buttons.forEach(
        (delete_todo_btn) => {
            delete_todo_btn.addEventListener(
                "click",
                async () =>
                    handle_todo_deletions(delete_todo_btn)
            );
        },
        { passive: true }
    );
};

const main = async () => {
    edit_requests();
    delete_requests();
};

main();
