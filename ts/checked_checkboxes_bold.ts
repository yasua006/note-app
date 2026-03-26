import { main_elem } from "./modules/main_elem_var";

const target_checkboxes: NodeListOf<HTMLInputElement> =
    main_elem.querySelectorAll(
        "input[value='1'][type='checkbox']"
    );

target_checkboxes.forEach((target_checkbox) => {
    const description_id: string =
        target_checkbox.id.replaceAll(
            "task-done-",
            "todo-description-"
        );

    const target_descriptions: NodeListOf<HTMLLIElement> =
        main_elem.querySelectorAll(
            `p[id^=${description_id}]`
        );

    target_descriptions.forEach((target_desc) => {
        target_desc.style.textDecoration = "line-through";
    });
});
